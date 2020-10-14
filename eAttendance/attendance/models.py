from django.db import models
from django.dispatch import receiver
from django.utils import timezone
import os
from account.models import User

class Attendance(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    fullname = models.CharField(max_length=110, blank=True, null=True)
    email = models.CharField(max_length=110, blank=True, null=True)
    designation = models.CharField(max_length=110, blank=True, null=True)
    status = models.CharField(max_length=110, blank=True, null=True)
    late = models.BooleanField(default=False)
    lateness = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.fullname