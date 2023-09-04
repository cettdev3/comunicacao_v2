from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from datetime import date,datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from login.models import Usuarios
from django.http import JsonResponse
import json
from django.utils.html import linebreaks
from datetime import datetime
from .utils import get_token_api_eventos,get_all_eventos,get_evento
import datetime
from .models import Entregaveis,Solicitacoes,Programacao_Adicional

@login_required(login_url='/')
def Form_Solicitacoes(request):

    token = get_token_api_eventos()
    eventos = get_all_eventos(token)


    data_atual = datetime.date.today()
    eventos_futuros = []
    if eventos:
        for evento in eventos:
            evento['data_fim'] = datetime.datetime.strptime(evento['data_fim'], '%Y-%m-%d').date()
            evento['data_inicio'] = datetime.datetime.strptime(evento['data_inicio'], '%Y-%m-%d').date()
            
            if evento['data_fim'] >= data_atual:
                eventos_futuros.append(evento)
    return render(request, 'solicitacoes.html',{'eventos':eventos_futuros})

@login_required(login_url='/')
def Dados_Gerais_Evento(request):
    print(request.GET)
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

    try:
        with transaction.atomic():

            #OBTÉM DADOS DA SOLICITAÇÃO
            idEvento = request.POST.get('eventos_gerais',None)
            tipoUnidade = request.POST.get('tipo_und',None)
            publicoEvento = request.POST.get('publico_evento',None)
            save_the_date = request.POST.get('save_the_date',None)
            programacao_evento = request.POST.get('programacao_evento',None)
            divulgacao_check = request.POST.get('divulgacao_check',None)
            programacao_check = request.POST.get('programacao_check',None)
            stand_check = request.POST.get('stand_check',None)
            evento_json = request.POST.get('json_data',None)
            userid = request.user.id
       
            token = get_token_api_eventos()
            json_evento = get_evento(token,idEvento)
            # json_string = str(json_evento).replace("'", "\"")


            #ANTES VERIFICA SE A SOLICITAÇÃO JÁ EXISTE
            solicitacao = Solicitacoes.objects.filter(evento_json__id = idEvento).first()
            if solicitacao:
                print(solicitacao.id)
            else:
                #CRIA A SOLICITACAO
                cria_solicitacao = Solicitacoes.objects.create(
                    tipo_projeto = tipoUnidade, 
                    publico_evento = publicoEvento,
                    criado_por_id = userid,
                    evento_json = json_evento,
                    status = 2
   
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
                    if 'prazo_save_the_date' in dado:
                        if dado == 'prazo_save_the_date':
                            prazo_save_the_date = request.POST.get(dado,None)
                            exemploarte_save_the_date = request.FILES.get('exemploarte_save_the_date',None)
                            tipoproduto_save_the_date = request.POST.get('tipoproduto_save_the_date',None)
                            categoriaproduto_save_the_date = request.POST.get('categoriaproduto_save_the_date',None)
                            descricao_save_the_date = request.POST.get('descricao_save_the_date',None)
                            obs_save_the_date = request.POST.get('obs_save_the_date',None)

                            #CONVERTE STRING PADRÃO 
                            if '    ' in descricao_save_the_date:
                                if descricao_save_the_date =='<p><br></p>':
                                    descricao_save_the_date = ''
                                descricao_save_the_date = descricao_save_the_date.strip()
                            
                            if '    ' in obs_save_the_date :
                                if obs_save_the_date == '<p><br></p>':
                                    obs_save_the_date = ''
                                obs_save_the_date = obs_save_the_date.strip()

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_save_the_date:
                                fss = FileSystemStorage()
                                exemploarte_save_the_date_file = fss.save(exemploarte_save_the_date.name, exemploarte_save_the_date)
                                exemploarte_save_the_date_url = fss.url(exemploarte_save_the_date_file)
                            else:
                                exemploarte_save_the_date_url = ''

                            
                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = cria_solicitacao.id,
                                prazo = prazo_save_the_date,
                                exemplo_arte = exemploarte_save_the_date_url,
                                tipo_entregavel = 1,
                                tipo_produto = tipoproduto_save_the_date,
                                categoria_produto = categoriaproduto_save_the_date,
                                descricao_audio_visual = descricao_save_the_date,
                                observacao = obs_save_the_date,
                                criado_por_id = userid

                                )
                            if eventos_entregaveis:
                                evento = Solicitacoes.objects.get(pk=cria_solicitacao.id)
                                evento.status = 1
                                evento.save()
                            
                        else:
                            index = dado[-1]
                            prazo_save_the_date = request.POST.get(dado,None)
                            exemploarte_save_the_date = request.FILES.get('exemploarte_save_the_date'+str(index),None)
                            tipoproduto_save_the_date = request.POST.get('tipoproduto_save_the_date'+str(index),None)
                            categoriaproduto_save_the_date = request.POST.get('categoriaproduto_save_the_date'+str(index),'')
                            descricao_save_the_date = request.POST.get('descricao_save_the_date'+str(index),None)
                            obs_save_the_date = request.POST.get('obs_save_the_date'+str(index),None)

                            #CONVERTE STRING PADRÃO 
                            if '    ' in descricao_save_the_date:
                                if descricao_save_the_date =='<p><br></p>':
                                    descricao_save_the_date = ''
                                descricao_save_the_date = descricao_save_the_date.strip()
                            
                            if '    ' in obs_save_the_date :
                                if obs_save_the_date == '<p><br></p>':
                                    obs_save_the_date = ''
                                obs_save_the_date = obs_save_the_date.strip()


                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_save_the_date:
                                fss = FileSystemStorage()
                                exemploarte_save_the_date_file = fss.save(exemploarte_save_the_date.name, exemploarte_save_the_date)
                                exemploarte_save_the_date_url = fss.url(exemploarte_save_the_date_file)
                            else:
                                exemploarte_save_the_date_url = ''


                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = cria_solicitacao.id,
                                prazo = prazo_save_the_date,
                                exemplo_arte = exemploarte_save_the_date_url,
                                tipo_entregavel = 1,
                                tipo_produto = tipoproduto_save_the_date,
                                categoria_produto = categoriaproduto_save_the_date,
                                descricao_audio_visual = descricao_save_the_date,
                                observacao = obs_save_the_date,
                                criado_por_id = userid
                                )
                            
                            if eventos_entregaveis:
                                evento = Solicitacoes.objects.get(pk=cria_solicitacao.id)
                                evento.status = 2
                                evento.save()

            #VERIFICA DIVULGAÇÃO
            indice = 0
            if divulgacao_check:
                for dado in dadosForm:
                    if 'prazo_divulgacao' in dado:
                        if dado == 'prazo_divulgacao':
                            prazo_divulgacao = request.POST.get('prazo_divulgacao',None)
                            exemploarte_divulgacao = request.FILES.get('exemploarte_divulgacao',None)
                            tipoproduto_divulgacao = request.POST.get('tipoproduto_divulgacao',None)
                            categoriaproduto_divulgacao = request.POST.get('categoriaproduto_divulgacao',None)
                            descricao_divulgacao = request.POST.get('descricao_divulgacao',None)
                            obs_divulgacao = request.POST.get('obs_divulgacao',None)

                            #CONVERTE STRING PADRÃO 
                            if '    ' in descricao_divulgacao:
                                if descricao_divulgacao == '<p><br></p>':
                                    descricao_divulgacao = ''
                                descricao_divulgacao = descricao_divulgacao.strip()
                            
                            if '    ' in obs_divulgacao:
                                if obs_divulgacao == '<p><br></p>':
                                    obs_divulgacao = ''
                                obs_divulgacao = obs_divulgacao.strip()

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_divulgacao:
                                fss = FileSystemStorage()
                                exemploarte_divulgacao_file = fss.save(exemploarte_divulgacao.name, exemploarte_divulgacao)
                                exemploarte_divulgacao_url = fss.url(exemploarte_divulgacao_file)
                            else:
                                exemploarte_divulgacao_url = ''

                            
                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = cria_solicitacao.id,
                                prazo = prazo_divulgacao,
                                exemplo_arte = exemploarte_divulgacao_url,
                                tipo_entregavel = 2,
                                tipo_produto = tipoproduto_divulgacao,
                                categoria_produto = categoriaproduto_divulgacao,
                                descricao_audio_visual = descricao_divulgacao,
                                observacao = obs_divulgacao,
                                criado_por_id = userid
                                )
                            if eventos_entregaveis:
                                evento = Solicitacoes.objects.get(pk=cria_solicitacao.id)
                                evento.status = 1
                                evento.save()
                        else:
                            index = dado[-1]
                            prazo_divulgacao = request.POST.get('prazo_divulgacao'+str(index),None)
                            exemploarte_divulgacao = request.FILES.get('exemploarte_divulgacao'+str(index),None)
                            tipoproduto_divulgacao = request.POST.get('tipoproduto_divulgacao'+str(index),None)
                            categoriaproduto_divulgacao = request.POST.get('categoriaproduto_divulgacao'+str(index),None)
                            descricao_divulgacao = request.POST.get('descricao_divulgacao'+str(index),None)
                            obs_divulgacao = request.POST.get('obs_divulgacao'+str(index),None)

                            #CONVERTE STRING PADRÃO 
                            if '    ' in descricao_divulgacao:
                                if descricao_divulgacao == '<p><br></p>':
                                    descricao_divulgacao = ''
                                descricao_divulgacao = descricao_divulgacao.strip()
                            
                            if '    ' in obs_divulgacao:
                                if obs_divulgacao == '<p><br></p>':
                                    obs_divulgacao = ''
                                obs_divulgacao = obs_divulgacao.strip()

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_divulgacao:
                                fss = FileSystemStorage()
                                exemploarte_divulgacao_file = fss.save(exemploarte_divulgacao.name, exemploarte_divulgacao)
                                exemploarte_divulgacao_url = fss.url(exemploarte_divulgacao_file)
                            else:
                                exemploarte_divulgacao_url = ''

                            
                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = cria_solicitacao.id,
                                prazo = prazo_divulgacao,
                                exemplo_arte = exemploarte_divulgacao_url,
                                tipo_entregavel = 2,
                                tipo_produto = tipoproduto_divulgacao,
                                categoria_produto = categoriaproduto_divulgacao,
                                descricao_audio_visual = descricao_divulgacao,
                                observacao = obs_divulgacao,
                                criado_por_id = userid
                                )
                            
                            if eventos_entregaveis:
                                evento = Solicitacoes.objects.get(pk=cria_solicitacao.id)
                                evento.status = 1
                                evento.save()
           
            #VERIFICA PROGRAMAÇÃO
            indice = 0
            if programacao_check:
                for dado in dadosForm:
                    if 'prazo_programacao' in dado:
                        if dado == 'prazo_programacao':
                            prazo_programacao = request.POST.get('prazo_programacao',None)
                            exemploarte_programacao = request.FILES.get('exemploarte_programacao',None)
                            tipoproduto_programacao = request.POST.get('tipoproduto_programacao',None)
                            categoriaproduto_programacao = request.POST.get('categoriaproduto_programacao',None)
                            descricao_programacao = request.POST.get('descricao_programacao',None)
                            obs_programacao = request.POST.get('obs_programacao',None)

                            #CONVERTE STRING PADRÃO 
                            if '    ' in descricao_programacao:
                                if descricao_programacao == '<p><br></p>':
                                    descricao_programacao = ''
                                descricao_programacao = descricao_programacao.strip()
                            
                            if '    ' in obs_programacao:
                                if obs_programacao == '<p><br></p>':
                                    obs_programacao = ''
                                obs_programacao = obs_programacao.strip()

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_programacao:
                                fss = FileSystemStorage()
                                exemploarte_programacao_file = fss.save(exemploarte_programacao.name, exemploarte_programacao)
                                exemploarte_programacao_url = fss.url(exemploarte_programacao_file)
                            else:
                                exemploarte_programacao_url = ''

                            
                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = cria_solicitacao.id,
                                prazo = prazo_programacao,
                                exemplo_arte = exemploarte_programacao_url,
                                tipo_entregavel = 3,
                                tipo_produto = tipoproduto_programacao,
                                categoria_produto = categoriaproduto_programacao,
                                descricao_audio_visual = descricao_programacao,
                                observacao = obs_programacao,
                                criado_por_id = userid
                                )
                            
                            if eventos_entregaveis:
                                evento = Solicitacoes.objects.get(pk=cria_solicitacao.id)
                                evento.status = 1
                                evento.save()
                        else:
                            index = dado[-1]
                            prazo_programacao = request.POST.get('prazo_programacao'+str(index),None)
                            exemploarte_programacao = request.FILES.get('exemploarte_programacao'+str(index),None)
                            tipoproduto_programacao = request.POST.get('tipoproduto_programacao'+str(index),None)
                            categoriaproduto_programacao = request.POST.get('categoriaproduto_programacao'+str(index),None)
                            descricao_programacao = request.POST.get('descricao_programacao'+str(index),None)
                            obs_programacao = request.POST.get('obs_programacao'+str(index),None)

                             #CONVERTE STRING PADRÃO 
                            if '    ' in descricao_programacao:
                                if descricao_programacao == '<p><br></p>':
                                    descricao_programacao = ''
                                descricao_programacao = descricao_programacao.strip()
                            
                            if '    ' in obs_programacao:
                                if obs_programacao == '<p><br></p>':
                                    obs_programacao = ''
                                obs_programacao = obs_programacao.strip()

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_programacao:
                                fss = FileSystemStorage()
                                exemploarte_programacao_file = fss.save(exemploarte_programacao.name, exemploarte_programacao)
                                exemploarte_programacao_url = fss.url(exemploarte_programacao_file)
                            else:
                                exemploarte_programacao_url = ''

                            
                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = cria_solicitacao.id,
                                prazo = prazo_programacao,
                                exemplo_arte = exemploarte_programacao_url,
                                tipo_entregavel = 3,
                                tipo_produto = tipoproduto_programacao,
                                categoria_produto = categoriaproduto_programacao,
                                descricao_audio_visual = descricao_programacao,
                                observacao = obs_programacao,
                                criado_por_id = userid
                                )
                            
                            if eventos_entregaveis:
                                evento = Solicitacoes.objects.get(pk=cria_solicitacao.id)
                                evento.status = 1
                                evento.save()
            
            #VERIFICA STAND
            indice = 0
            if stand_check:
                for dado in dadosForm:
                    if 'prazo_stand' in dado:
                        if dado == 'prazo_stand':
                            prazo_stand = request.POST.get('prazo_stand',None)
                            exemploarte_stand = request.FILES.get('exemploarte_stand',None)
                            tipoproduto_stand = request.POST.get('tipoproduto_stand',None)
                            categoriaproduto_stand = request.POST.get('categoriaproduto_stand',None)
                            descricao_stand = request.POST.get('descricao_stand',None)
                            obs_stand = request.POST.get('obs_stand',None)
                            userid = request.user.id

                            #CONVERTE STRING PADRÃO 
                            if '    ' in descricao_stand:
                                if descricao_stand == '<p><br></p>':
                                    descricao_stand = ''
                                descricao_stand = descricao_stand.strip()
                            
                            if '    ' in obs_stand:
                                if obs_stand == '<p><br></p>':
                                    obs_stand = ''
                                obs_stand = obs_stand.strip()

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_stand:
                                fss = FileSystemStorage()
                                exemploarte_stand_file = fss.save(exemploarte_stand.name, exemploarte_stand)
                                exemploarte_stand_url = fss.url(exemploarte_stand_file)
                            else:
                                exemploarte_stand_url = ''

                            
                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = cria_solicitacao.id,
                                prazo = prazo_stand,
                                exemplo_arte = exemploarte_stand_url,
                                tipo_entregavel = 4,
                                tipo_produto = tipoproduto_stand,
                                categoria_produto = categoriaproduto_stand,
                                descricao_audio_visual = descricao_stand,
                                observacao = obs_stand,
                                criado_por_id = userid 
                                )
                            
                            if eventos_entregaveis:
                                evento = Solicitacoes.objects.get(pk=cria_solicitacao.id)
                                evento.status = 1
                                evento.save()
                        else:
                            index = dado[-1]
                            prazo_stand = request.POST.get('prazo_stand'+str(index),None)
                            exemploarte_stand = request.FILES.get('exemploarte_stand'+str(index),None)
                            tipoproduto_stand = request.POST.get('tipoproduto_stand'+str(index),None)
                            categoriaproduto_stand = request.POST.get('categoriaproduto_stand'+str(index),None)
                            descricao_stand = request.POST.get('descricao_stand'+str(index),None)
                            obs_stand = request.POST.get('obs_stand'+str(index),None)

                             #CONVERTE STRING PADRÃO 
                            if '    ' in descricao_stand:
                                if descricao_stand == '<p><br></p>':
                                    descricao_stand = ''
                                descricao_stand = descricao_stand.strip()
                            
                            if '    ' in obs_stand:
                                if obs_stand == '<p><br></p>':
                                    obs_stand = ''
                                obs_stand = obs_stand.strip()

                            #CODIFICA PARA OBTER A URL E ADICIONAR IMAGEM NO SISTEMA
                            if exemploarte_stand:
                                fss = FileSystemStorage()
                                exemploarte_stand_file = fss.save(exemploarte_stand.name, exemploarte_stand)
                                exemploarte_stand_url = fss.url(exemploarte_stand_file)
                            else:
                                exemploarte_stand_url = ''

                            
                            eventos_entregaveis = Entregaveis.objects.create(
                                evento_id = cria_solicitacao.id,
                                prazo = prazo_stand,
                                exemplo_arte = exemploarte_stand_url,
                                tipo_entregavel = 3,
                                tipo_produto = tipoproduto_stand,
                                categoria_produto = categoriaproduto_stand,
                                descricao_audio_visual = descricao_stand,
                                observacao = obs_stand,
                                criado_por_id = userid
                                )
                            
                            if eventos_entregaveis:
                                evento = Solicitacoes.objects.get(pk=cria_solicitacao.id)
                                evento.status = 1
                                evento.save()
            
            return JsonResponse({"success_message": "Solicitação Realizada!"}) 
        
    except Exception as e:
         return JsonResponse({"error_message": "Não foi possível realizar a solicitação: " + str(e)}, status=400)
