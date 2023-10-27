from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from gerir_time.models import Permissoes
from .models import Notificacoes
from django.http import JsonResponse
import requests
from django.contrib.auth.models import User
from django.db import transaction

@login_required(login_url='/')
def Permissoes_Menu(request):

    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first()

    return {'permissoes':permissoes}

@login_required(login_url='/')
def Notifications(request):
    notificacoes = Notificacoes.objects.filter(user_id = request.user.id,readonly = 1).count()
    data = {'notificacoes': notificacoes}
    return JsonResponse(data)

@login_required(login_url='/')
def Notificacoes_User(request):
    notificacoes = Notificacoes.objects.filter(user_id = request.user.id).all().order_by('-data')
    notificacoes_enviadas = Notificacoes.objects.filter(origem_id = request.user.id).all().order_by('-data')
    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first()
    usuarios = User.objects.all()
    return render(request, 'notificacoes.html',{'notificacoes':notificacoes,'permissoes':permissoes,'usuarios':usuarios,'notificacoes_enviadas':notificacoes_enviadas})

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
    notificacao.readonly = 2
    notificacao.save()
    
    return render(request, 'ajax/tbl_notify_unread.html',{'notificacao':notificacao})

@login_required(login_url='/')
def Send_Notify(request):

    user_id = request.POST['user_id']
    notificacao = request.POST['notificacao']
    notify = Notificacoes.objects.create(user_id = user_id, descricao = notificacao, origem_id = request.user.id)
    return JsonResponse({"success_message": "Solicitação Realizada!"}) 

@login_required(login_url='/')
def Read_Notification(request):
    notificacao_id = request.GET['notificacao_id']
    print(notificacao_id)
   
    return JsonResponse({"success_message": "Solicitação Realizada!"}) 

@login_required(login_url='/')
def Read_All_Notifications(request):
    Notificacoes.objects.filter(user_id=request.user.id).update(readonly=2)
   
    return JsonResponse({"success_message": "Solicitação Realizada!"}) 