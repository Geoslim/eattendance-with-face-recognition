from django.urls import path

from . import views
# from attendance import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.admin_dashboard, name = 'admin_dashboard'),
   
    # path('dashboard/?=<str:getting_day>/', views.get_day, name='get_day'),
    
    path('dashboard/records/today', views.today, name='today'),
    path('dashboard/records/range', views.custom_range, name='custom_range'),
    path('dashboard/records/yesterday', views.yesterday, name='yesterday'),
    path('dashboard/records/last-7-days', views.last_7_days, name='last_7_days'),
   
    
]