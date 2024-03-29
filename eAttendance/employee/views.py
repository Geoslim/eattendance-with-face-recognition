from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from account.models import User
from .models import Designation
from attendance.models import Attendance
from tasks.models import Task
import sweetify

@login_required(login_url='login')
def employee_dashboard(request):
    if not request.user.is_superuser:
        attendance = Attendance.objects.filter(user_id=request.user).order_by('-created')
        tasks = Task.objects.filter(user_id=request.user).order_by('-created')
        pending_tasks = Task.objects.filter(user_id=request.user,status=False)
        count_pending_tasks = len(pending_tasks)
        context = {
            'attendance': attendance,
            'tasks': tasks,
            'count_pending_tasks': count_pending_tasks,
            'page_title':'Dashboard'
        }
        return render(request, 'employee-dashboard/index.html', context)
    
    if request.user.is_superuser:
        sweetify.info(request, 'Welcome back', button='Ok', timer=3000)
        return redirect("admin_dashboard")
    
    
@login_required(login_url='login')
def employee_profile(request):
    if not request.user.is_superuser:
        form = PasswordChangeForm(request.user)
        return render(request, 'employee-dashboard/profile.html', {'form': form, 'page_title':'Profile'})
    
    if request.user.is_superuser:
        sweetify.info(request, 'Welcome back', button='Ok', timer=3000)
        return redirect("admin_dashboard")
      

    
        
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
            return render(request, 'admin-dashboard/designation.html', {'designations':designations, 'page_title':'Designations'})
    
    if not request.user.is_superuser:
        sweetify.info(request, 'Welcome back', button='Ok', timer=3000)
        return redirect("employee_dashboard")
       
    
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
                'page_title':f'Edit {designation_edit.title}'
            }
            return render(request, 'admin-dashboard/designation.html', context)
    
    if not request.user.is_superuser:
        sweetify.info(request, 'Welcome back', button='Ok', timer=3000)
        return redirect("employee_dashboard")
    
   
        
@login_required(login_url='login')
def all_employees(request):
    if request.user.is_superuser:
        all_employees = User.objects.filter(is_superuser=0)
        # print(all_employees)
        return render(request, 'admin-dashboard/all-employees.html', {'all_employees':all_employees, 'page_title':'All Employees'})
    
    if not request.user.is_superuser:
        sweetify.info(request, 'Welcome back', button='Ok', timer=3000)
        return redirect("employee_dashboard")
    
        
        
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
            'tasks': tasks,
            'page_title':f'Viewing {employee.username}',
        }
        return render(request, 'admin-dashboard/view-employee.html',context)
    
    if not request.user.is_superuser:
        sweetify.info(request, 'Welcome back', button='Ok', timer=3000)
        return redirect("employee_dashboard")
   
   
@login_required(login_url='login')
def update_employee(request, user_id):
    if request.user.is_superuser:
        
        if request.method == 'POST': 
            employee_update = User.objects.filter(pk=user_id)
            employee_update.update(
                last_name = request.POST['last_name'],
                first_name = request.POST['first_name'],
                email = request.POST['email'] ,
                designation_id = request.POST['designation'],
                gender = request.POST['gender'],
                mobile = request.POST['mobile'],
                member_since = request.POST['member_since'],
                # profile_image = request.FILES['profile_image'] 
               
            )
            sweetify.info(request, f'Employee updated successfully!', button='Ok', timer=3000)
            return redirect("view_employee", user_id)
            
      
    
    if not request.user.is_superuser:
        sweetify.info(request, 'Welcome back', button='Ok', timer=3000)
        return redirect("employee_dashboard")
    
   
      
@login_required(login_url='login')
def delete_employee(request, user_id):
    if request.user.is_superuser:
        employee = get_object_or_404(User, pk=user_id)
        if request.method == "POST":
            employee.delete()
            sweetify.info(request, "Employee Deleted Successfully", button='Ok', timer=3000)
            return redirect("all_employees")
        context = {
           "employee" : employee,
            'page_title':f'Deleting {employee.username}',
       }
        
        return render(request, 'admin-dashboard/delete-employee.html', context)
    
    if not request.user.is_superuser:
        sweetify.info(request, 'Welcome back', button='Ok', timer=3000)
        return redirect("employee_dashboard")