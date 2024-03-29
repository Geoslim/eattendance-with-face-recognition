from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .models import User
from employee.models import Designation
# from .forms import UserRegisterForm
import sweetify
from django.core.mail import EmailMessage

# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.sites.shortcuts import get_current_site

# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from PIL import Image, ImageDraw
import cv2
import face_recognition

# Create your views here.
@login_required(login_url='login')
def register(request):
    
    if request.user.is_superuser:
            # mail_subject = 'Activate your account.'
        # message = render_to_string('accounts/acc_active_email.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': default_token_generator.make_token(user),
        # })
        # to_email = form.cleaned_data.get('email')

        # email = EmailMessage(
        #             mail_subject, message, to=[to_email]
        #         )
        # email.send()
    
        desig = Designation.objects.all()
        
        if request.method == 'POST':
           
            username = request.POST['username'].lower()
            last_name = request.POST['last_name']
            first_name = request.POST['first_name']
            email = request.POST['email'] 
            designation = request.POST['designation']
            
            if 'gender' not in request.POST:
                sweetify.info(request, 'You need to Select a Gender', button='Ok', timer=3000)
                return redirect("register")
            else:
                gender = request.POST['gender']
            
            mobile = request.POST['mobile']
            member_since = request.POST['member_since']
            
            if 'profile_image' not in request.FILES:
                sweetify.info(request, 'You need to Upload an Image', button='Ok', timer=3000)
                return redirect("register")
            else:
                profile_image = request.FILES['profile_image']
            
            image = face_recognition.load_image_file(profile_image)
            # Find all the faces in the image
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) == 0 or len(face_locations) > 1:
                sweetify.info(request, "{} face(s) found in this photograph. Upload an image with just one face.".format(len(face_locations)), button='Ok', timer=3000)
                print()
                return redirect("register")
        
            
            if User.objects.filter(email=email).exists():
                sweetify.info(request, f'{email} is already taken.', button='Ok', timer=3000)
                return redirect("register")
            
            elif User.objects.filter(username=username).exists():
                sweetify.info(request, f'{username} is already taken.', button='Ok', timer=3000)
                return redirect("register")

            else:    
                user = User.objects.create_user(
                    username=username, 
                    first_name=first_name, 
                    last_name=last_name, 
                    email=email, 
                    gender=gender, 
                    mobile=mobile, 
                    member_since=member_since, 
                    designation_id=designation, 
                    profile_image=profile_image, 
                    
                    )
                password = User.objects.make_random_password(length=14, allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMONPQRSTUVWXYZ023456789")
                print()
                print(password)
                print()
                user.set_password(password)
                user.save()
                sweetify.info(request, f'Account for {username} created successfully!', button='Ok', timer=3000)
                return redirect("register")
            
        else:
        
            return render(request, 'register.html', {'desig': desig, 'page_title':'Add New Employee'})
        
    if not request.user.is_superuser:
        sweetify.info(request, 'Welcome back', button='Ok', timer=3000)
        return redirect("employee_dashboard")

    
    

# def user_login(request):
#     logout(request)
#     username = password = ''
#     if request.POST:
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 # return redirect('dashboard')
    
#     return render(request, 'login.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            sweetify.success(request, 'Your password was successfully updated!')
            return redirect('employee_profile')
        else:
            sweetify.error(request, 'Please correct the error below.')
            return redirect('employee_profile')
    # else:
    #     form = PasswordChangeForm(request.user)
    # return render(request, 'accounts/change_password.html', {
    #     'form': form
    # })