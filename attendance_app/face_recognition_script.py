import os
import cv2
import numpy as np
import time
from django.conf import settings
from django.shortcuts import get_object_or_404
from attendance_app.models import Attendee
import traceback

def verify_face(expected_name, test_mode=False):
    try:
        # Load attendee and face image
        attendee = get_object_or_404(Attendee, name=expected_name)
        image_path = os.path.join(settings.MEDIA_ROOT, str(attendee.face_image))
        print(f"Loading face image from: {image_path}")

        if not os.path.exists(image_path):
            raise FileNotFoundError("Face image not found.")

        registered_face = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if registered_face is None:
            raise ValueError("Unable to read registered face image.")

        registered_face = cv2.resize(registered_face, (200, 200))

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train([registered_face], np.array([0]))

        while True:
            cap = None
            for i in range(3):
                cam = cv2.VideoCapture(i)
                if cam.isOpened():
                    cap = cam
                    print(f"Webcam opened at index {i}")
                    break
            if cap is None:
                raise RuntimeError("Webcam not found.")

            print("Look at the camera. Press 'q' to cancel.")
            match_found = False
            start_time = time.time()

            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            while True:
                ret, frame = cap.read()
                if not ret:
                    continue

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    face_roi = gray[y:y+h, x:x+w]
                    face_resized = cv2.resize(face_roi, (800, 800))
                    label, confidence = recognizer.predict(face_resized)

                    print(f"Confidence: {confidence}")
                    if confidence < 118:
                        match_found = True
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame, "Match!", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        break
                    else:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        cv2.putText(frame, "Not Match", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                cv2.imshow("Face Verification", frame)

                if match_found:
                    print("Face Verified!")
                    break
                if time.time() - start_time > 120:
                    print("Timeout.")
                    break
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Cancelled.")
                    break

            cap.release()
            cv2.destroyAllWindows()

            if match_found:
                return True
            else:
                retry = input("Face not verified. Try again? (yes/no): ").strip().lower()
                if retry == 'yes':
                    continue
                else:
                    choice = input("Do you want to continue anyway? (yes/no): ").strip().lower()
                    return choice == 'yes'

    except Exception as e:
        print("Error during face verification:")
        traceback.print_exc()
        if test_mode:
            print("Proceeding anyway (test mode).")
            return True
        else:
            choice = input("System error. Do you want to continue anyway? (yes/no): ").strip().lower()
            return choice == 'yes'



