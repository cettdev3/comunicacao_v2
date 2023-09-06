from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Tarefas
from django.db import transaction
from django.http import JsonResponse

# Create your views here.
@login_required(login_url='/')
def Backlog(request):
    tarefas = Tarefas.objects.filter(usuario=request.user.id).all()
    
    return render(request, 'backlog.html',{'tarefas':tarefas})

@login_required(login_url='/')
def Ajax_View_Task(request):
    print(request.GET)
    idtask = request.GET['tarefaId']
    tarefa = Tarefas.objects.filter(id=idtask).first()

    
    return render(request, 'ajax/ajax_view_task.html', {'tarefa': tarefa})

@login_required(login_url='/')
def Ajax_Move_Task(request):
    try:
        with transaction.atomic():

            idtask = request.GET['taskId']
            step = request.GET['step']

            tarefa = Tarefas.objects.get(id=idtask)
            tarefa.status  = step
            tarefa.save()

            tarefas = Tarefas.objects.filter(usuario_id=request.user.id).all()

            return render(request, 'ajax/ajax_move_task.html', {'tarefas': tarefas})
        
    except Exception as e:
         return JsonResponse({"error_message": "Não foi possível realizar a solicitação: " + str(e)}, status=400)