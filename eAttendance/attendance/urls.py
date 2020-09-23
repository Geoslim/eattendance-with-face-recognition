from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from . import attend_views

urlpatterns = [
   
    path('verify/', views.verify, name='verify'),
    path('genral-attendance/', attend_views.gen_attend, name='gen_attend'),
    
   
    
]