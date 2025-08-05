from PIL import Image

path = r"media/face_images/abc_BtUMs8r.jpg"  # Update this to match the filename from error

try:
    img = Image.open(path)
    print(f"Mode: {img.mode}")
    print(f"Size: {img.size}")
    print(f"Format: {img.format}")
except Exception as e:
    print(f" Error: {e}")
