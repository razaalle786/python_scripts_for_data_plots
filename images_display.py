from PIL import Image, ImageDraw

# Create an A4 landscape-sized canvas
canvas_width = 297  # A4 landscape width in mm
canvas_height = 210  # A4 landscape height in mm
canvas = Image.new("RGB", (canvas_width, canvas_height), (255, 255, 255))
draw = ImageDraw.Draw(canvas)

# Define the position and size for each image
image_paths = ["image1.png", "image2.png", "image3.png"]  # Replace with your image paths
image_positions = [(10, 10), (60, 
