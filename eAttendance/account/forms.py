from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from employee.models import Designation
import datetime

User = get_user_model()
# designations = Designation.objects.all()
# for desig in designations:
#     print(desig.title)
#     DESIGNATION_CHOICES =[('1','One'),('2','Two')]

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, help_text='100 characters max. Letters Only')
    profile_image = forms.ImageField()
    member_since = forms.DateField(initial=datetime.date.today)
    # designation  = forms.ChoiceField(required=True,)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','password1', 'password2', 'member_since','profile_image','designation']

        
# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField()
    
#     class Meta:
#         model = User
#         fields = ['username', 'email']
#         #  fields = '__all__'
#         # exclude = ['username', 'email']
# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['image']