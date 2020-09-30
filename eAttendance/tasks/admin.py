from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ['task', 'priority','status','created']
admin.site.register(Task, TaskAdmin)