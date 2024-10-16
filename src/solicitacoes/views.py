from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from datetime import date,datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import os
from django.utils.html import linebreaks
from datetime import datetime
from .utils import get_token_api_eventos,get_all_eventos,get_evento
import datetime
from .models import Entregaveis,Solicitacoes,Programacao_Adicional,Tarefas,Escolas
from .serializers import Solicitacao_Serializar,Tarefas_Serializar,Entregaveis_Serializar
from django.contrib.auth.models import User
from gerir_time.models import Permissoes
from .templates_notify import *
import ast
from django.core.files.storage import default_storage
from django.conf import settings

def convert_data_formatada(data):

    data = data.split('-')
    data = data[2]+'/'+data[1]+'/'+data[0]
    return data

@login_required(login_url='/')
def Permissoes_usuario(request):
    permissoes = []
    usuario = request.POST['usuarioPerm']
    for dados in request.POST:
        if 'checkbox' in dados:
            perm = request.POST[dados]
            permissoes.append(perm)
    
    permissoes = ','.join(permissoes)
    user  = Permissoes.objects.get(usuario_id=usuario)
    user.permissao = permissoes
    user.save()
    messages.success(request, 'Permissões de usuários alterada(s) com sucesso!')
    return redirect('/gerir-time')

@login_required(login_url='/')
def Form_Solicitacoes(request):
    try:
        permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first()
        # token = get_token_api_eventos()
        # eventos = get_all_eventos(token)
        eventos = None

        eventos_no_prazo = []
        if eventos:
            for evento in eventos:
                try:
                    evento['data_fim'] = datetime.datetime.strptime(evento['data_fim'], '%Y-%m-%d').date()
                    evento['data_inicio'] = datetime.datetime.strptime(evento['data_inicio'], '%Y-%m-%d').date()
                    if evento['data_fim'] >= datetime.date.today():
                        eventos_no_prazo.append(evento)

                except:
                    pass
    except:eventos_no_prazo = {}


    return render(request, 'solicitacoes.html',{'eventos':eventos_no_prazo,'permissoes':permissoes})

@login_required(login_url='/')
def Visualizar_Solicitacao(request,codigo):
    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first()

    solicitacao = Solicitacoes.objects.filter(id=codigo).first()
    evento_json = solicitacao.evento_json
    try:
        arquivos = solicitacao.arquivos
        arquivos_list = ast.literal_eval(arquivos)
    except:
        arquivos_list = []

    escola = Escolas.objects.filter(id=evento_json['escola']).first()
    if solicitacao.criado_por_id == request.user.id or permissoes.departamento_id == 1 or '9' in permissoes.permissao:
        solicitacao = Solicitacao_Serializar(solicitacao).data
        solicitacao['data_solicitacao'] = datetime.datetime.strptime(solicitacao['data_solicitacao'], '%Y-%m-%d').date()
        try:
            solicitacao['prazo_entrega'] = datetime.datetime.strptime(solicitacao['prazo_entrega'], '%Y-%m-%d').date()
        except:
                solicitacao['prazo_entrega'] = ''
        
        programacao_adicional = Programacao_Adicional.objects.filter(solicitacao_id=codigo).all()


        entregaveis = Entregaveis.objects.filter(evento_id=codigo).all()
        entregaveis = Entregaveis_Serializar(entregaveis,many=True).data

       

        tarefas_por_entregavel = {}

        for entregavel in entregaveis:
            try:
                arquivos_entregaveis = entregavel['arquivos']
                arquivos_list_entregavel = ast.literal_eval(arquivos_entregaveis)
                entregavel['arquivos'] = arquivos_list_entregavel
                entregavel['prazo'] = datetime.datetime.strptime(entregavel['prazo'], '%Y-%m-%d').date()
                entregavel['data_solicitacao'] = datetime.datetime.strptime(entregavel['data_solicitacao'], '%Y-%m-%d').date()
            
                tarefas_relacionadas = Tarefas.objects.filter(entregavel_id=entregavel['id']).all().order_by('-id')
                
            except:
                tarefas_relacionadas = {}
                arquivos_list_entregavel = []
            try:
                ultima_tarefa_id = Tarefas.objects.filter(entregavel_id=entregavel['id']).latest('id')
            except:
                ultima_tarefa_id = None
            entregavel['tarefas_relacionadas'] = tarefas_relacionadas
            entregavel['ultima_tarefa_id'] = ultima_tarefa_id

        usuarios = User.objects.all().order_by('first_name')
        context = {'solicitacao':solicitacao,'entregaveis':entregaveis,'programacao_adicional':programacao_adicional,'usuarios':usuarios,'tarefas_por_entregavel': tarefas_por_entregavel,'permissoes':permissoes,'escola':escola,'arquivos':arquivos_list}
        return render(request,'visualizar_solicitacao.html',context)
    else:
        messages.error(request, 'Você não tem permissões para acessar!')
        return redirect('/solicitacoes')

@login_required(login_url='/')
def Dados_Gerais_Evento(request):

    idEvento = request.GET['idEvento']
    if idEvento != "und":
        token = get_token_api_eventos()
        evento = get_evento(token,idEvento)
        evento['data_fim'] = datetime.datetime.strptime(evento['data_fim'], '%Y-%m-%d').date()
        evento['data_inicio'] = datetime.datetime.strptime(evento['data_inicio'], '%Y-%m-%d').date()
        context = {'evento':evento}
    else:
        escolas = Escolas.objects.all()
        return render(request,'ajax/ajax_designar_und.html',{'escolas':escolas})

    return render(request,'ajax/ajax_dados_gerais_evento.html',context)

