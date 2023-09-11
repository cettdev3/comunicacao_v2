from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from solicitacoes.models import Escolas
from .models import Permissoes
# Create your views here.
# Create your views here.
@login_required(login_url='/')
def Gerir_time(request):
    #users = User.objects.select_related('user_id').values('id', 'email','first_name', 'username', 'usuarios__unidade__nome').values('id','email', 'first_name', 'username', 'usuarios__unidade__nome')
    usuarios = User.objects.all()
    unidades = Escolas.objects.all()
    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first
    return render(request, 'gerir_time.html',{'usuarios':usuarios,'unidades':unidades,'permissoes':permissoes})

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