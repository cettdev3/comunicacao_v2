from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from solicitacoes.models import Escolas
from .models import Permissoes,Departamentos
from django.contrib import messages
from django.db import transaction

# Create your views here.
@login_required(login_url='/')
def Gerir_time(request):
    #users = User.objects.select_related('user_id').values('id', 'email','first_name', 'username', 'usuarios__unidade__nome').values('id','email', 'first_name', 'username', 'usuarios__unidade__nome')
    usuarios = User.objects.all()
    unidades = Escolas.objects.all()
    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first
    departamentos = Departamentos.objects.all()
    users = User.objects.select_related('user_id').values('id', 'email','first_name', 'username', 'permissoes__unidade__nome','permissoes__departamento__departamento','permissoes__unidade__convenio').values('id','email', 'first_name', 'username', 'permissoes__unidade__nome','permissoes__departamento__departamento','permissoes__unidade__convenio')
    return render(request, 'gerir_time.html',{'usuarios':usuarios,'unidades':unidades,'permissoes':permissoes,'departamentos':departamentos,'users':users})

@login_required(login_url='/')
def Ajax_load_unidade(request):
    userId = request.GET['userid']
    dados = Permissoes.objects.filter(usuario_id = userId).first()

    unidades = Escolas.objects.all()
    unidade = dados.unidade_id
    return render(request, 'ajax/ajax_unidade.html', {'unidade': unidade,'unidades':unidades})

@login_required(login_url='/')
def Ajax_load_permissoes(request):
    userId = request.GET['userid']
    dados = Permissoes.objects.filter(usuario_id = userId).first()
    unidades = Escolas.objects.all()
    permissoes  = dados
    return render(request, 'ajax/ajax_permissoes.html', {'permissoes': permissoes})

@login_required(login_url='/')
def Cadastrar_usuario(request):
    nome_completo = request.POST['nome_completo']
    usuario = request.POST['usuario']
    senha = request.POST['senha']
    email = request.POST['email']
    departamento =  request.POST['departamento']
    unidade_user = request.POST['unidade_user']


    criar_usuario = User.objects.create_user(username=usuario,password=senha,email=email,first_name=nome_completo)
    create_table = Permissoes.objects.create(usuario_id = criar_usuario.id,permissao='',unidade_id=unidade_user,departamento_id=departamento)
    messages.success(request, 'Usuário cadastrado com sucesso!')
    return redirect('/gerir-time')

@login_required(login_url='/')
def Ajax_load_usuario(request):
    userId = request.GET['userid']
    usuarios = User.objects.all()
    unidades = Escolas.objects.all()
    departamentos = Departamentos.objects.all()
    permission = Permissoes.objects.filter(usuario_id=userId).first()

    return render(request, 'ajax/ajax_load_usuario.html',{'permission':permission,'usuarios':usuarios,'unidades':unidades,'departamentos':departamentos})

@login_required(login_url='/')
def Edita_usuario(request):
    with transaction.atomic():
        idUser = request.POST['usuario_id']

        nome = request.POST['nome_completo']
        usuario = request.POST['usuario']
        departamento = request.POST['departamento']
        unidade_user = request.POST['unidade_user']
        try:
            senha = request.POST['senha']
        except:
            pass
        
        email = request.POST['email']

        user = User.objects.get(id=idUser)
        user.first_name = nome
        user.username = usuario
        if senha:
            user.set_password(senha)
        
        user.email = email
        user.save()

        permission = Permissoes.objects.get(usuario_id=idUser)
        permission.unidade_id = unidade_user
        permission.departamento_id = departamento
        permission.save()

        messages.success(request, 'Usuário alterado com sucesso!')
        return redirect('/gerir-time')