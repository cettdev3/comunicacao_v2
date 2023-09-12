from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Tarefas
from django.db import transaction
from django.http import JsonResponse
import datetime
from gerir_time.models import Permissoes
# Create your views here.
@login_required(login_url='/')
def Backlog(request):
    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first
    tarefas = Tarefas.objects.filter(usuario=request.user.id).all()
    
    return render(request, 'backlog.html',{'tarefas':tarefas,'permissoes':permissoes})

@login_required(login_url='/')
def Ajax_View_Task(request):
    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first
    idtask = request.GET['tarefaId']
    tarefa = Tarefas.objects.filter(id=idtask).first()
    
    
    return render(request, 'ajax/ajax_view_task.html', {'tarefa': tarefa,'permissoes':permissoes})

@login_required(login_url='/')
def Ajax_Move_Task(request):
    try:
        with transaction.atomic():

            idtask = request.POST['taskId']
            step = request.POST['step']
            entrega = request.POST.get('entrega')
            tarefa = Tarefas.objects.get(id=idtask)
            if entrega:
                tarefa.descricao_entrega = entrega
                tarefa.data_entrega = datetime.date.today()
            tarefa.status  = step

            tarefa.save()

            tarefas = Tarefas.objects.filter(usuario_id=request.user.id).all()

            return render(request, 'ajax/ajax_move_task.html', {'tarefas': tarefas})
        
    except Exception as e:
         return JsonResponse({"error_message": "Não foi possível realizar a solicitação: " + str(e)}, status=400)