@login_required(login_url='/')
def Ajax_Realiza_Solicitacao(request):
    dadosForm = request.POST


    with transaction.atomic():

            #OBTÉM DADOS DA SOLICITAÇÃO
            idEvento = request.POST.get('eventos_gerais',None)
            publicoEvento = request.POST.get('publico_evento',None)
            save_the_date = request.POST.get('save_the_date',None)
            programacao_evento = request.POST.get('programacao_evento',None)
            divulgacao_check = request.POST.get('divulgacao_check',None)
            programacao_check = request.POST.get('programacao_check',None)
            stand_check = request.POST.get('stand_check',None)
            prazo_entrega = request.POST.get('prazo_entrega',None)
            briefing = request.POST.get('briefing_solicitacao',None)
            userid = request.user.id
            try:
                arquivos_solicitacao = []
                arquivos = request.FILES.getlist('files[]')
                for arquivo in arquivos:
                    fs1 = FileSystemStorage()
                    filename1 = fs1.save(arquivo.name, arquivo)
                    arquivo_url = fs1.url(filename1)
                    arquivos_solicitacao.append(arquivo_url)
            except:
                arquivo_url = []

            if idEvento != 'und':
                tipoUnidade = request.POST.get('tipo_und',None)
                token = get_token_api_eventos()
                json_evento = get_evento(token,idEvento)

            

                #ANTES VERIFICA SE A SOLICITAÇÃO JÁ EXISTE
                solicitacao = Solicitacoes.objects.filter(evento_json__id = idEvento,criado_por_id = request.user.id).first()
                if solicitacao:
                    print(solicitacao.id)
                else:
                    #CRIA A SOLICITACAO
                    solicitacao = Solicitacoes.objects.create(
                        tipo_projeto = tipoUnidade, 
                        publico_evento = publicoEvento,
                        criado_por_id = userid,
                        evento_json = json_evento,
                        prazo_entrega = prazo_entrega,
                        briefing = briefing,
                        arquivos = arquivos_solicitacao
                        
                    )
        
                

            else:
                tipoUnidade = request.POST.get('tipo_und',None)
                escola = request.POST.get('escola',None)
                endereco_escola = request.POST.get('endereco_escola',None)
                data_inicio = request.POST.get('data_inicial',None)
                data_fim = request.POST.get('data_final',None)
                
                if data_inicio:
                    data_inicio = convert_data_formatada(data_inicio)
                if data_fim:
                    data_fim = convert_data_formatada(data_fim)

                
                titulo_evento = request.POST.get('titulo_evento',None)
                json_evento = {
                        "escola":escola,
                        "endereco":endereco_escola,
                        "data_inicio":data_inicio,
                        "data_fim":data_fim,
                        "titulo_evento":titulo_evento,

                }
                #CRIA A SOLICITACAO
                solicitacao = Solicitacoes.objects.create(
                    tipo_projeto = tipoUnidade, 
                    publico_evento = publicoEvento,
                    criado_por_id = userid,
                    evento_json = json_evento,
                    prazo_entrega = prazo_entrega,
                    briefing = briefing,
                    arquivos = arquivos_solicitacao
                )




            
 


            #VERIFICA PROGRAMAÇÃO
            if programacao_evento:
                indice = 0
                for dados in dadosForm:
                    try:
                        if 'data_programacao' in dados:
                            if indice == 0:
                                data_programacao = request.POST['data_programacao']
                                hora_programacao = request.POST['hora_programacao']
                                hora_programacao_final = request.POST['hora_programacao_final']
                                atividade_programacao = request.POST['atividade_programacao']
                                solicitacao_id = solicitacao.id
                                programacao_adicional = Programacao_Adicional.objects.create(
                                    data=data_programacao, hora=hora_programacao,hora_final = hora_programacao_final, atividade=atividade_programacao, solicitacao_id=solicitacao_id)
                                indice += 2

                            if indice > 0:
                                data_programacao = request.POST['data_programacao'+str(
                                    indice)]
                                hora_programacao = request.POST['hora_programacao'+str(
                                    indice)]
                                hora_programacao_final = request.POST['hora_programacao_final'+str(
                                    indice)]
                                atividade_programacao = request.POST['atividade_programacao'+str(
                                    indice)]
                                solicitacao_id = solicitacao.id
                                programacao_adicional = Programacao_Adicional.objects.create(
                                    data=data_programacao, hora=hora_programacao,hora_final = hora_programacao_final, atividade=atividade_programacao, solicitacao_id=solicitacao_id)
                                
                                indice += 1
                    except:
                        pass

            #VERIFICA ENTREGAVEIS
            indice = 0
            if save_the_date:
                for dado in dadosForm:
                    if 'pecas_save_the_date' in dado:
                        if dado == 'pecas_save_the_date':
                            prazo_save_the_date = prazo_entrega
                            exemploarte_save_the_date = request.FILES.get('exemploarte_save_the_date',None)
                            tipoproduto_save_the_date = request.POST.get('tipoproduto_save_the_date',None)
                            categoriaproduto_save_the_date = request.POST.get('categoriaproduto_save_the_date',None)
                            descricao_save_the_date = request.POST.get('descricao_save_the_date',None)
                            #obs_save_the_date = request.POST.get('obs_save_the_date',None)
                            outros_entregavel = request.POST.get('outros_field_save_the_date','')

                         

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_save_the_date:
                                fss = FileSystemStorage()
                                exemploarte_save_the_date_file = fss.save(exemploarte_save_the_date.name, exemploarte_save_the_date)
                                exemploarte_save_the_date_url = fss.url(exemploarte_save_the_date_file)
                            else:
                                exemploarte_save_the_date_url = ''

                            #PEGO OS ARQUIVOS DO ENTREGÁVEL PRINCIPAL
                            try:
                                arquivos_entregaveis_save_the_date = []
                                arquivos_save_the_date = request.FILES.getlist('file_save_the_date')
                                for arquivo in arquivos_save_the_date:
                                    fs1 = FileSystemStorage()
                                    filename1 = fs1.save(arquivo.name, arquivo)
                                    arquivo_url = fs1.url(filename1)
                                    arquivos_entregaveis_save_the_date.append(arquivo_url)
                            except:
                                arquivos_entregaveis_save_the_date = []
                                arquivos_entregaveis_save_the_date = []

                          
                            
                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = solicitacao.id,
                                prazo = prazo_save_the_date,
                                exemplo_arte = exemploarte_save_the_date_url,
                                tipo_entregavel = 1,
                                tipo_produto = tipoproduto_save_the_date,
                                categoria_produto = categoriaproduto_save_the_date,
                                descricao_audio_visual = descricao_save_the_date,
                                #observacao = obs_save_the_date,
                                criado_por_id = userid,
                                arquivos = arquivos_entregaveis_save_the_date,
                                outros = outros_entregavel
                                )
     
                            
                        else:
                            index = dado[-1]
                            prazo_save_the_date = prazo_entrega
                            exemploarte_save_the_date = request.FILES.get('exemploarte_save_the_date'+str(index),None)
                            tipoproduto_save_the_date = request.POST.get('tipoproduto_save_the_date'+str(index),None)
                            categoriaproduto_save_the_date = request.POST.get('categoriaproduto_save_the_date'+str(index),'')
                            descricao_save_the_date = request.POST.get('descricao_save_the_date'+str(index),None)
                            #obs_save_the_date = request.POST.get('obs_save_the_date'+str(index),None)
                            outros_entregavel = request.POST.get('outros_field_save_the_date'+str(index),'')

                          
                            #PEGO OS ARQUIVOS DO ENTREGÁVEIS DINAMICOS
                            try:
                                arquivos_entregaveis_save_the_date = []
                                arquivos_save_the_date = request.FILES.getlist('file_save_the_date'+str(index))
                                for arquivo in arquivos_save_the_date:
                                    fs1 = FileSystemStorage()
                                    filename1 = fs1.save(arquivo.name, arquivo)
                                    arquivo_url = fs1.url(filename1)
                                    arquivos_entregaveis_save_the_date.append(arquivo_url)
                            except:
                                arquivos_entregaveis_save_the_date = []

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_save_the_date:
                                fss = FileSystemStorage()
                                exemploarte_save_the_date_file = fss.save(exemploarte_save_the_date.name, exemploarte_save_the_date)
                                exemploarte_save_the_date_url = fss.url(exemploarte_save_the_date_file)
                            else:
                                exemploarte_save_the_date_url = ''


                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = solicitacao.id,
                                prazo = prazo_save_the_date,
                                exemplo_arte = exemploarte_save_the_date_url,
                                tipo_entregavel = 1,
                                tipo_produto = tipoproduto_save_the_date,
                                categoria_produto = categoriaproduto_save_the_date,
                                descricao_audio_visual = descricao_save_the_date,
                                #observacao = obs_save_the_date,
                                criado_por_id = userid,
                                arquivos = arquivos_entregaveis_save_the_date,
                                outros = outros_entregavel
                                )
                            

            #VERIFICA DIVULGAÇÃO
            indice = 0
            if divulgacao_check:
                for dado in dadosForm:
                    if 'pecas_divulgacao' in dado:
                        if dado == 'pecas_divulgacao':
                            prazo_divulgacao = prazo_entrega
                            exemploarte_divulgacao = request.FILES.get('exemploarte_divulgacao',None)
                            tipoproduto_divulgacao = request.POST.get('tipoproduto_divulgacao',None)
                            categoriaproduto_divulgacao = request.POST.get('categoriaproduto_divulgacao',None)
                            descricao_divulgacao = request.POST.get('descricao_divulgacao',None)
                            #obs_divulgacao = request.POST.get('obs_divulgacao',None)
                            outros_entregavel = request.POST.get('outros_divulgacao','')

                            #PEGO OS ARQUIVOS DO ENTREGÁVEIS DINAMICOS
                            try:
                                arquivos_entregaveis_divulgacao = []
                                arquivos_divulgacao = request.FILES.getlist('file_divulgacao')
                                for arquivo in arquivos_divulgacao:
                                    fs1 = FileSystemStorage()
                                    filename1 = fs1.save(arquivo.name, arquivo)
                                    arquivo_url = fs1.url(filename1)
                                    arquivos_entregaveis_divulgacao.append(arquivo_url)
                            except:
                                arquivos_entregaveis_divulgacao = []

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_divulgacao:
                                fss = FileSystemStorage()
                                exemploarte_divulgacao_file = fss.save(exemploarte_divulgacao.name, exemploarte_divulgacao)
                                exemploarte_divulgacao_url = fss.url(exemploarte_divulgacao_file)
                            else:
                                exemploarte_divulgacao_url = ''

                            #PEGO OS ARQUIVOS DO ENTREGÁVEL PRINCIPAL
                            try:
                                arquivos_entregaveis_divulgacao = []
                                arquivos_divulgacao = request.FILES.getlist('file_divulgacao')
                                for arquivo in arquivos_divulgacao:
                                    fs1 = FileSystemStorage()
                                    filename1 = fs1.save(arquivo.name, arquivo)
                                    arquivo_url = fs1.url(filename1)
                                    arquivos_entregaveis_divulgacao.append(arquivo_url)
                            except:
                                arquivos_entregaveis_divulgacao = []
                            
                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = solicitacao.id,
                                prazo = prazo_divulgacao,
                                exemplo_arte = exemploarte_divulgacao_url,
                                tipo_entregavel = 2,
                                tipo_produto = tipoproduto_divulgacao,
                                categoria_produto = categoriaproduto_divulgacao,
                                descricao_audio_visual = descricao_divulgacao,
                                #observacao = obs_divulgacao,
                                arquivos = arquivos_entregaveis_divulgacao,
                                outros = outros_entregavel,
                                criado_por_id = userid,
    
                                )
             
                        else:
                            index = dado[-1]
                            exemploarte_divulgacao = request.FILES.get('exemploarte_divulgacao'+str(index),None)
                            tipoproduto_divulgacao = request.POST.get('tipoproduto_divulgacao'+str(index),None)
                            categoriaproduto_divulgacao = request.POST.get('categoriaproduto_divulgacao'+str(index),None)
                            descricao_divulgacao = request.POST.get('descricao_divulgacao'+str(index),None)
                            #obs_divulgacao = request.POST.get('obs_divulgacao'+str(index),None)
                            outros_entregavel = request.POST.get('outros_divulgacao'+str(index),'')
                            prazo_divulgacao = prazo_entrega
     
                            #PEGO OS ARQUIVOS DO ENTREGÁVEIS DINAMICOS
                            try:
                                arquivos_entregaveis_divulgacao = []
                                arquivos_divulgacao = request.FILES.getlist('file_divulgacao'+str(index))
                                for arquivo in arquivos_divulgacao:
                                    fs1 = FileSystemStorage()
                                    filename1 = fs1.save(arquivo.name, arquivo)
                                    arquivo_url = fs1.url(filename1)
                                    arquivos_entregaveis_divulgacao.append(arquivo_url)
                            except:
                                arquivos_entregaveis_divulgacao = []

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_divulgacao:
                                fss = FileSystemStorage()
                                exemploarte_divulgacao_file = fss.save(exemploarte_divulgacao.name, exemploarte_divulgacao)
                                exemploarte_divulgacao_url = fss.url(exemploarte_divulgacao_file)
                            else:
                                exemploarte_divulgacao_url = ''

                            try:
                                arquivos_entregaveis_divulgacao = []
                                arquivos_divulgacao = request.FILES.getlist('file_divulgacao'+str(index))
                                for arquivo in arquivos_divulgacao:
                                    fs1 = FileSystemStorage()
                                    filename1 = fs1.save(arquivo.name, arquivo)
                                    arquivo_url = fs1.url(filename1)
                                    arquivos_entregaveis_divulgacao.append(arquivo_url)
                            except:
                                arquivos_entregaveis_divulgacao = []

                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = solicitacao.id,
                                prazo = prazo_divulgacao,
                                exemplo_arte = exemploarte_divulgacao_url,
                                tipo_entregavel = 2,
                                tipo_produto = tipoproduto_divulgacao,
                                categoria_produto = categoriaproduto_divulgacao,
                                descricao_audio_visual = descricao_divulgacao,
                                #observacao = obs_divulgacao,
                                criado_por_id = userid,
                                arquivos = arquivos_entregaveis_divulgacao,
                                outros = outros_entregavel
                                )

           
            #VERIFICA PROGRAMAÇÃO
            indice = 0
            if programacao_check:
                for dado in dadosForm:
                    if 'pecas_programacao' in dado:
                        if dado == 'pecas_programacao':
                            prazo_programacao = prazo_entrega
                            exemploarte_programacao = request.FILES.get('exemploarte_programacao',None)
                            tipoproduto_programacao = request.POST.get('tipoproduto_programacao',None)
                            categoriaproduto_programacao = request.POST.get('categoriaproduto_programacao',None)
                            descricao_programacao = request.POST.get('descricao_programacao',None)
                            #obs_programacao = request.POST.get('obs_programacao',None)
                            outros_entregavel = request.POST.get('outros_programacao','')

                            #PEGO OS ARQUIVOS DO ENTREGÁVEIS DINAMICOS
                            try:
                                arquivos_entregaveis_programacao = []
                                arquivos_programacao = request.FILES.getlist('file_programacao')
                                for arquivo in arquivos_programacao:
                                    fs1 = FileSystemStorage()
                                    filename1 = fs1.save(arquivo.name, arquivo)
                                    arquivo_url = fs1.url(filename1)
                                    arquivos_entregaveis_programacao.append(arquivo_url)
                            except:
                                arquivos_entregaveis_programacao = []

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_programacao:
                                fss = FileSystemStorage()
                                exemploarte_programacao_file = fss.save(exemploarte_programacao.name, exemploarte_programacao)
                                exemploarte_programacao_url = fss.url(exemploarte_programacao_file)
                            else:
                                exemploarte_programacao_url = ''

                            #PEGO OS ARQUIVOS DO ENTREGÁVEL PRINCIPAL
                            try:
                                arquivos_entregaveis_programacao = []
                                arquivos_programacao = request.FILES.getlist('file_programacao')
                                for arquivo in arquivos_programacao:
                                    fs1 = FileSystemStorage()
                                    filename1 = fs1.save(arquivo.name, arquivo)
                                    arquivo_url = fs1.url(filename1)
                                    arquivos_entregaveis_programacao.append(arquivo_url)
                            except:
                                arquivos_entregaveis_programacao = []
                            
                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = solicitacao.id,
                                prazo = prazo_programacao,
                                exemplo_arte = exemploarte_programacao_url,
                                tipo_entregavel = 3,
                                tipo_produto = tipoproduto_programacao,
                                categoria_produto = categoriaproduto_programacao,
                                descricao_audio_visual = descricao_programacao,
                                #observacao = obs_programacao,
                                arquivos = arquivos_entregaveis_programacao,
                                criado_por_id = userid,
                                outros = outros_entregavel
                                )
               
                        else:
                            index = dado[-1]
                            prazo_programacao = prazo_entrega
                            exemploarte_programacao = request.FILES.get('exemploarte_programacao'+str(index),None)
                            tipoproduto_programacao = request.POST.get('tipoproduto_programacao'+str(index),None)
                            categoriaproduto_programacao = request.POST.get('categoriaproduto_programacao'+str(index),None)
                            descricao_programacao = request.POST.get('descricao_programacao'+str(index),None)
                            obs_programacao = request.POST.get('obs_programacao'+str(index),None)
                            outros_entregavel = request.POST.get('outros_programacao'+str(index),'')

                            #PEGO OS ARQUIVOS DO ENTREGÁVEIS DINAMICOS
                            try:
                                arquivos_entregaveis_programacao = []
                                arquivos_programacao = request.FILES.getlist('file_programacao'+str(index))
                                for arquivo in arquivos_programacao:
                                    fs1 = FileSystemStorage()
                                    filename1 = fs1.save(arquivo.name, arquivo)
                                    arquivo_url = fs1.url(filename1)
                                    arquivos_entregaveis_programacao.append(arquivo_url)
                            except:
                                arquivos_entregaveis_programacao = []

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_programacao:
                                fss = FileSystemStorage()
                                exemploarte_programacao_file = fss.save(exemploarte_programacao.name, exemploarte_programacao)
                                exemploarte_programacao_url = fss.url(exemploarte_programacao_file)
                            else:
                                exemploarte_programacao_url = ''

                            try:
                                arquivos_entregaveis_programacao = []
                                arquivos_programacao = request.FILES.getlist('file_programacao'+str(index))
                                for arquivo in arquivos_programacao:
                                    fs1 = FileSystemStorage()
                                    filename1 = fs1.save(arquivo.name, arquivo)
                                    arquivo_url = fs1.url(filename1)
                                    arquivos_entregaveis_programacao.append(arquivo_url)
                            except:
                                arquivos_entregaveis_programacao = []
                            
                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = solicitacao.id,
                                prazo = prazo_programacao,
                                exemplo_arte = exemploarte_programacao_url,
                                tipo_entregavel = 3,
                                tipo_produto = tipoproduto_programacao,
                                categoria_produto = categoriaproduto_programacao,
                                descricao_audio_visual = descricao_programacao,
                                #observacao = obs_programacao,
                                criado_por_id = userid,
                                outros = outros_entregavel,
                                arquivos = arquivos_entregaveis_programacao
                                )

            
            #VERIFICA STAND
            indice = 0
            if stand_check:
                for dado in dadosForm:
                    if 'pecas_stand' in dado:
                        if dado == 'pecas_stand':
                            prazo_stand = prazo_entrega
                            exemploarte_stand = request.FILES.get('exemploarte_stand',None)
                            tipoproduto_stand = request.POST.get('tipoproduto_stand',None)
                            categoriaproduto_stand = request.POST.get('categoriaproduto_stand',None)
                            descricao_stand = request.POST.get('descricao_stand',None)
                            #obs_stand = request.POST.get('obs_stand',None)
                            outros_entregavel = request.POST.get('outros_stand','')
                            userid = request.user.id

                            #PEGO OS ARQUIVOS DO ENTREGÁVEIS DINAMICOS
                            try:
                                arquivos_entregaveis_stand = []
                                arquivos_stand = request.FILES.getlist('file_programacao')
                                for arquivo in arquivos_stand:
                                    fs1 = FileSystemStorage()
                                    filename1 = fs1.save(arquivo.name, arquivo)
                                    arquivo_url = fs1.url(filename1)
                                    arquivos_entregaveis_stand.append(arquivo_url)
                            except:
                                arquivos_entregaveis_stand = []
                          

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_stand:
                                fss = FileSystemStorage()
                                exemploarte_stand_file = fss.save(exemploarte_stand.name, exemploarte_stand)
                                exemploarte_stand_url = fss.url(exemploarte_stand_file)
                            else:
                                exemploarte_stand_url = ''

                            #PEGO OS ARQUIVOS DO ENTREGÁVEL PRINCIPAL
                            try:
                                arquivos_entregaveis_stand = []
                                arquivos_stand = request.FILES.getlist('file_stand')
                                for arquivo in arquivos_stand:
                                    fs1 = FileSystemStorage()
                                    filename1 = fs1.save(arquivo.name, arquivo)
                                    arquivo_url = fs1.url(filename1)
                                    arquivos_entregaveis_stand.append(arquivo_url)
                            except:
                                arquivos_entregaveis_stand = []

                            
                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = solicitacao.id,
                                prazo = prazo_stand,
                                exemplo_arte = exemploarte_stand_url,
                                tipo_entregavel = 4,
                                tipo_produto = tipoproduto_stand,
                                categoria_produto = categoriaproduto_stand,
                                descricao_audio_visual = descricao_stand,
                                #observacao = obs_stand,
                                criado_por_id = userid,
                                arquivos = arquivos_entregaveis_stand,
                                outros = outros_entregavel
                                )
                            
                   
                        else:
                            index = dado[-1]
                            prazo_stand = prazo_entrega
                            exemploarte_stand = request.FILES.get('exemploarte_stand'+str(index),None)
                            tipoproduto_stand = request.POST.get('tipoproduto_stand'+str(index),None)
                            categoriaproduto_stand = request.POST.get('categoriaproduto_stand'+str(index),None)
                            descricao_stand = request.POST.get('descricao_stand'+str(index),None)
                            #obs_stand = request.POST.get('obs_stand'+str(index),None)
                            outros_entregavel = request.POST.get('outros_stand'+str(index),'')

                            #PEGO OS ARQUIVOS DO ENTREGÁVEIS DINAMICOS
                            try:
                                arquivos_entregaveis_stand = []
                                arquivos_stand = request.FILES.getlist('file_programacao'+str(index))
                                for arquivo in arquivos_stand:
                                    fs1 = FileSystemStorage()
                                    filename1 = fs1.save(arquivo.name, arquivo)
                                    arquivo_url = fs1.url(filename1)
                                    arquivos_entregaveis_stand.append(arquivo_url)
                            except:
                                arquivos_entregaveis_stand = []
                         

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_stand:
                                fss = FileSystemStorage()
                                exemploarte_stand_file = fss.save(exemploarte_stand.name, exemploarte_stand)
                                exemploarte_stand_url = fss.url(exemploarte_stand_file)
                            else:
                                exemploarte_stand_url = ''

                            try:
                                arquivos_entregaveis_stand = []
                                arquivos_stand = request.FILES.getlist('file_stand'+str(index))
                                for arquivo in arquivos_stand:
                                    fs1 = FileSystemStorage()
                                    filename1 = fs1.save(arquivo.name, arquivo)
                                    arquivo_url = fs1.url(filename1)
                                    arquivos_entregaveis_stand.append(arquivo_url)
                            except:
                                arquivos_entregaveis_stand = []

                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = solicitacao.id,
                                prazo = prazo_stand,
                                exemplo_arte = exemploarte_stand_url,
                                tipo_entregavel = 3,
                                tipo_produto = tipoproduto_stand,
                                categoria_produto = categoriaproduto_stand,
                                descricao_audio_visual = descricao_stand,
                                #observacao = obs_stand,
                                criado_por_id = userid,
                                arquivos = arquivos_entregaveis_stand,
                                outros = outros_entregavel
                                )
                            
                    
            nova_notificacao(request,solicitacao.id)
            return JsonResponse({"success_message": "Solicitação Realizada!"}) 

