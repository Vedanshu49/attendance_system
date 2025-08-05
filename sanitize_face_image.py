from PIL import Image
import os

# Directory containing face images
face_dir = os.path.join("media", "face_images")

# Loop through all images in the folder
for filename in os.listdir(face_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        path = os.path.join(face_dir, filename)
        try:
            with Image.open(path) as img:
                # Remove metadata and convert to RGB
                clean = img.convert("RGB")
                # Save as .jpg (even if original is png)
                new_path = os.path.splitext(path)[0] + ".jpg"
                clean.save(new_path, format="JPEG", quality=95)
                print(f"Cleaned and saved: {new_path}")

                # Remove old file if different
                if path != new_path:
                    os.remove(path)

        except Exception as e:
            print(f"Failed to process {filename}: {e}")
