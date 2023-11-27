import os
from PIL import Image
from fpdf import FPDF

# Folder containing PNG images
image_folder = "230704_2_nosource_-1Vbias_1000G_12us_900mVthreshold_08_22_2023_001"

# Folder to store resized images
output_folder = "resized_images"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

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

# Function to add a new page to the PDF
def add_new_page():
    pdf.add_page()
    pdf.set_xy(0, 0)

# Initialize the first page
add_new_page()

# Counter to keep track of images
image_counter = 0

# Iterate through the image files, create resized images, and add them to the PDF
for image_file in os.listdir(image_folder):
    if image_file.endswith(".png"):
        # Open the image
        image_path = os.path.join(image_folder, image_file)
        img = Image.open(image_path)
        
        # Resize the image with LANCZOS resampling
        img = img.resize((canvas_width, canvas_height), Image.LANCZOS)
        
        # Save the resized image to the output folder
        resized_image_path = os.path.join(output_folder, image_file)
        img.save(resized_image_path)
        
        # Calculate position for the current image in the grid
        row = image_counter // columns
        col = image_counter % columns
        x = col * canvas_width
        y = row * canvas_height

        # Add a new page if the current page is full
        if image_counter > 0 and image_counter % images_per_page == 0:
            add_new_page()

        # Paste the resized image onto the canvas at the calculated position
        pdf.image(resized_image_path, x=x, y=y, w=canvas_width, h=canvas_height)
        
        # Increment the image counter
        image_counter += 1

# Save the PDF with all the canvases
pdf_output_path = "230704_2_nosource_-1Vbias_1000G_12us_900mVthreshold_08_22_2023_001.pdf"
pdf.output(pdf_output_path)
print(f"PDF saved to {pdf_output_path}")
