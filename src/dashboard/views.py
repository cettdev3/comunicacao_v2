from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import date,datetime
import datetime
from django.core import serializers
from django.http import JsonResponse
import json as j
from django.contrib.auth.models import User
from django.db import transaction
from solicitacoes.models import Solicitacoes
from solicitacoes.serializers import Solicitacao_Serializar
from gerir_time.models import Permissoes

# Create your views here.
@login_required(login_url='/')
def Dashboard(request):
    permissoes = Permissoes.objects.filter(id=request.user.id).first()
    
    solicitacoes = Solicitacoes.objects.all()
    solicitacoes = Solicitacao_Serializar(solicitacoes,many=True).data
    for solicitacao in solicitacoes:
        solicitacao['data_solicitacao'] = datetime.datetime.strptime(solicitacao['data_solicitacao'], '%Y-%m-%d').date()
        
    return render(request,'dashboard.html',{'solicitacoes':solicitacoes,'permissoes':permissoes})