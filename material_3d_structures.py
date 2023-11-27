from pymatgen.ext.matproj import MPRester
from ase import Atoms
from ase.visualize import view
import matplotlib.pyplot as plt

# Initialize the Materials Project API key if you have one (optional)
api_key = "13lPp3x0oEeD9YXlzDxvphf4f5UMuryl"

# Create an instance of MPRester
mpr = MPRester(api_key)

# Get the crystal structure for MAPbI3 by its Materials Project material ID
data = mpr.get_structure_by_material_id("mp-1069538")

# Separate symbols and positions
symbols = [site.specie.symbol for site in data.sites]
positions = [site.coords for site in data.sites]

# Create an ASE Atoms object from the separated data
ase_structure = Atoms(symbols=symbols, positions=positions)

# Visualize the 3D structure using ASE's view function
view(ase_structure)

# Show the 3D structure using Matplotlib (optional)
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
for atom in ase_structure:
    ax.scatter(atom.x, atom.y, atom.z, s=100, label=atom.symbol)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.legend()
plt.show()
