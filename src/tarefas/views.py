from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Tarefas
from gerir_time.models import Permissoes
# Create your views here.
@login_required(login_url='/')

def Tasks(request):
    tarefas = Tarefas.objects.all().order_by('prazo_entrega')
    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first
    return render(request, 'tarefas.html',{'tarefas':tarefas,'permissoes':permissoes})