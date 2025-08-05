# RFID and Face Match Attendance Logger

import time
import os
import sys
import django
import pyttsx3
from playsound import playsound

# 1 --- SETUP DJANGO ENVIRONMENT PROPERLY ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rfid_web.settings')
django.setup()

# 2 --- IMPORT DJANGO MODELS AND MODULES ---
from attendance_app.models import Attendee
from attendance_app.face_recognition_script import verify_face
from attendance_app.attendance_logger import log_attendance

# 3 --- SETUP TTS ENGINE ---
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# 4 --- SUBJECT INPUT ---
subject = input("Enter Subject / Lecture Name: ").strip()
if not subject:
    print("Subject is required to start attendance.")
    exit()

print(f"Attendance for subject: {subject}")
print("Test Mode: No RFID hardware connected. Using manual UID input.")
print("System Ready. Waiting for RFID...")

# 5 --- SERIAL CONNECTION (commented for test mode) ---
# import serial
# try:
#     ser = serial.Serial('COM3', 9600, timeout=1)
#     print("Connected to RFID Reader.")
# except Exception as e:
#     print(f"Error: Could not connect to serial port - {e}")
#     exit()

# 6 --- MAIN LOOP ---
while True:
    try:
        # Use manual UID input in test mode
        uid = input("Enter simulated UID: ").strip()

        # Hardware version (uncomment when hardware is used)
        # uid = ser.readline().decode().strip()

        if uid:
            print(f"RFID Detected: {uid}")

            try:
                attendee = Attendee.objects.get(uid=uid)
                name = attendee.name
                print(f"Welcome {name}")

                engine.say(f"Hello {name}, please look at the camera")
                engine.runAndWait()

                if verify_face(name):
                    log_attendance(name, subject)
                    playsound("attendance_app/static/sounds/success.wav")
                    engine.say("Attendance marked successfully")
                    engine.runAndWait()
                else:
                    print("Skipping attendance. User chose not to continue.")
                    playsound("attendance_app/static/sounds/duplicate.wav")
                    engine.say("Attendance not marked")
                    engine.runAndWait()

            except Attendee.DoesNotExist:
                print("UID not registered.")
                engine.say("UID not registered")
                engine.runAndWait()
                playsound("attendance_app/static/sounds/duplicate.wav")

            time.sleep(2)

    except KeyboardInterrupt:
        print("Program stopped manually.")
        break

    except Exception as e:
        print(f"Error occurred: {e}")

# Debug log
print(f"verify_face loaded from: {verify_face.__module__}")



