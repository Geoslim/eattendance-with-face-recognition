from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import UserRegisterForm
import sweetify
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required(login_url='login')

def register(request):
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        # sweetify.info(request, 'Message sent', button='Ok', timer=3000)
        # return redirect('register')
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            sweetify.info(request, f'Account for {username} created successfully!', button='Ok', timer=3000)
            return redirect("register")
        # username = request.POST['username'].lower()
        # last_name = request.POST['last_name']
        # first_name = request.POST['first_name']
        # email = request.POST['email'] 
        # # mobile = request.POST['mobile']
        # member_since = request.POST['member_since']
        # profile_image = request.FILES['profile_image']
        # password = make_password('password')
        # print(profile_image)
        # print(username)
        # return redirect('register')

        
        # if User.objects.filter(email=email).exists():
        #     sweetify.info(request, f'{email} is already taken.', button='Ok', timer=3000)
        #     return redirect("register")

        # else:    
        #     user = User.objects.create_user(
        #         username=username, 
        #         first_name=first_name, 
        #         last_name=last_name, 
        #         email=email, 
        #         member_since=member_since, 
        #         profile_image=profile_image, 
        #         password=password, 
        #         )
        #     user.save()
        #     sweetify.info(request, f'Account for {username} created successfully!', button='Ok', timer=3000)
        #     return redirect("register")
        
    else:
       form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

    
    

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

