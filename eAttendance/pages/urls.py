from django.urls import path

from . import views
# from attendance import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.admin_dashboard, name = 'admin_dashboard'),
   
    
    # path('news/', views.news, name='news'),
    # path('contact/', views.contact, name='contact'),
    # path('destinations/', views.destinations, name='destinations'),
    # path('elements/', views.elements, name='elements'),
   
    
]