@login_required(login_url='/')
def Ajax_Cria_Tarefa(request):
   
    try:
        tituloTarefa = request.POST.get('titulo',None)
        designar_usuario = request.POST.get('usuario',None)
        prioridade = request.POST.get('prioridade',None)
        prazo_entrega = request.POST.get('prazo_entrega',None)
        descricao_tarefa = request.POST.get('descricao_tarefa',None)
        entregavel_id = request.POST.get('idEntregavel',None)

        tarefas = Tarefas.objects.create(
            titulo_tarefa = tituloTarefa,
            descricao_tarefa = descricao_tarefa,
            status = 0,
            usuario_id = designar_usuario,
            usuario_designou_id = request.user.id,
            entregavel_id = entregavel_id,
            prazo_entrega = prazo_entrega,
            prioridade = prioridade,
    )
        tarefas_all = Tarefas.objects.filter(entregavel_id = entregavel_id ).all()
        solicitacao_id = Entregaveis.objects.filter(id=entregavel_id).first()

        nova_tarefa(request,solicitacao_id.evento_id,designar_usuario,tarefas.id,entregavel_id)

        return render(request,'ajax/ajax_load_tbl_tarefas.html',{'tarefas':tarefas_all})
    except Exception as e:
        return JsonResponse({"error_message": "Não foi possível realizar a solicitação: " + str(e)}, status=400)

