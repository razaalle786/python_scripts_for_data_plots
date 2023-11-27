import os
from PIL import Image, ImageDraw
from fpdf import FPDF

# Folder containing PNG images
image_folder = "230704_2_nosource_-1Vbias_1000G_12us_900mVthreshold_08_22_2023_001"

# Get a list of all PNG files in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith(".png")]

# Define the size of each canvas (33mm x 24mm)
canvas_width = 33
canvas_height = 24

# Number of rows and columns in the grid
rows = 12
columns = 6

# Calculate the total number of images per page
images_per_page = rows * columns

# Create a PDF document to save the canvases
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=0)

# Iterate through the image files and create pages with grids
for i in range(0, len(image_files), images_per_page):
    pdf.add_page()
    
    for j in range(images_per_page):
        index = i + j
        if index < len(image_files):
            image_file = image_files[index]
            
            # Calculate position for the current image in the grid
            row = j // columns
            col = j % columns
            x = col * canvas_width
            y = row * canvas_height

            # Open and resize the image with LANCZOS resampling
            image_path = os.path.join(image_folder, image_file)
            img = Image.open(image_path)
            img = img.resize((canvas_width, canvas_height), Image.LANCZOS)

            # Paste the resized image onto the canvas at the calculated position
            pdf.set_xy(x, y)
            pdf.image(image_path, x=x, y=y, w=canvas_width, h=canvas_height)

# Save the PDF with all the canvases
pdf_output_path = "nosource08222023.pdf"
pdf.output(pdf_output_path)
print(f"PDF saved to {pdf_output_path}")
