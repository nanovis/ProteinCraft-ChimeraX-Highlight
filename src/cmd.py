from chimerax.core.commands import (
    CmdDesc, ColorArg, IntArg, StringArg, NoArg
)
from chimerax.atomic import ResiduesArg
from chimerax.core.colors import Color

# keep track of what we're highlighting
_highlighted = {}  # residue -> (color, width)

def highlight_info(session):
    """Print information about currently highlighted objects"""
    if not _highlighted:
        session.logger.info("No objects are currently highlighted")
        return

    session.logger.info("Currently highlighted objects:")
    for obj, (color, width) in _highlighted.items():
        session.logger.info(f"  {obj} - Color: {color}, Width: {width}")

highlight_info_desc = CmdDesc(
    synopsis='Print information about currently highlighted objects'
) 

def add_highlights(session, residues, color=Color("yellow"), width=4):
    """Add highlight outline to residues"""
    
    for r in residues:
        _highlighted[r] = (color, width)
        # Set the highlight color and width for this residue
        r.atoms.selected = True
        session.main_view.highlight_color = color.rgba
        session.main_view.highlight_thickness = width
        session.main_view.redraw_needed = True

desc_add = CmdDesc(
    synopsis='Add highlight outline to objects',
    required=[("residues", ResiduesArg)],
    keyword=[("color", ColorArg), ("width", IntArg)],
)

def remove_highlights(session, residues):
    """Remove highlight outline from residues"""
    for r in residues:
        _highlighted.pop(r, None)
        # Deselect the atoms to remove the highlight
        r.atoms.selected = False
        session.main_view.redraw_needed = True

desc_rm = CmdDesc(
    synopsis='Remove highlight outline from objects',
    required=[("residues", ResiduesArg)],
)
