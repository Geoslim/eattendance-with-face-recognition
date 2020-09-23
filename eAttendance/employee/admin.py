from django.contrib import admin
from .models import Designation

class DesignationAdmin(admin.ModelAdmin):
    list_display = ['title', 'time_in', 'time_out', 'lateness_benchmark']
admin.site.register(Designation, DesignationAdmin)