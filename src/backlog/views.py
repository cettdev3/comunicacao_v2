from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Tarefas


# Create your views here.
@login_required(login_url='/')
def Backlog(request):
    tarefas = Tarefas.objects.filter(usuario=request.user.id).all()
    
    return render(request, 'backlog.html',{'tarefas':tarefas})