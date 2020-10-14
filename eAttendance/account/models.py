from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils import timezone
from employee.models import Designation
import os
from PIL import Image

def photo_path(instance, filename):
    basefilename, file_extension= os.path.splitext(filename)
   
    return 'profile_images/{username}.{basename}{ext}'.format(username= instance.username, basename= basefilename, ext= file_extension)



class User(AbstractUser):
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
    mobile = models.CharField(max_length=14, blank=True)
    profile_image = models.ImageField(default='default.png', upload_to=photo_path)
    member_since = models.DateTimeField(null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE,null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=100, default='Signed Out' ,blank=True)
    ban_time = models.DateTimeField(auto_now_add=True)
    attendance_time = models.DateTimeField(default=None, null=True, blank=True)
    lateness_ago = models.CharField(max_length=20, default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    # def save(self, **kwargs):
    #     super().save()
    
    #     img = Image.open(self.image.path)
        
        
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         print()
    #         print(self.image)
    #         print()
    #         img.save(self.image.path)
            
            
@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).profile_image
    except sender.DoesNotExist:
        return False

    new_file = instance.profile_image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)