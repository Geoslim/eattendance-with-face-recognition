from django.urls import path

from . import views
# from attendance import views

urlpatterns = [
    path('<int:user_id>/add/', views.add_task, name='add_task')
    # path('edit/', views.edit_task, name='edit_task')
   
]