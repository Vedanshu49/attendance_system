cd /d "%~dp0"

start "DjangoServer" cmd /k "python manage.py runserver"
start "ReaderScript" cmd /k "python attendance_app/rfid_reader.py"
