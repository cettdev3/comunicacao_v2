from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Tarefas
from django.db import transaction
from django.http import JsonResponse
import datetime
from gerir_time.models import Permissoes
from django.core.files.storage import FileSystemStorage
import json
import ast
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
    try:
        arquivos = tarefa.arquivos
        arquivos_list = ast.literal_eval(arquivos)
    except:
        arquivos_list = None

    
    return render(request, 'ajax/ajax_view_task.html', {'tarefa': tarefa,'permissoes':permissoes,'arquivos':arquivos_list})

@login_required(login_url='/')
def Ajax_Move_Task(request):

    with transaction.atomic():
        print(request.POST)
        idtask = request.POST['taskId']
        step = request.POST['step']
        entrega = request.POST.get('entrega',None)
        if entrega == 'undefined':
            entrega = None
        try:
            arquivos_task = []
            arquivos = request.FILES.getlist('files[]')
            for arquivo in arquivos:
                fs1 = FileSystemStorage()
                filename1 = fs1.save(arquivo.name, arquivo)
                arquivo_url = fs1.url(filename1)
                arquivos_task.append(arquivo_url)
        except:
            arquivo_url = ''

        tarefa = Tarefas.objects.get(id=idtask)

        tarefa.descricao_entrega = entrega
        tarefa.data_entrega = datetime.date.today()
        
        tarefa.status  = step
        tarefa.arquivos = arquivos_task
        tarefa.save()

        tarefas = Tarefas.objects.filter(usuario_id=request.user.id).all()

        return render(request, 'ajax/ajax_move_task.html', {'tarefas': tarefas})
        
