from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from account.models import User
# User = get_user_model()
import sweetify
import datetime 
from attendance.models import Attendance
# import timeago

def index(request):
    # datetime_str_1 = '12:55:26'
    # datetime_str_2 = '08:30:00'
    # datetime_object_1 = datetime.datetime.strptime(datetime_str_1, '%H:%M:%S').time()
    # datetime_object_2 = datetime.datetime.strptime(datetime_str_2, '%H:%M:%S').time()
    # datetime_object_3 =  datetime.datetime.combine(datetime.datetime.now(), datetime_object_1)
    # datetime_object_4 =  datetime.datetime.combine(datetime.datetime.now(), datetime_object_2)
    # print(datetime_object_1)
    # print(datetime_object_2)
    # print(datetime_object_3)
    # print(datetime_object_4)
    
    
    # print()
    # print (timeago.format(datetime_object_4, datetime_object_3))
    
    # context = {'page_title':'George'}
    return render(request, 'index.html')

@login_required(login_url='login')
def admin_dashboard(request):
    if request.user.is_superuser:
        employee_count=len(User.objects.filter(is_superuser = 0))
        today_clock_in_count=len(Attendance.objects.filter(status='Signed In'))
        today_clock_out_count=len(Attendance.objects.filter(status='Signed Out'))
       
        context = {
            'employee_count':employee_count,
            'today_clock_in_count':today_clock_in_count,
            'today_clock_out_count':today_clock_out_count,
            'page_title':'Dashboard',
        }
        return render(request, 'admin-dashboard/index.html', context)
    
    if not request.user.is_superuser:
        sweetify.info(request, 'Welcome back', button='Ok', timer=3000)
        return redirect("employee_dashboard")
        # return render(request, 'employee-dashboard/index.html')

@login_required(login_url='login')
def today(request):
    if request.user.is_superuser:
        employee_count=len(User.objects.filter(is_superuser = 0, ))
        today = datetime.date.today()
       
        today_clock_in_count=len(Attendance.objects.filter(created__gte=(today) ,status='Signed In' ))
        today_clock_out_count=len(Attendance.objects.filter(created__gte=(today) ,status='Signed Out' ))
       
        context = {
            'employee_count':employee_count,
            'today_clock_in_count':today_clock_in_count,
            'today_clock_out_count':today_clock_out_count,
            'today':today,
            'page_title':'Dashboard',
        }
        return render(request, 'admin-dashboard/index.html', context)

    
@login_required(login_url='login')
def yesterday(request):
    if request.user.is_superuser:
        employee_count=len(User.objects.filter(is_superuser = 0, ))
        today = datetime.date.today()
        print(today)
        yesterday = today - datetime.timedelta(days=1)
        print(yesterday)
        yesterday_clock_in_count=len(Attendance.objects.filter(created__range=(yesterday, today) ,status='Signed In' ))
        yesterday_clock_out_count=len(Attendance.objects.filter(created__range=(yesterday, today) ,status='Signed Out' ))
       
        context = {
            'employee_count':employee_count,
            'yesterday_clock_in_count':yesterday_clock_in_count,
            'yesterday_clock_out_count':yesterday_clock_out_count,
            'yesterday':yesterday,
            'page_title':'Dashboard',
        }
        return render(request, 'admin-dashboard/index.html', context)


@login_required(login_url='login')  
def last_7_days(request):
    if request.user.is_superuser:
        employee_count=len(User.objects.filter(is_superuser = 0, ))
        today = datetime.date.today()
        last_week = today - datetime.timedelta(days=7)
        yesterday = today - datetime.timedelta(days=1)
        last_week_clock_in_count=len(Attendance.objects.filter(created__range=(last_week, today) ,status='Signed In' ))
        last_week_clock_out_count=len(Attendance.objects.filter(created__range=(last_week, today) ,status='Signed Out' ))
       
        context = {
            'employee_count':employee_count,
            'last_week_clock_in_count':last_week_clock_in_count,
            'last_week_clock_out_count':last_week_clock_out_count,
            'today':today,
            'last_week':last_week,
            'yesterday':yesterday,
            'page_title':'Dashboard',
        }
        return render(request, 'admin-dashboard/index.html', context)
    
@login_required(login_url='login')  
def custom_range(request):  
     if request.user.is_superuser:
        start_date = request.GET['start_date']
        print(start_date)
        end_date = request.GET['end_date']
        employee_count=len(User.objects.filter(is_superuser = 0))
        today = datetime.date.today()
        last_week = today - datetime.timedelta(days=7)
        yesterday = today - datetime.timedelta(days=1)
       
        record_day_clock_in = len(Attendance.objects.filter(created__range=(start_date, end_date) ,status='Signed In'))
        record_day_clock_out = len(Attendance.objects.filter(created__range=(start_date, end_date) ,status='Signed Out'))
       
        context = {
            'employee_count':employee_count,
            'record_day_clock_in':record_day_clock_in,
            'record_day_clock_out':record_day_clock_out,
            'today':today,
            'start_date':start_date,
            'end_date':end_date,
            'last_week':last_week,
            'yesterday':yesterday,
            'page_title':'Dashboard',
        }
        return render(request, 'admin-dashboard/index.html', context)