@login_required(login_url='/')
def Ajax_Realiza_Entrega(request):
   
    try:
        idEntregavel = request.POST.get('idEntregavel',None)
        statusEntregavel = request.POST.get('statusEntregavel',None)
        entregavel = Entregaveis.objects.get(id=idEntregavel)
        entregavel.status = statusEntregavel
        entregavel.save()
        if statusEntregavel != '4':
            enviar_solicitante(request,entregavel.evento_id,entregavel.criado_por_id,request.user.id,entregavel.id)
        else:
            confirmar_recebimento(request,entregavel.evento_id)
        return JsonResponse({"success_message": "Entrega Realizada"}) 
    except Exception as e:
        return JsonResponse({"error_message": "Não foi possível realizar a solicitação: " + str(e)}, status=400)   

@login_required(login_url='/')
def Ajax_Revisa_Task(request):

    try:
        idTask = request.POST.get('idTask',None)
        novo_prazo_entrega = request.POST.get('novo_prazo_entrega',None)
        nova_descricao_tarefa = request.POST.get('nova_descricao_tarefa',None)

        #obtem a tarefa atual e informa que ela foi revisionada
        tarefa = Tarefas.objects.get(id=idTask)
        tarefa_revisao = tarefa
        

        tarefas = Tarefas.objects.create(
            titulo_tarefa = tarefa_revisao.titulo_tarefa,
            descricao_tarefa = nova_descricao_tarefa,
            status = 2,
            usuario_id = tarefa_revisao.usuario_id,
            usuario_designou_id = tarefa_revisao.usuario_designou_id,
            entregavel_id = tarefa_revisao.entregavel_id,
            prazo_entrega = novo_prazo_entrega,
            prioridade = tarefa_revisao.prioridade,
    )
        
        tarefa.tipo = tarefas.id
        tarefa.save()

        entregavel = Entregaveis.objects.filter(id= tarefa_revisao.entregavel_id).first()
        solicitacao = Solicitacoes.objects.filter(id = entregavel.evento_id).first()

        tarefa_em_revisao(request,solicitacao.id,tarefa_revisao.usuario_id,tarefas.id,tarefa_revisao.entregavel_id)
        return JsonResponse({"success_message": "Tarefa em revisão!"}) 
    except Exception as e:
        return JsonResponse({"error_message": "Não foi possível realizar a solicitação: " + str(e)}, status=400)
    
