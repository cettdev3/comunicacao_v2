from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from gerir_time.models import Permissoes
import requests

@login_required(login_url='/')
def Permissoes_Menu(request):

    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first()
    print(permissoes)

    return {'permissoes':permissoes}