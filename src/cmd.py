from chimerax.core.commands import (
    CmdDesc, ColorArg, FloatArg
)
from chimerax.atomic import ResiduesArg
from chimerax.core.colors import Color
from chimerax.core.colors import most_common_color

# keep track of what we're highlighting
_highlighted = {}  # residue -> (color, strength)

def highlight_info(session):
    """Print information about currently highlighted objects"""
    if not _highlighted:
        session.logger.info("No objects are currently highlighted")
        return

    session.logger.info("Currently highlighted objects:")
    for obj, (color, strength) in _highlighted.items():
        session.logger.info(f"  {obj} - Highlight Color: {color}, Strength: {strength}")

highlight_info_desc = CmdDesc(
    synopsis='Print information about currently highlighted objects'
) 

def _get_chain_color(residue):
    """Get the most common color of atoms in the residue's chain"""
    chain = residue.chain
    if chain is None:
        return None
    residues_list = chain.residues
    if not residues_list:
        return None
    
    # Convert list of colors to numpy array with correct dtype
    import numpy as np
    colors = np.array([residue.ribbon_color for residue in residues_list], dtype=np.uint8)
    
    return most_common_color(colors)

def _interpolate_color(color1, color2, strength):
    """Interpolate between two colors based on strength (0-1)"""
    
    # cap strength between 0.0 and 1.0
    strength = max(0.0, min(strength, 1.0))

    r1, g1, b1, a1 = color1
    r2, g2, b2, _ = color2
    r = r1 + (r2 - r1) * strength
    g = g1 + (g2 - g1) * strength
    b = b1 + (b2 - b1) * strength
    
    return (r, g, b, a1)

def add_highlights(session, residues, color=Color("red"), strength=0.5):
    """Add highlight to residues by interpolating between chain color and highlight color"""
    
    for r in residues:
        _highlighted[r] = (color, strength)
        
        # Get the chain's most common color
        chain_color = _get_chain_color(r)
        if chain_color is None:
            chain_color = Color("black")
            session.logger.warning(f"No common chain color found for residue {r.name}, using black")
        # Interpolate between chain color and highlight color
        highlight_color = _interpolate_color(chain_color, color.rgba, strength)
        
        # Update the residue's ribbon color
        r.ribbon_color = highlight_color

desc_add = CmdDesc(
    synopsis='Add residues for highlighting',
    required=[("residues", ResiduesArg)],
    optional=[("color", ColorArg), ("strength", FloatArg)],
)

def remove_highlights(session, residues):
    """Remove residues from highlighting"""
    for r in residues:
        _highlighted.pop(r, None)
        # Reset the ribbon color to the chain's color
        chain_color = _get_chain_color(r)
        if chain_color is not None:
            r.ribbon_color = chain_color

desc_rm = CmdDesc(
    synopsis='Remove residues from highlighting',
    required=[("residues", ResiduesArg)],
)
