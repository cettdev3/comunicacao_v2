from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from datetime import date,datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.utils.html import linebreaks
from datetime import datetime
from .utils import get_token_api_eventos,get_all_eventos,get_evento
import datetime
from .models import Entregaveis,Solicitacoes,Programacao_Adicional,Tarefas,Escolas
from .serializers import Solicitacao_Serializar,Tarefas_Serializar,Entregaveis_Serializar
from django.contrib.auth.models import User
from gerir_time.models import Permissoes

def convert_data_formatada(data):
    print(data)
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
    messages.success(request, 'Usuário cadastrado com sucesso!')
    return redirect('/gerir-time')

@login_required(login_url='/')
def Form_Solicitacoes(request):
    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first
    token = get_token_api_eventos()
    eventos = get_all_eventos(token)

  
    if eventos:
        for evento in eventos:
            try:
                evento['data_fim'] = datetime.datetime.strptime(evento['data_fim'], '%Y-%m-%d').date()
                evento['data_inicio'] = datetime.datetime.strptime(evento['data_inicio'], '%Y-%m-%d').date()
            except:
                pass


    return render(request, 'solicitacoes.html',{'eventos':eventos,'permissoes':permissoes})

@login_required(login_url='/')
def Visualizar_Solicitacao(request,codigo):
    permissoes = Permissoes.objects.filter(usuario_id=request.user.id).first()

    solicitacao = Solicitacoes.objects.filter(id=codigo).first()
    if solicitacao.criado_por_id == request.user.id or permissoes.departamento_id == 1:
        solicitacao = Solicitacao_Serializar(solicitacao).data
        solicitacao['data_solicitacao'] = datetime.datetime.strptime(solicitacao['data_solicitacao'], '%Y-%m-%d').date()
        
        programacao_adicional = Programacao_Adicional.objects.filter(solicitacao_id=codigo).all()


        entregaveis = Entregaveis.objects.filter(evento_id=codigo).all()
        entregaveis = Entregaveis_Serializar(entregaveis,many=True).data
        tarefas_por_entregavel = {}

        for entregavel in entregaveis:
            entregavel['prazo'] = datetime.datetime.strptime(entregavel['prazo'], '%Y-%m-%d').date()
            entregavel['data_solicitacao'] = datetime.datetime.strptime(entregavel['data_solicitacao'], '%Y-%m-%d').date()
            try:
                tarefas_relacionadas = Tarefas.objects.filter(entregavel_id=entregavel['id']).latest('id')
            except:
                tarefas_relacionadas = {}

            entregavel['tarefas_relacionadas'] = tarefas_relacionadas

        usuarios = User.objects.all()
        context = {'solicitacao':solicitacao,'entregaveis':entregaveis,'programacao_adicional':programacao_adicional,'usuarios':usuarios,'tarefas_por_entregavel': tarefas_por_entregavel,'permissoes':permissoes}
        return render(request,'visualizar_solicitacao.html',context)
    else:
        messages.error(request, 'Você não tem permissões para acessar!')
        return redirect('/solicitacoes')


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
    print(dadosForm)
    try:
        with transaction.atomic():

            #OBTÉM DADOS DA SOLICITAÇÃO
            idEvento = request.POST.get('eventos_gerais',None)
            publicoEvento = request.POST.get('publico_evento',None)
            save_the_date = request.POST.get('save_the_date',None)
            programacao_evento = request.POST.get('programacao_evento',None)
            divulgacao_check = request.POST.get('divulgacao_check',None)
            programacao_check = request.POST.get('programacao_check',None)
            stand_check = request.POST.get('stand_check',None)
            userid = request.user.id

            if idEvento != 'und':
                tipoUnidade = request.POST.get('tipo_und',None)
                token = get_token_api_eventos()
                json_evento = get_evento(token,idEvento)
                # json_string = str(json_evento).replace("'", "\"")
                print(request.user.id)

                #ANTES VERIFICA SE A SOLICITAÇÃO JÁ EXISTE
                solicitacao = Solicitacoes.objects.filter(evento_json__id = idEvento).first()
                if solicitacao:
                    print(solicitacao.id)
                else:
                    #CRIA A SOLICITACAO
                    solicitacao = Solicitacoes.objects.create(
                        tipo_projeto = tipoUnidade, 
                        publico_evento = publicoEvento,
                        criado_por_id = userid,
                        evento_json = json_evento,
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
                                evento_id = solicitacao.id,
                                prazo = prazo_save_the_date,
                                exemplo_arte = exemploarte_save_the_date_url,
                                tipo_entregavel = 1,
                                tipo_produto = tipoproduto_save_the_date,
                                categoria_produto = categoriaproduto_save_the_date,
                                descricao_audio_visual = descricao_save_the_date,
                                observacao = obs_save_the_date,
                                criado_por_id = userid

                                )
     
                            
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
                                evento_id = solicitacao.id,
                                prazo = prazo_save_the_date,
                                exemplo_arte = exemploarte_save_the_date_url,
                                tipo_entregavel = 1,
                                tipo_produto = tipoproduto_save_the_date,
                                categoria_produto = categoriaproduto_save_the_date,
                                descricao_audio_visual = descricao_save_the_date,
                                observacao = obs_save_the_date,
                                criado_por_id = userid
                                )
                            
 
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
                                evento_id = solicitacao.id,
                                prazo = prazo_divulgacao,
                                exemplo_arte = exemploarte_divulgacao_url,
                                tipo_entregavel = 2,
                                tipo_produto = tipoproduto_divulgacao,
                                categoria_produto = categoriaproduto_divulgacao,
                                descricao_audio_visual = descricao_divulgacao,
                                observacao = obs_divulgacao,
                                criado_por_id = userid
                                )
             
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
                                evento_id = solicitacao.id,
                                prazo = prazo_divulgacao,
                                exemplo_arte = exemploarte_divulgacao_url,
                                tipo_entregavel = 2,
                                tipo_produto = tipoproduto_divulgacao,
                                categoria_produto = categoriaproduto_divulgacao,
                                descricao_audio_visual = descricao_divulgacao,
                                observacao = obs_divulgacao,
                                criado_por_id = userid
                                )

           
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
                                evento_id = solicitacao.id,
                                prazo = prazo_programacao,
                                exemplo_arte = exemploarte_programacao_url,
                                tipo_entregavel = 3,
                                tipo_produto = tipoproduto_programacao,
                                categoria_produto = categoriaproduto_programacao,
                                descricao_audio_visual = descricao_programacao,
                                observacao = obs_programacao,
                                criado_por_id = userid
                                )
               
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
                                evento_id = solicitacao.id,
                                prazo = prazo_programacao,
                                exemplo_arte = exemploarte_programacao_url,
                                tipo_entregavel = 3,
                                tipo_produto = tipoproduto_programacao,
                                categoria_produto = categoriaproduto_programacao,
                                descricao_audio_visual = descricao_programacao,
                                observacao = obs_programacao,
                                criado_por_id = userid
                                )
                            
                  
            
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
                                evento_id = solicitacao.id,
                                prazo = prazo_stand,
                                exemplo_arte = exemploarte_stand_url,
                                tipo_entregavel = 4,
                                tipo_produto = tipoproduto_stand,
                                categoria_produto = categoriaproduto_stand,
                                descricao_audio_visual = descricao_stand,
                                observacao = obs_stand,
                                criado_por_id = userid 
                                )
                            
                   
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
                                evento_id = solicitacao.id,
                                prazo = prazo_stand,
                                exemplo_arte = exemploarte_stand_url,
                                tipo_entregavel = 3,
                                tipo_produto = tipoproduto_stand,
                                categoria_produto = categoriaproduto_stand,
                                descricao_audio_visual = descricao_stand,
                                observacao = obs_stand,
                                criado_por_id = userid
                                )
                            
                    
            
            return JsonResponse({"success_message": "Solicitação Realizada!"}) 
        
    except Exception as e:
         return JsonResponse({"error_message": "Não foi possível realizar a solicitação: " + str(e)}, status=400)

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
        tarefas = Tarefas.objects.filter(entregavel_id = entregavel_id ).all()

        return render(request,'ajax/ajax_load_tbl_tarefas.html',{'tarefas':tarefas})
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
            return JsonResponse({"success_message": "Tarefa Negada!"})
        elif tipo == '2':
            entregavel = Entregaveis.objects.get(id=entregavelId)
            entregavel.status = 5
            entregavel.motivo_revisao = descricao_negativa
            entregavel.save()
            return JsonResponse({"success_message": "Tarefa Devolvida!"})

    except Exception as e:
        return JsonResponse({"error_message": "Não foi possível realizar a solicitação: " + str(e)}, status=400)

@login_required(login_url='/')
def Ajax_Altera_Entregavel(request):
    entregavelID = request.GET['entregavelId']
    entregavel = Entregaveis.objects.filter(id=entregavelID).first()
    
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
