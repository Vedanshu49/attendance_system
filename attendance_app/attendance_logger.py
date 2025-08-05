import os
from datetime import datetime
import pandas as pd
from django.conf import settings
from attendance_app.models import Attendee, AttendanceRecord
from openpyxl import load_workbook

# Ensure logs folder exists
LOG_DIR = os.path.join(settings.BASE_DIR, 'attendance_logs')
os.makedirs(LOG_DIR, exist_ok=True)

def log_attendance(name, subject):
    try:
        # Get UID from DB
        attendee = Attendee.objects.get(name=name)
        uid = attendee.uid

        # Prepare today's log file
        date_str = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(LOG_DIR, f"attendance_{date_str}.xlsx")
        now = datetime.now().strftime('%H:%M:%S')

        # New attendance row
        new_entry = {"Name": name, "UID": uid, "Time": now}
        df_new = pd.DataFrame([new_entry])

        already_marked = False

        if os.path.exists(log_file):
            # File exists — check sheet
            with pd.ExcelWriter(log_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                try:
                    existing_df = pd.read_excel(log_file, sheet_name=subject)
                    if (existing_df["Name"] == name).any():
                        print(f" {name} already marked present for subject '{subject}'")
                        already_marked = True
                        return False
                except:
                    pass  # Subject sheet doesn't exist yet

                # Write to subject sheet
                df_new.to_excel(writer, sheet_name=subject, index=False, header=not writer.sheets.get(subject))
        else:
            # Create new file and first subject sheet
            with pd.ExcelWriter(log_file, engine='openpyxl') as writer:
                df_new.to_excel(writer, sheet_name=subject, index=False)

        # Log to database model
        if not already_marked:
            AttendanceRecord.objects.create(
                name=name,
                uid=uid,
                subject=subject
            )

        print(f" Logged {name} at {now} for subject: {subject}")
        return True

    except Attendee.DoesNotExist:
        print(f" Attendee '{name}' not found in DB.")
        return False

    except Exception as e:
        print(f" Error logging attendance: {e}")
        return False
