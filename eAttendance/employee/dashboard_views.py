from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from account.models import User
from .models import Designation
from attendance.models import Attendance
import sweetify



message=len(User.objects.filter(is_superuser='Adarsh'))