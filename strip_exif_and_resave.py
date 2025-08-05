from PIL import Image
import os

img_path = r"media/face_images/abc_BtUMs8r.jpg"  # Change to your image name
img = Image.open(img_path).convert("RGB")

# Overwrite the image without EXIF metadata
img.save(img_path, format="JPEG", quality=95, subsampling=0)

print(f"Cleaned and saved image without EXIF: {img_path}")
