import os
import sys
import django

#  Setup Django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rfid_web.settings')  # Replace with your actual Django project name
django.setup()


from attendance_app.models import Attendee

updated = 0

for attendee in Attendee.objects.all():
    old_path = attendee.face_image.name  # e.g. face_images/aaa.png
    base, ext = os.path.splitext(old_path)

    new_path = f"{base}.jpg"

    # Only change if file exists
    full_path = os.path.join("media", new_path)
    if os.path.exists(full_path):
        attendee.face_image.name = new_path
        attendee.save()
        print(f" Updated: {attendee.name} → {new_path}")
        updated += 1
    else:
        print(f" File not found for: {attendee.name} → expected at: {full_path}")

print(f"\n Done. {updated} records updated.")
