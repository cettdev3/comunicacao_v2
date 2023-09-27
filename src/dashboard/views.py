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
import json
from django.db.models import Q

def convert_data_formatada(data):

    data = data.split('/')
    data = data[2]+'-'+data[1]+'-'+data[0]
    return data

# Create your views here.
@login_required(login_url='/')
def Dashboard(request):
    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first()
    departamento = permissoes.departamento_id
    if departamento == 1:
        solicitacao = Solicitacoes.objects.all().order_by('prazo_entrega')
        solicitacoes = Solicitacao_Serializar(solicitacao,many=True).data
        usuarios = User.objects.all()

    elif '9' in permissoes.permissao:
        departamento_id_do_usuario = Permissoes.objects.filter(usuario_id=request.user.id).first()

        solicitações_visíveis = Solicitacoes.objects.filter(criado_por__permissoes__departamento_id=departamento_id_do_usuario.departamento_id).distinct()
        solicitacoes = Solicitacao_Serializar(solicitações_visíveis,many=True).data
        usuarios = User.objects.filter(permissoes__departamento_id = departamento).all()
        ev_eventos = Solicitacoes.objects.filter(criado_por__permissoes__departamento_id=departamento_id_do_usuario.departamento_id).distinct()
    else:
        solicitacao = Solicitacoes.objects.filter(criado_por_id=request.user.id)
        solicitacoes = Solicitacao_Serializar(solicitações_visíveis,many=True).data
        usuarios = User.objects.filter(id=request.user.id).all()

    for solicitacao in solicitacoes:
        solicitacao['data_solicitacao'] = datetime.datetime.strptime(solicitacao['data_solicitacao'], '%Y-%m-%d').date()
        try:
            solicitacao['prazo_entrega'] = datetime.datetime.strptime(solicitacao['prazo_entrega'], '%Y-%m-%d').date()
        except:
             solicitacao['prazo_entrega'] = ''
        
    return render(request,'dashboard.html',{'solicitacoes':solicitacoes,'permissoes':permissoes, 'usuarios':usuarios})

@login_required(login_url='/')
def Filter(request):
 
    projeto = request.GET.get('projeto','')
    data_solicitacao = request.GET.get('data_solicitacao','')
    evento = request.GET.get('evento','').strip()
    prazo_entrega = request.GET.get('prazo_entrega','')
    solicitante = request.GET.get('solicitante','')
    solicitacao = Solicitacoes.objects.all()

    # # Aplique filtros condicionais com base nos parâmetros presentes na solicitação
    if projeto:
        solicitacao = solicitacao.filter(tipo_projeto=projeto)

    if data_solicitacao:
        solicitacao = solicitacao.filter(data_solicitacao=data_solicitacao)

    if prazo_entrega:
        solicitacao = solicitacao.filter(prazo_entrega=prazo_entrega)

    if evento:
        try:
            evento_id = int(evento)
            solicitacao = solicitacao.filter(evento_json__id=evento_id)
        except:
            titulo_evento = evento
            solicitacao = solicitacao.filter(evento_json__titulo_evento=titulo_evento)
       
    if solicitante:
        solicitacao = solicitacao.filter(criado_por_id=solicitante)

    return render(request, 'ajax/tbl_solicitacoes.html', {'solicitacoes': solicitacao})

@login_required(login_url='/')
def Filter_Concluido(request):
  
    projeto = request.GET.get('projeto','')
    data_solicitacao = request.GET.get('data_solicitacao','')
    evento = request.GET.get('evento','').strip()
    data_evento = request.GET.get('data_evento','')
    solicitante = request.GET.get('solicitante','')
    solicitacao = Solicitacoes.objects.all()

    # # Aplique filtros condicionais com base nos parâmetros presentes na solicitação
    if projeto:
        solicitacao = solicitacao.filter(tipo_projeto=projeto)

    if data_solicitacao:
        solicitacao = solicitacao.filter(data_solicitacao=data_solicitacao)

    if evento:
        try:
            evento_id = int(evento)
            solicitacao = solicitacao.filter(evento_json__id=evento_id)
        except:
            titulo_evento = evento
            solicitacao = solicitacao.filter(evento_json__titulo_evento=titulo_evento)
       
    if solicitante:
        solicitacao = solicitacao.filter(criado_por_id=solicitante)

    return render(request, 'ajax/tbl_solicitacao_finalizada.html', {'solicitacoes': solicitacao})