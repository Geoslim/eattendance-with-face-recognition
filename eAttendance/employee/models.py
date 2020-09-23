from django.db import models
from django.dispatch import receiver
from django.utils import timezone
import os
from PIL import Image

class Designation(models.Model):
    
    title = models.CharField(max_length=110, blank=True)
    time_in = models.CharField(max_length=110, blank=True, null=True)
    time_out = models.CharField(max_length=110, blank=True, null=True)
    lateness_benchmark = models.CharField(max_length=110, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title