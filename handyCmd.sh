toolshed uninstall Highlight; devel build /home/luod/ProteinCraft/python_plugins/ProteinCraft-ChimeraX-Highlight; devel install /home/luod/ProteinCraft/python_plugins/ProteinCraft-ChimeraX-Highlight exit true


from chimerax.atomic import Structure
mols = session.models.list(type = Structure)
mol = mols[0]

from chimerax.atomic import selected_residues
res = selected_residues(session)[0]