import os
from PIL import Image
import numpy as np
import cv2
import face_recognition

# === Step 1: File paths (raw string avoids backslash issues) ===
input_path = r"C:\Users\VEDANSHU\Desktop\projects\pbl project\media\face_images\aaa.jpg"
output_path = r"C:\Users\VEDANSHU\Desktop\projects\pbl project\media\face_images\aaa_cleaned.png"

# === Step 2: Ensure original image exists ===
if not os.path.exists(input_path):
    print("Input image file not found!")
    exit()

# === Step 3: Clean + Convert image ===
try:
    pil_image = Image.open(input_path).convert("RGB")
    pil_image.save(output_path, "PNG")
    print("Image re-saved with stripped metadata and clean RGB format.")
except Exception as e:
    print("Failed to re-save image:", e)
    exit()

# === Step 4: Load cleaned image with OpenCV ===
image_bgr = cv2.imread(output_path, cv2.IMREAD_COLOR)
if image_bgr is None:
    print("OpenCV failed to load the image.")
    exit()

# === Step 5: Convert BGR to RGB and force dtype to uint8 ===
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
image_rgb = np.ascontiguousarray(image_rgb, dtype=np.uint8)

# === Step 6: Verify structure ===
print(f"Shape: {image_rgb.shape}, dtype: {image_rgb.dtype}")
if image_rgb.ndim != 3 or image_rgb.shape[2] != 3 or image_rgb.dtype != np.uint8:
    print("Image is not valid 8-bit RGB format")
    exit()

# === Step 7: Try encoding face ===
try:
    encodings = face_recognition.face_encodings(image_rgb)
    if encodings:
        print("Face encoded successfully!")
    else:
        print("Face detected but could not encode.")
except Exception as e:
    print("Error loading or encoding face:", e)
