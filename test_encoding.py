import os
import cv2
import face_recognition

# Path to folder you want to scan
FOLDER_TO_SCAN = r"C:\Users\VEDANSHU\Desktop\pbl project\media\face_images"

def is_image_usable(image_path):
    try:
        img = cv2.imread(image_path)

        if img is None:
            print(f"Could not load: {image_path}")
            return False

        # Convert to RGB for face_recognition
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Try to get face encodings
        encodings = face_recognition.face_encodings(img_rgb)

        if encodings:
            print(f"Usable: {os.path.basename(image_path)} (Encodings found: {len(encodings)})")
            return True
        else:
            print(f"Not usable: {os.path.basename(image_path)} (No face encodings found)")
            return False

    except Exception as e:
        print(f"Error in {os.path.basename(image_path)}: {e}")
        return False

def scan_folder(folder):
    print(f"\n🔍 Scanning folder: {folder}\n")
    for filename in os.listdir(folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(folder, filename)
            is_image_usable(image_path)

# Run it
if __name__ == "__main__":
    scan_folder(FOLDER_TO_SCAN)
