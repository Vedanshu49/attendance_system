from django.db import models

class Attendee(models.Model):
    name = models.CharField(max_length=100)
    uid = models.CharField(max_length=100, unique=True)
    face_image = models.ImageField(upload_to='face_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.uid})"


class AttendanceRecord(models.Model):
    name = models.CharField(max_length=100)
    uid = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

