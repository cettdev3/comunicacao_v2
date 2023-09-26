from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from gerir_time.models import Permissoes
from .models import Notificacoes
from django.http import JsonResponse
import requests

@login_required(login_url='/')
def Permissoes_Menu(request):

    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first()
    print(permissoes)

    return {'permissoes':permissoes}

@login_required(login_url='/')
def Notifications(request):
    notificacoes = Notificacoes.objects.filter(user_id = request.user.id,readonly = 1).count()
    data = {'notificacoes': notificacoes}
    return JsonResponse(data)

@login_required(login_url='/')
def Notificacoes_User(request):
    notificacoes = Notificacoes.objects.filter(user_id = request.user.id).all()
    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first()
    return render(request, 'notificacoes.html',{'notificacoes':notificacoes,'permissoes':permissoes})

@login_required(login_url='/')
def Get_Notifications(request):
    idNotify = request.GET['id']
    notificacao = Notificacoes.objects.filter(id=idNotify).first()
    # permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first()
    return render(request, 'ajax/modal_notifications.html',{'notificacao':notificacao})

@login_required(login_url='/')
def Read_Notify(request):
    idNotify = request.POST['id']
    notificacao = Notificacoes.objects.get(id=idNotify)
    notificacao.readonly = ''
    return render(request, 'ajax/modal_notifications.html',{'notificacao':notificacao})