@login_required(login_url='/')
def Ajax_Devolve_Entregavel(request):

    try:
        idEntregavel = request.POST.get('entregavelId',None)
        motivo = request.POST.get('motivo_devolucao',None)

        #obtem o entregável atual e informa que ela foi devolvido
        entregavel = Entregaveis.objects.get(id=idEntregavel)
        entregavel.status = 3
        entregavel.motivo_revisao = motivo
        entregavel.save()

        devolver_correcao_entrega(request,entregavel.evento_id,request.user.id,entregavel.id)
        return JsonResponse({"success_message": "Tarefa em revisão!"}) 
    except Exception as e:
        return JsonResponse({"error_message": "Não foi possível realizar a solicitação: " + str(e)}, status=400)

@login_required(login_url='/')
def Ajax_Endereco_Escola(request):
    idEscola = request.GET['idEscola']
    if idEscola:
        escola = Escolas.objects.filter(id=idEscola).first()
        escola_info = Escolas.objects.filter(id=idEscola).values()
        escola_info = escola_info[0]
        endereco_montado = ''

        if escola_info['logradouro']:
            endereco_montado = endereco_montado + escola_info['logradouro'] + ' - '
        if escola_info['bairro']:
            endereco_montado  = endereco_montado + escola_info['bairro'] + ' - '
        if escola_info['complemento']:
            endereco_montado  = endereco_montado + escola_info['complemento'] + ' - '
        if escola_info['cep']:
            endereco_montado  = endereco_montado + escola_info['cep'] + ' - '
        if escola_info['cidade']:
            endereco_montado  = endereco_montado + escola_info['cidade']

        return render(request,'ajax/ajax_load_endereco.html',{'escola':escola,'endereco':endereco_montado})

