from django.contrib import admin
from .models import Attendance

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'email','designation', 'status', 'created']
admin.site.register(Attendance, AttendanceAdmin)