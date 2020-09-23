from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.models import User
from .models import Attendance

@login_required(login_url='login')
def gen_attend(request):
    if request.user.is_superuser:
        attendance = Attendance.objects.all().order_by('-created')
        return render(request, 'admin-dashboard/gen-attendance.html', {'attendance': attendance})
    
    if not request.user.is_superuser:
        return render(request, 'employee-dashboard/index.html')