@login_required(login_url='/')
def Ajax_Negar_Entregavel(request):
    try:
        entregavelId = request.POST['idEntregavel']
        descricao_negativa = request.POST['negativa_descricao']
        tipo = request.POST['tipo']

        if tipo == '1':
            entregavel = Entregaveis.objects.get(id=entregavelId)
            entregavel.status = 6
            entregavel.motivo_revisao = descricao_negativa
            entregavel.save()
            negar_entregavel_solicitante(request,entregavel.criado_por_id,request.user.id,entregavel.evento_id,entregavel.id)
            return JsonResponse({"success_message": "Tarefa Negada!"})
        elif tipo == '2':
            entregavel = Entregaveis.objects.get(id=entregavelId)
            entregavel.status = 5
            entregavel.motivo_revisao = descricao_negativa
            entregavel.save()
            devolver_entregavel_comunicacao(request,entregavel.criado_por_id,request.user.id,entregavel.evento_id, entregavel.id)
            return JsonResponse({"success_message": "Tarefa Devolvida!"})

    except Exception as e:
        return JsonResponse({"error_message": "Não foi possível realizar a solicitação: " + str(e)}, status=400)

@login_required(login_url='/')
def Ajax_Altera_Entregavel(request):
    entregavelID = request.GET['entregavelId']
    entregavel = Entregaveis.objects.filter(id=entregavelID).first()
    arquivos_entregaveis = entregavel.arquivos if entregavel.arquivos else '[]'
    arquivos_list_entregavel = ast.literal_eval(arquivos_entregaveis)
    entregavel.arquivos = arquivos_list_entregavel
    return render(request, 'ajax/ajax_editar_entregaveis.html', {'entregavel': entregavel})

