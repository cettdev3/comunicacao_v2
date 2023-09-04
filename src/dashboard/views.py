from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from login.models import Usuarios
from django.core.paginator import Paginator
from datetime import date,datetime
import datetime
from django.core import serializers
from django.http import JsonResponse
import json as j
from django.contrib.auth.models import User
from django.db import transaction

# Create your views here.
@login_required(login_url='/')
def Dashboard(request):
    userLog = request.user
    infoUserLog = Usuarios.objects.filter(user=request.user.id).values()
    data_atual = datetime.date.today()
    
   
    return render(request,'dashboard.html')