from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from account.models import User
# User = get_user_model()

def index(request):
    context = {'name':'George'}
    return render(request, 'index.html', context)

@login_required(login_url='login')
def admin_dashboard(request):
    if request.user.is_superuser:
        return render(request, 'admin-dashboard/index.html')
    
    if not request.user.is_superuser:
        return render(request, 'employee-dashboard/index.html')

