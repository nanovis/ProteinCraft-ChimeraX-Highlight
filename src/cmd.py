from chimerax.core.commands import (
    CmdDesc, ColorArg, IntArg, StringArg, NoArg
)
from chimerax.atomic import ResiduesArg

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

def add_highlights(session, residues, color="yellow", width=4):
    for r in residues:
        _highlighted[r] = (color, width)

desc_add = CmdDesc(
    synopsis='Add silhouette highlight to objects',
    required=[("residues", ResiduesArg)],
    keyword=[("color", ColorArg), ("width", IntArg)],
)

def remove_highlights(session, residues):
    for r in residues:
        _highlighted.pop(r, None)

desc_rm = CmdDesc(
    synopsis='Remove silhouette highlight from objects',
    required=[("residues", ResiduesArg)],
)
