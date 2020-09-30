from django.urls import path

from . import views
# from attendance import views

urlpatterns = [
    path('<int:user_id>/add/', views.add_task, name='add_task'),
    path('<int:task_id>/update/', views.update_task, name='update_task'),
    path('<int:task_id>/delete', views.delete_task, name = 'delete_task'),
   
]