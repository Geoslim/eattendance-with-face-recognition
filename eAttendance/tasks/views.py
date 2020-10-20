from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from account.models import User
from .models import Task
import sweetify

from twilio.rest import Client
import os
import environ

@login_required(login_url='login')
def add_task(request, user_id):
    if request.user.is_superuser:
        employee = get_object_or_404(User, pk=user_id)
        if request.method == "POST":
            
            user_id = request.POST['employee_id']
            task = request.POST['task']
            priority = request.POST['priority']
            
            task = Task.objects.create(
                user_id=user_id, 
                task=task, 
                priority=priority, 
                )
           
            task.save()
            env = environ.Env()
            environ.Env().read_env()
            TWILIO_NUMBER = env("TWILIO_NUMBER")
            
        # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
            twilio  = Client()

            twilio.messages.create(
                from_=TWILIO_NUMBER,
                to='whatsapp:+2347030102959',
                body=f'New Task Added. {task}. The task is marked as {priority}')
            
            sweetify.info(request, f"Task added to {employee.username} Successfully", button='Ok', timer=3000)
            return redirect("all_employees")
        context = {
           "employee" : employee,
           'page_title':f'Add Task to {employee.username}',
       }
        
        return render(request, 'admin-dashboard/tasks.html', context)
    
    if not request.user.is_superuser:
        return render(request, 'employee-dashboard/index.html')
    

@login_required(login_url='login')
def update_task(request, task_id):

    # status = request.POST['status']
    employee_id = request.POST['employee_id']
    
    employee_task = Task.objects.filter(pk=task_id)
    for task in employee_task:
        this_status = task.status
        
    if this_status == 0:
        employee_task.update(status=1)
        sweetify.info(request, f"Task marked as complete ", button='Ok', timer=3000)
        return redirect("view_employee", employee_id)
    
    if this_status == 1:
        employee_task.update(status=0)
        sweetify.info(request, f"Task marked as incomplete ", button='Ok', timer=3000)
        return redirect("view_employee", employee_id)
    


@login_required(login_url='login')
def employee_update_task(request, task_id):

    # status = request.POST['status']
    employee_id = request.POST['employee_id']
    
    employee_task = Task.objects.filter(pk=task_id)
    for task in employee_task:
        this_status = task.status
        
    if this_status == 0:
        employee_task.update(status=1)
        sweetify.info(request, f"Task marked as complete ", button='Ok', timer=3000)
        return redirect('employee_dashboard')
    
    if this_status == 1:
        employee_task.update(status=0)
        sweetify.info(request, f"Task marked as incomplete ", button='Ok', timer=3000)
        return redirect('employee_dashboard')
    



@login_required(login_url='login')
def delete_task(request, task_id):
    employee_task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        employee_task.delete()
        sweetify.info(request, "Task Deleted Successfully", button='Ok', timer=3000)
        return redirect("all_employees")
    # context = {
    #     "employee" : employee
    # }
    
    # return render(request, 'admin-dashboard/delete-employee.html', context)