from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Tarefas
# Create your views here.
@login_required(login_url='/')

def Tasks(request):
    tarefas = Tarefas.objects.all()
    
    return render(request, 'tarefas.html',{'tarefas':tarefas})