@login_required(login_url='/')
def Ajax_Alterar_Entregavel(request):
    try:
        with transaction.atomic():
            entregavel_id = request.POST.get('identregavel',None)
            obs_audiovisual = request.POST.get('descricao_audiovisual',None)
            obs = request.POST.get('descricao',None)

            entregavel = Entregaveis.objects.get(id=entregavel_id)
            if obs_audiovisual:
                entregavel.descricao_audio_visual = obs_audiovisual
            if obs:
                entregavel.observacao = obs
            
            entregavel.status = 0

            entregavel.save()
            return JsonResponse({"success_message": "Entregável Alterado!"})

    except Exception as e:
        return JsonResponse({"error_message": "Não foi possível alterar o entregável: " + str(e)}, status=400)

@login_required(login_url='/')
def Ajax_Alterar_Solicitacao(request):
    solicitacaoId = request.GET['solicitacaoId']
    solicitacao = Solicitacoes.objects.filter(id=solicitacaoId).first()
    unidades = Escolas.objects.all()
    usuarios = User.objects.all().order_by('first_name')
    solicitacao.evento_json['data_inicio'] = datetime.datetime.strptime(solicitacao.evento_json['data_inicio'], '%d/%m/%Y').date()
    solicitacao.evento_json['data_fim'] = datetime.datetime.strptime(solicitacao.evento_json['data_fim'], '%d/%m/%Y').date()
    try:
        arquivos = solicitacao.arquivos
        arquivos_list = ast.literal_eval(arquivos)
    except:
        arquivos_list = None
    return render(request, 'ajax/ajax_edit_solicitacao_modal.html', {'solicitacao': solicitacao,'unidades':unidades,'usuarios':usuarios,'arquivos':arquivos_list})

@login_required(login_url='/')
def Ajax_Altera_Solicitacao(request):
    try:
        solicitacaoID = request.POST.get('solicitacaoID',None)
        projeto = request.POST.get('projeto',None)
        titulo_evento = request.POST.get('titulo_evento',None)
        data_inicio = request.POST.get('data_inicio',None)
        data_fim = request.POST.get('data_fim',None)
        publico_evento = request.POST.get('publico_evento',None)
        unidade = request.POST.get('unidade',None)
        endereco = request.POST.get('endereco',None)
        data_inicio_convertida = convert_data_formatada(data_inicio)
        data_fim_convertida = convert_data_formatada(data_fim)
        briefing = request.POST.get('briefing',None)
        prazo_entrega = request.POST.get('prazo_entrega_solicitacao',None)

        evento_json = {"escola": unidade, "endereco": endereco, "data_inicio": data_inicio_convertida, "data_fim": data_fim_convertida, "titulo_evento": titulo_evento}
        solicitacao = Solicitacoes.objects.get(id=solicitacaoID)

  
        solicitacao.evento_json = evento_json
        solicitacao.tipo_projeto = projeto
        solicitacao.publico_evento = publico_evento
        solicitacao.prazo_entrega = prazo_entrega
        solicitacao.criado_por_id = request.POST.get('solicitante',None)
        briefing_antigo = solicitacao.briefing
        if briefing != None:
            if briefing_antigo:
                solicitacao.briefing = briefing + '<hr><b>Briefing Antigo</b>: ' + briefing_antigo
            else:
                solicitacao.briefing = briefing
        
        solicitacao.save()

        Entregaveis.objects.filter(evento_id=solicitacaoID).update(prazo=prazo_entrega)
        return render(request, 'ajax/ajax_load_files.html', {'arquivos': solicitacao.arquivos,'solicitacao':solicitacao})

    except Exception as e:
        return JsonResponse({"error_message": "Não foi possível realizar a solicitação: " + str(e)}, status=400)

@login_required(login_url='/')
def Ajax_Change_Entregavel(request):


    with transaction.atomic():
        entregavelId = request.POST.get('entregavelID','')
        prazo = request.POST.get('prazo_save_the_date','')
        tipo_produto = request.POST.get('tipoproduto_save_the_date','')
        categoria = request.POST.get('categoriaproduto_save_the_date','')
        tipo_entregavel = request.POST.get('tipo_entregavel','')
        audiovisual =  request.POST.get('audio_visual','')
        observacoes =  request.POST.get('obs_save_the_date','')
    
        entregavel = Entregaveis.objects.get(id=entregavelId)
        entregavel.prazo = prazo
        entregavel.tipo_produto = tipo_produto
        entregavel.categoria_produto = categoria
        entregavel.tipo_entregavel = tipo_entregavel
        entregavel.descricao_audio_visual = audiovisual
        entregavel.observacao = observacoes

        #PEGO OS ARQUIVOS DO ENTREGÁVEL PRINCIPAL
        try:
            arquivos_entregaveis = []
            arquivos = request.FILES.getlist('fileInput')
            for arquivo in arquivos:
                fs1 = FileSystemStorage()
                filename1 = fs1.save(arquivo.name, arquivo)
                arquivo_url = fs1.url(filename1)
                arquivos_entregaveis.append(arquivo_url)
        except:
            arquivo_url = ''
        
        todos_arquivos = []
        arquivos = ast.literal_eval(entregavel.arquivos)
        arquivos_antigos = arquivos
        for arquivo in arquivos_antigos:
            todos_arquivos.append(arquivo)

        for arquivo in arquivos_entregaveis:
            todos_arquivos.append(arquivo)
        
        entregavel.arquivos = todos_arquivos

        entregavel.save()

    block = f'gerenciador_de_arquivos_entregavel_{entregavel.id}'
    tipo = 'entregavel'

    return render(request, 'ajax/ajax_load_files.html', {'arquivos': entregavel.arquivos,'solicitacao':entregavel,'block':block,'tipo':tipo})

@login_required(login_url='/')
def Ajax_Add_Entregavel(request):

    user_loggin = request.user.id
    solicitacao = request.POST.get('solicitacaoId','')
    solicitacao_entregavel = Solicitacoes.objects.filter(id=solicitacao).first()
    prazo_entrega = solicitacao_entregavel.prazo_entrega
    with transaction.atomic():  
        evento_id = request.POST.get('solicitacaoId','')
        tipo_produto = request.POST.get('tipoproduto_save_the_date','')
        categoria = request.POST.get('categoriaproduto_save_the_date','')
        tipo_entregavel = request.POST.get('tipo_entregavel','')
        audiovisual =  request.POST.get('audio_visual','')
        #observacoes =  request.POST.get('obs_save_the_date','')
        outros_entregaveis = request.POST.get('outro_entregavel','')
        arquivos = []

        entregavel = Entregaveis.objects.create(prazo = prazo_entrega, tipo_produto = tipo_produto, categoria_produto = categoria,tipo_entregavel = tipo_entregavel, descricao_audio_visual = audiovisual,arquivos = arquivos, status = 0,criado_por_id = user_loggin,evento_id = evento_id,outros = outros_entregaveis)
        nova_notificacao(request,evento_id)
        return JsonResponse({"success_message": "Tarefa Devolvida!"})

