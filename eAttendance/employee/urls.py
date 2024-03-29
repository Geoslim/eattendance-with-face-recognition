from django.urls import path

from .import views
# from attendance import views

urlpatterns = [
    
    path('designation/', views.designations, name = 'designation'),
    path('edit-designation/<int:designation_id>', views.edit_designation, name = 'edit_designation'),
    path('all-employees/', views.all_employees, name = 'all_employees'),
    path('view-employee/<int:user_id>', views.view_employee, name = 'view_employee'),
    path('view-employee/<int:user_id>/update', views.update_employee, name = 'update_employee'),
    path('employee/<int:user_id>/delete', views.delete_employee, name = 'delete_employee'),
    
    
    
    path('employee-dashboard/', views.employee_dashboard, name = 'employee_dashboard'),
    path('employee-profile/', views.employee_profile, name = 'employee_profile'),
    
    # path('news/', views.news, name='news'),
    # path('contact/', views.contact, name='contact'),
    # path('destinations/', views.destinations, name='destinations'),
    # path('elements/', views.elements, name='elements'),
   
    
]