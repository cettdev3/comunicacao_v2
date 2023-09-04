from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from datetime import date,datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from login.models import Usuarios
from django.http import JsonResponse
import json
from django.utils.html import linebreaks
from datetime import datetime


@login_required(login_url='/')
def Solicitacoes(request):

    return render(request, 'solicitacoes.html')