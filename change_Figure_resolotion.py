from PIL import Image
import os

# Define the folder containing the images
img_folder = r"C:\Lingling\Paper\Tree_canopy\screenshots"

# Define the desired DPI
dpi = 300

# Define the output folder
output_folder = r"C:\Lingling\Paper\Tree_canopy\output"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process each image in the folder
for filename in os.listdir(img_folder):
    if filename.endswith(".png"):  # You can add other extensions if needed
        img_path = os.path.join(img_folder, filename)
        img = Image.open(img_path)

        # Save the image with the new DPI
        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_300dpi.png")
        img.save(output_path, dpi=(dpi, dpi))

print("Processing complete.")
