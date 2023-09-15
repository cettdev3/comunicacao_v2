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
from django.contrib.auth.models import User
# Create your views here.
@login_required(login_url='/')
def Backlog(request):
    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first
    tarefas = Tarefas.objects.filter(usuario=request.user.id).all()
    
    return render(request, 'backlog.html',{'tarefas':tarefas,'permissoes':permissoes})

@login_required(login_url='/')
def Ajax_View_Task(request):
    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first()
    idtask = request.GET['tarefaId']
    url_atual = request.GET['urlAtual']
    tarefa = Tarefas.objects.filter(id=idtask).first()
    idEntregavel = tarefa.entregavel_id
    allTasks = Tarefas.objects.filter(entregavel_id=idEntregavel).all()

    try:
        arquivos = tarefa.arquivos
        arquivos_list = ast.literal_eval(arquivos)
    except:
        arquivos_list = None



    return render(request, 'ajax/ajax_view_task.html', {'tarefa': tarefa,'permissoes':permissoes,'arquivos':arquivos_list,'url_atual':url_atual,'allTasks':allTasks})
        

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
        
@login_required(login_url='/')
def Ajax_Edit_Task(request):
    tarefaId = request.GET['tarefaId']
    tarefa = Tarefas.objects.filter(id=tarefaId).first()
    usuarios = User.objects.all().order_by('first_name')
    return render(request, 'ajax/ajax_edit_stask.html', {'tarefa': tarefa,'usuarios':usuarios})

        
@login_required(login_url='/')
def Ajax_Altera_Task(request):
    with transaction.atomic():
        tarefaId = request.POST.get('tarefa_edit_id')
        status_tarefa_edit = request.POST.get('status_tarefa_edit',None)
        tarefa = Tarefas.objects.get(id=tarefaId)
        tarefa.prazo_entrega = request.POST.get('prazo_modal_edit','')
        tarefa.titulo_tarefa = request.POST.get('titulo_tarefa_edit','')
        tarefa.prioridade = request.POST.get('prioridade_modal_edit','')
        if status_tarefa_edit != '4':
            tarefa.status = status_tarefa_edit
        tarefa.descricao_tarefa = request.POST.get('descricao_task_edit','')
        tarefa.usuario_id = request.POST.get('designar_usuario_edit','')
        tarefa.save()
        return JsonResponse({"success_message": "Tarefa Editada!"})

@login_required(login_url='/')
def Ajax_Task_For_Task(request):
    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first()
    idtask = request.GET['tarefaId']
    url_atual = request.GET['urlAtual']
    tarefa = Tarefas.objects.filter(id=idtask).first()
    idEntregavel = tarefa.entregavel_id
    allTasks = Tarefas.objects.filter(entregavel_id=idEntregavel).all()

    try:
        arquivos = tarefa.arquivos
        arquivos_list = ast.literal_eval(arquivos)
    except:
        arquivos_list = None

    return render(request, 'ajax/ajax_view_task_ftask.html', {'tarefa': tarefa,'permissoes':permissoes,'arquivos':arquivos_list,'url_atual':url_atual,'allTasks':allTasks})
