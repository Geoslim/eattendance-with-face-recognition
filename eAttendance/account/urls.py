from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name = 'logout'),
    
    # path('login/', views.user_login, name = 'login'),
    path('add-employee/', views.register, name = 'register'),
    
    # path('about/', views.about, name='about'),
    # path('news/', views.news, name='news'),
    # path('contact/', views.contact, name='contact'),
    # path('destinations/', views.destinations, name='destinations'),
    # path('elements/', views.elements, name='elements'),
   
    
]