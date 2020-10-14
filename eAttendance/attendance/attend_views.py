from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.models import User
from .models import Attendance
import datetime 


@login_required(login_url='login')
def gen_attend(request, param=None, param_end=None):
    
    if request.user.is_superuser:
        today = datetime.date.today()
        last_week = today - datetime.timedelta(days=7)
        yesterday = today - datetime.timedelta(days=1)
        
        if param is not None:
            new_param = datetime.datetime.strptime(param, '%Y-%m-%d').date()
            # res = isinstance(new_param, str) 
        
        if param == None:
            attendance = Attendance.objects.all().order_by('-created')
            return render(request, 'admin-dashboard/gen-attendance.html', {'attendance': attendance, 'page_title':'General Attendance'})
        
        if new_param == today:
            attendance = Attendance.objects.filter(created__gte=(param)).order_by('-created')
            return render(request, 'admin-dashboard/gen-attendance.html', {'attendance': attendance, 'page_title':'General Attendance'})
        
        if new_param == yesterday:
            attendance = Attendance.objects.filter(created__range=(yesterday, today)).order_by('-created')
            return render(request, 'admin-dashboard/gen-attendance.html', {'attendance': attendance, 'page_title':'General Attendance'})

        if new_param == last_week:
            attendance = Attendance.objects.filter(created__range=(last_week, today)).order_by('-created')
            return render(request, 'admin-dashboard/gen-attendance.html', {'attendance': attendance, 'page_title':'General Attendance'})
        
        return render(request, 'admin-dashboard/index.html')
    
    if not request.user.is_superuser:
        return render(request, 'employee-dashboard/index.html')
    
    
@login_required(login_url='login')
def custom_gen_attend(request, param_start, param_end):
    
    if request.user.is_superuser:
        if param_start is not None:
            
            start_param = datetime.datetime.strptime(param_start, '%Y-%m-%d').date() 
            end_param = datetime.datetime.strptime(param_end, '%Y-%m-%d').date() + datetime.timedelta(days=1)
            
            attendance = Attendance.objects.filter(created__range=(start_param, end_param)).order_by('-created')
            return render(request, 'admin-dashboard/gen-attendance.html', {'attendance': attendance, 'page_title':'General Attendance'})
        
        return render(request, 'admin-dashboard/index.html')

    if not request.user.is_superuser:
        return render(request, 'employee-dashboard/index.html')

