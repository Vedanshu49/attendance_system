from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from .models import Attendee, AttendanceRecord

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'uid', 'image_tag')
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        if obj.face_image:
            return format_html('<img src="{}" width="100" height="100" />', obj.face_image.url)
        return "(No image)"
    
    image_tag.short_description = 'Face Image'


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'uid', 'subject', 'timestamp')
    list_filter = ('subject', 'timestamp')  #  Subject-wise + Date grouping
    search_fields = ('name', 'uid', 'subject')
    actions = ['export_as_csv']  #  Export feature

    @admin.action(description='Export selected attendance as CSV')
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=attendance_export.csv'
        writer = csv.writer(response)
        writer.writerow(['Name', 'UID', 'Subject', 'Timestamp'])

        for record in queryset:
            writer.writerow([record.name, record.uid, record.subject, record.timestamp.strftime('%Y-%m-%d %H:%M:%S')])

        return response


admin.site.register(Attendee, AttendeeAdmin)

