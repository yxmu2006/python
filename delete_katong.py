import os
from PIL import Image

# Set the directory path
dir_path = 'F:\\4k桌面\\Game'

# Create the "del" directory if it doesn't exist
del_dir = os.path.join(dir_path, 'del')
if not os.path.exists(del_dir):
    os.makedirs(del_dir)

# Define a function to check if an image is cartoon-style
def is_cartoon_image(img_file_path):
    try:
        img = Image.open(img_file_path)
        width, height = img.size
        pixels = list(img.getdata())
        for pixel in pixels:
            r, g, b = pixel[:3]  # Get the RGB values of the pixel
            if all(x > 200 for x in [r, g, b]):  # Check if the pixel is bright
                return True  # If it is, consider the image cartoon-style
        return False  # If not, consider the image non-cartoon-style
    except Exception as e:
        print(f"Failed to open {file}: {str(e)}")
        return None

# Iterate over the files in the directory
for file in os.listdir(dir_path):
    if file.endswith('.jpg') or file.endswith('.png'):
        img_file_path = os.path.join(dir_path, file)
        if is_cartoon_image(img_file_path):  # Check if the image is cartoon-style
            print(f"Found cartoon image: {file}")
            os.rename(img_file_path, os.path.join(del_dir, file))  # Move the image to the "del" directory
