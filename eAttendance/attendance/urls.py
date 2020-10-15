from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from . import attend_views

urlpatterns = [
   
    path('verify/', views.verify, name='verify'),
    
    path('general-attendance/', attend_views.gen_attend, name='gen_attend'),
    path('general-attendance/<str:param>/', attend_views.gen_attend, name='gen_attend'),
    path('general-attendance/<str:param>/<str:param_end>/', attend_views.gen_attend, name='gen_attend'),
    
    path('general-attendance/custom/<str:param_start>/<str:param_end>/', attend_views.custom_gen_attend, name='custom_gen_attend'),
    
    path('lateness/', attend_views.lateness, name='lateness'),
    path('lateness/<str:late_param>/', attend_views.lateness, name='lateness'),
    path('lateness/<str:late_param>/<str:late_param_end>', attend_views.lateness, name='lateness'),
    
    path('lateness/custom/<str:late_param_start>/<str:late_param_end>/', attend_views.custom_lateness, name='custom_lateness'),
   
    
]