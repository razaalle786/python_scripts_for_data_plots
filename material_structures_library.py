from pymatgen.ext.matproj import MPRester

# Initialize the Materials Project API key if you have one (optional)
api_key = "Zglv6WKzMfY5QzPJYjByzwFTwVwoBGHW"

# Create an instance of MPRester
mpr = MPRester(api_key)

# Search for the structure of MAPbI3 using the new method
data = mpr.get_structure_by_material_id("mp-567290")

# Print the crystal structure
print(data)
