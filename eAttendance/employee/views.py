from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from account.models import User
from .models import Designation
from attendance.models import Attendance
from tasks.models import Task
import sweetify

@login_required(login_url='login')
def employee_dashboard(request):
    if not request.user.is_superuser:
        attendance = Attendance.objects.filter(user_id=request.user.id).order_by('-created')
        tasks = Task.objects.filter(user_id=user_id).order_by('-created')
        
        context = {
            'attendance': attendance,
            'tasks': tasks
        }
        return render(request, 'employee-dashboard/index.html', context)
    
    if request.user.is_superuser:
        return render(request, 'admin-dashboard/index.html')
      
    
@login_required(login_url='login')
def designations(request):
    if request.user.is_superuser:
        designations = Designation.objects.all()
    
        if request.method == 'POST':
            title = request.POST['title']
            time_in = request.POST['time_in']
            time_out = request.POST['time_out']
            lateness_benchmark = request.POST['lateness_benchmark']
            
            if Designation.objects.filter(title=title).exists():
                sweetify.info(request, f'{title} already exists on the application.', button='Ok', timer=3000)
                return redirect("designation")
            
            else:    
                designation = Designation.objects.create(title = title, time_in = time_in, time_out = time_out, lateness_benchmark = lateness_benchmark)
                designation.save()
                sweetify.info(request, f'Designation for {title} created successfully!', button='Ok', timer=3000)
                return redirect("designation")
        else:
            return render(request, 'admin-dashboard/designation.html', {'designations':designations})
    
    if not request.user.is_superuser:
        return render(request, 'employee-dashboard/index.html')
       
    
@login_required(login_url='login')
def edit_designation(request, designation_id):
    if request.user.is_superuser:
        
        if request.method == 'POST':
            designation_update = Designation.objects.filter(pk=designation_id)
            designation_update.update(
                title = request.POST['title'],
                time_in = request.POST['time_in'],
                time_out = request.POST['time_out'],
                lateness_benchmark = request.POST['lateness_benchmark'],
            )
            sweetify.info(request, f'Designation updated successfully!', button='Ok', timer=3000)
            return redirect("designation")
            
        else:
            designations = Designation.objects.all()
            designation_edit = get_object_or_404(Designation, pk=designation_id)
            context = {
                'designations': designations,
                'designation_edit': designation_edit,
            }
            return render(request, 'admin-dashboard/designation.html', context)
    
    if not request.user.is_superuser:
        return render(request, 'employee-dashboard/index.html')
    
   
        
@login_required(login_url='login')
def all_employees(request):
    if request.user.is_superuser:
        all_employees = User.objects.filter(is_superuser=0)
        # print(all_employees)
        return render(request, 'admin-dashboard/all-employees.html', {'all_employees':all_employees})
    
    if not request.user.is_superuser:
        return render(request, 'employee-dashboard/index.html')
    
        
        
@login_required(login_url='login')
def view_employee(request, user_id):
    if request.user.is_superuser:
        designations = Designation.objects.all()
        employee = get_object_or_404(User, pk=user_id)
        attendance = Attendance.objects.filter(user_id=user_id).order_by('-created')
        tasks = Task.objects.filter(user_id=user_id).order_by('-created')
        context = {
            'employee':employee, 
            'attendance': attendance,
            'designations': designations,
            'tasks': tasks
        }
        return render(request, 'admin-dashboard/view-employee.html',context)
    
    if not request.user.is_superuser:
        return render(request, 'employee-dashboard/index.html')
   
    
@login_required(login_url='login')
def delete_employee(request, user_id):
    if request.user.is_superuser:
        employee = get_object_or_404(User, pk=user_id)
        if request.method == "POST":
            employee.delete()
            sweetify.info(request, "Employee Deleted Successfully", button='Ok', timer=3000)
            return redirect("all_employees")
        context = {
           "employee" : employee
       }
        
        return render(request, 'admin-dashboard/delete-employee.html', context)
    
    if not request.user.is_superuser:
        return render(request, 'employee-dashboard/index.html')