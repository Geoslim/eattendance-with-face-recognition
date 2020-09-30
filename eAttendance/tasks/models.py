from django.db import models
from django.dispatch import receiver
from django.utils import timezone
import os
from account.models import User

class Task(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    task = models.CharField(max_length=200, blank=True, null=True)
    priority = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.task