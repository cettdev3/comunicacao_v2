from django.shortcuts import render, redirect
from login.models import Usuarios
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
import requests

def marcar_notificacao_lida(request):
    print(request.GET)
    notification = Notification.objects.get(id=request.GET['notificacao'])
    notification.unread = False
    notification.save()
    unread_notifications = Notification.objects.unread().filter(recipient=request.user.id)
    total_notificacoes =  notify_unread(request.user).count()
    return render(request, 'ajax/bell.html', {'notificacoes': unread_notifications,'count':total_notificacoes})

#NOTIFICAÇÕES NÃO LIDAS
def notify_unread(user):
    unread_notifications = Notification.objects.unread().filter(recipient=user)
    return unread_notifications

# Create your views here.
@login_required(login_url='/')
def Permissoes_Menu(request):
    unread_notifications =  notify_unread(request.user)
    total_notificacoes =  notify_unread(request.user).count()
    print(total_notificacoes)
    info = Usuarios.objects.filter(user=request.user.id).values()
    permissoes = info[0]['permissoes']

    return {'permissoes':permissoes,'notificacoes':unread_notifications,'count':total_notificacoes}

