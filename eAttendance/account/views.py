from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from employee.models import Designation
from .forms import UserRegisterForm
import sweetify

from PIL import Image, ImageDraw
import cv2
import face_recognition

# Create your views here.
# @login_required(login_url='login')

def register(request):
    desig = Designation.objects.all()
    
    if request.method == 'POST' and request.FILES['profile_image']:
        # form = UserRegisterForm(request.POST, request.FILES)
        # sweetify.info(request, 'Message sent', button='Ok', timer=3000)
        # return redirect('register')
        # if form.is_valid():
        #     form.save()
        #     username = form.cleaned_data.get('username')
        #     sweetify.info(request, f'Account for {username} created successfully!', button='Ok', timer=3000)
        #     return redirect("register")
        username = request.POST['username'].lower()
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        email = request.POST['email'] 
        designation = request.POST['designation']
        gender = request.POST['gender']
        mobile = request.POST['mobile']
        member_since = request.POST['member_since']
        profile_image = request.FILES['profile_image']
        
        image = face_recognition.load_image_file(profile_image)
        # Find all the faces in the image
        face_locations = face_recognition.face_locations(image)
        if len(face_locations) == 0 or len(face_locations) > 1:
            sweetify.info(request, "{} face(s) found in this photograph. Upload an image with just one face.".format(len(face_locations)), button='Ok', timer=3000)
            print()
            return redirect("register")
        
        # if len(face_locations) > 1 :
        #     sweetify.info(request, "{} face(s) found in this photograph. Upload an image with just one face.".format(len(face_locations)), button='Ok', timer=3000)
        #     print()
        #     return redirect("register")
       
        # image = cv2.imread(profile_image)
        # image_small = cv2.resize(image, (0,0), None, 0.25, 0.265)
        # image_small = cv2.cvtColor(image_small, cv2.COLOR_BGR2RGB)
        # encode = face_recognition.face_encodings(image_small)
        # if len(encode) < 0:
        #     
        #     return redirect("register")

        # print(username)
       
        
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
    #    form = UserRegisterForm()
    # return render(request, 'register.html', {'form': form})
        return render(request, 'register.html', {'desig': desig})

    
    

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

