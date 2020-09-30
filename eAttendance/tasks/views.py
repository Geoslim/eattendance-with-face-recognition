from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from account.models import User
from .models import Task
# from attendance.models import Attendance
import sweetify



@login_required(login_url='login')
def add_task(request, user_id):
    if request.user.is_superuser:
        employee = get_object_or_404(User, pk=user_id)
        if request.method == "POST":
            # employee.delete()
            sweetify.info(request, "Task added Successfully", button='Ok', timer=3000)
            return redirect("all_employees")
        context = {
           "employee" : employee
       }
        
        return render(request, 'admin-dashboard/tasks.html', context)
    
    if not request.user.is_superuser:
        return render(request, 'employee-dashboard/index.html')