@login_required(login_url='/')
def Ajax_Reenvia_Entregavel(request):
    with transaction.atomic():
        entregavelId = request.POST.get('idEntregavel','')
        entregavel = Entregaveis.objects.get(id=entregavelId)
        entregavel.status = 0
        entregavel.save()


        devolver_correcao_entrega(request,entregavel.evento_id,request.user.id,entregavel.id)
        return JsonResponse({"success_message": "Tarefa Devolvida!"})
    
@login_required(login_url='/')
def Ajax_Delete_Files(request):
    with transaction.atomic():

        solicitacaoId = request.POST.get('solicitacao',None)
        arquivo_removido = request.POST.get('arquivo',None)
        tipo = request.POST.get('tipo',None)
        
        if tipo == 'solicitacao':
            solicitacao = Solicitacoes.objects.filter(id=solicitacaoId).first()
            arquivos = ast.literal_eval(solicitacao.arquivos)
            novos_arquivos = [] 
            for arquivo in arquivos:
                tag = '/media/'+arquivo_removido
                if tag not in arquivo:
                    novos_arquivos.append(arquivo)
                else:
                    url = settings.MEDIA_ROOT + '\\' + arquivo_removido
                    if default_storage.exists(arquivo_removido):
                        default_storage.delete(url)
                
            solicitacao.arquivos = novos_arquivos
            solicitacao.save()
        
            print(novos_arquivos)
            block = f'gerenciador_de_arquivos_solicitacao'
            tipo = 'solicitacao'
            return render(request, 'ajax/ajax_load_files.html', {'arquivos': solicitacao.arquivos,'solicitacao':solicitacao,'block':block,'tipo':tipo})
        
        elif tipo == 'entregavel':
            entregavel = Entregaveis.objects.filter(id=solicitacaoId).first()
            arquivos = ast.literal_eval(entregavel.arquivos)
            novos_arquivos = [] 
            for arquivo in arquivos:
                tag = '/media/'+arquivo_removido
                if tag not in arquivo:
                    novos_arquivos.append(arquivo)
                else:
                    url = settings.MEDIA_ROOT + '\\' + arquivo_removido
                    if default_storage.exists(arquivo_removido):
                        default_storage.delete(url)
                
            entregavel.arquivos = novos_arquivos
            entregavel.save()
            block = f'gerenciador_de_arquivos_entregavel_{entregavel.id}'
            tipo = 'entregavel'

            return render(request, 'ajax/ajax_load_files.html', {'arquivos': entregavel.arquivos,'solicitacao':entregavel,'block':block,'tipo':tipo })

@login_required(login_url='/')
def Ajax_Altera_Arquivos(request):
    solicitacaoID = request.POST.get('solicitacao',None)
    arquivo_removido = request.POST.get('arquivo',None)
    tipo = request.POST.get('tipo',None)

    with transaction.atomic():
        if tipo == 'solicitacao':
            solicitacao = Solicitacoes.objects.get(id=solicitacaoID)

            try:
                arquivos_solicitacao = []
                arquivos = request.FILES.getlist('files[]')
                for arquivo in arquivos:
                    fs1 = FileSystemStorage()
                    filename1 = fs1.save(arquivo.name, arquivo)
                    arquivo_url = fs1.url(filename1)
                    arquivos_solicitacao.append(arquivo_url)
            except:
                arquivo_url = ''

            todos_arquivos = []
            arquivos = ast.literal_eval(solicitacao.arquivos)
            arquivos_antigos = arquivos
            for arquivo in arquivos_antigos:
                todos_arquivos.append(arquivo)

            for arquivo in arquivos_solicitacao:
                todos_arquivos.append(arquivo)

            solicitacao.arquivos = todos_arquivos
            solicitacao.save()

            block = f'gerenciador_de_arquivos_solicitacao'
            tipo = 'solicitacao'

            return render(request, 'ajax/ajax_load_files.html', {'arquivos': solicitacao.arquivos,'solicitacao':solicitacao,'block':block,'tipo':tipo})
        
        elif tipo == 'entregavel':
            entregavel = Entregaveis.objects.get(id=solicitacaoID)

            try:
                arquivos_entregaveis = []
                arquivos = request.FILES.getlist('files[]')
                for arquivo in arquivos:
                    fs1 = FileSystemStorage()
                    filename1 = fs1.save(arquivo.name, arquivo)
                    arquivo_url = fs1.url(filename1)
                    arquivos_entregaveis.append(arquivo_url)
            except:
                arquivo_url = ''

            todos_arquivos = []
            arquivos = ast.literal_eval(entregavel.arquivos)
            arquivos_antigos = arquivos
            for arquivo in arquivos_antigos:
                todos_arquivos.append(arquivo)

            for arquivo in arquivos_entregaveis:
                todos_arquivos.append(arquivo)

            entregavel.arquivos = todos_arquivos
            entregavel.save()

            block = f'gerenciador_de_arquivos_entregavel_{entregavel.id}'
            tipo = 'entregavel'

            return render(request, 'ajax/ajax_load_files.html', {'arquivos': entregavel.arquivos,'solicitacao':entregavel,'block':block,'tipo':tipo})

@login_required(login_url='/')
def Ajax_Finalizar_Solicitacao(request):
     with transaction.atomic():
        solicitacaoID = request.POST.get('solicitacao_id', None)
        
        # Alterar status da solicitação
        solicitacao = Solicitacoes.objects.get(id=solicitacaoID)
        solicitacao.status = 3
        solicitacao.save()

        # Alterar status dos entregáveis relacionados à solicitação
        entregaveis = Entregaveis.objects.filter(evento_id=solicitacaoID)
        entregaveis.update(status=4)

        # Atualizar as tarefas relacionadas aos entregáveis
        for entregavel in entregaveis:
            Tarefas.objects.filter(entregavel_id=entregavel.id).update(status=4)
        
        return JsonResponse({"success_message": "Solicitação Finalizada"})