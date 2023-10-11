from django.contrib.auth.models import User
from solicitacoes.models import Entregaveis, Solicitacoes, Tarefas, Programacao_Adicional
from menu.models import Notificacoes
from datetime import datetime
from django.core.files.storage import FileSystemStorage, default_storage
from setup.settings import MEDIA_ROOT
import os
from django.core.files.base import ContentFile
import base64


def convert(src):
    with open(src, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        decoded_image = base64.b64decode(encoded_image)
    return decoded_image


def createSolicitacao(solicitacaoData):
    criado_por = User.objects.get(id=int(solicitacaoData['criado_por_id']))
    evento_json = solicitacaoData['evento_json']
    motivo_alteracao = solicitacaoData['motivo_alteracao']
    tipo_projeto = int(solicitacaoData['tipo_projeto'])
    publico_evento = solicitacaoData['publico_evento']
    data_solicitacao = solicitacaoData['data_solicitacao']
    statusSolicitacao = solicitacaoData['status']
    briefing = solicitacaoData['briefing']

    solicitacao = Solicitacoes(criado_por=criado_por, evento_json=evento_json, motivo_alteracao=motivo_alteracao,
                               tipo_projeto=tipo_projeto, publico_evento=publico_evento, data_solicitacao=data_solicitacao,
                               status=statusSolicitacao, briefing=briefing)
    solicitacao.save()

    return solicitacao


def createEntregavel(entregavelData, solicitacao):
    if solicitacao is None:
        solicitacaolId = int(entregavelData['solicitacao_id'])
        solicitacao = Solicitacoes.objects.get(id=solicitacaolId)

    if 'prazo' not in entregavelData:
        prazo = solicitacao.prazo_entrega
    else:
        prazo = datetime.strptime(entregavelData['prazo'], '%Y-%m-%d').date()
    criado_por = User.objects.get(
        id=int(entregavelData['criado_por_id']))

    data_solicitacao = datetime.strptime(
        entregavelData['data_solicitacao'], '%Y-%m-%d').date()
    tipo_entregavel = int(entregavelData['tipo_entregavel'])
    tipo_produto = int(entregavelData['tipo_produto'])
    categoria_produto = entregavelData['categoria_produto']
    descricao_audio_visual = entregavelData['descricao_audio_visual']
    observacao = entregavelData['observacao']
    motivo_revisao = entregavelData['motivo_revisao']
    statusEntregavel = int(entregavelData['status'])

    fs = FileSystemStorage()
    exemplo_arte_url = entregavelData['exemplo_arte']
    file_name = os.path.basename(exemplo_arte_url)
    decoded_file = convert(exemplo_arte_url)
    file = ContentFile(decoded_file, name=file_name)
    saved_file_name = fs.save(file.name, file)
    urEntregavel = fs.url(saved_file_name)

    entregavel = Entregaveis(prazo=prazo, data_solicitacao=data_solicitacao, exemplo_arte=urEntregavel,
                             tipo_entregavel=tipo_entregavel, tipo_produto=tipo_produto,
                             categoria_produto=categoria_produto, descricao_audio_visual=descricao_audio_visual, observacao=observacao,
                             motivo_revisao=motivo_revisao, status=statusEntregavel)
    entregavel.evento = solicitacao
    entregavel.criado_por = criado_por
    entregavel.save()

    return entregavel


def createTarefa(tarefaData, entregavel):
    if entregavel is None:
        entregavelId = int(tarefaData['entregavel_id'])
        entregavel = Entregaveis.objects.get(id=entregavelId)

    usuario = User.objects.get(id=int(tarefaData['usuario_id']))
    usuario_designou = User.objects.get(
        id=int(tarefaData['usuario_designou_id']))
    titulo_tarefa = tarefaData['titulo_tarefa']
    data_tarefa = datetime.strptime(
        tarefaData['data_tarefa'], '%Y-%m-%d').date()
    prazo_entrega = datetime.strptime(
        tarefaData['prazo_entrega'], '%Y-%m-%d').date()
    data_entrega = datetime.strptime(
        tarefaData['data_entrega'], '%Y-%m-%d').date()
    descricao_tarefa = tarefaData['descricao_tarefa']
    descricao_entrega = tarefaData['descricao_entrega']
    prioridade = int(tarefaData['prioridade'])
    tipo = int(tarefaData['tipo'])
    statusTarefa = int(tarefaData['status'])

    fs = FileSystemStorage()
    urlArquivosSalvos = []
    arquivos = tarefaData['arquivos']
    for arquivo in arquivos:
        file_name = os.path.basename(arquivo)
        decoded_file = convert(arquivo)
        file = ContentFile(decoded_file, name=file_name)
        saved_file_name = fs.save(file.name, file)
        urlArquivo = fs.url(saved_file_name)
        urlArquivosSalvos.append(urlArquivo)

    tarefa = Tarefas(titulo_tarefa=titulo_tarefa, data_tarefa=data_tarefa, prazo_entrega=prazo_entrega,
                     data_entrega=data_entrega, descricao_tarefa=descricao_tarefa, descricao_entrega=descricao_entrega,
                     prioridade=prioridade, tipo=tipo, status=statusTarefa, arquivos=arquivos)
    tarefa.entregavel = entregavel
    tarefa.usuario = usuario
    tarefa.usuario_designou = usuario_designou
    tarefa.arquivos = str(urlArquivosSalvos)
    tarefa.save()

    return tarefa


def createProgramacao(programacaoData, solicitacao):
    if solicitacao is None:
        solicitacaoId = int(programacaoData['solicitacao_id'])
        solicitacao = Solicitacoes.objects.get(id=solicitacaoId)

    data = datetime.strptime(
        programacaoData['data'], '%Y-%m-%d').date()
    hora = programacaoData['hora']
    hora_final = programacaoData['hora_final']
    atividade = programacaoData['atividade']

    programacao = Programacao_Adicional(
        data=data, hora=hora, hora_final=hora_final, atividade=atividade)
    programacao.solicitacao = solicitacao
    programacao.save()

    return programacao


def createNotificacao(notificacaoData):
    data = datetime.strptime(notificacaoData['data'], '%Y-%m-%dT%H:%M:%S')
    user = User.objects.get(id=int(notificacaoData['user_id']))
    descricao = notificacaoData['descricao']
    origem = User.objects.get(id=int(notificacaoData['origem_id']))
    readonly = int(notificacaoData['readonly'])

    notificacao = Notificacoes(
        data=data, user=user, descricao=descricao, origem=origem, readonly=readonly)
    notificacao.save()

    return notificacao


def updateSolicitacao(solicitacaoData, pk):
    solicitacao = Solicitacoes.objects.get(id=pk)

    if 'criado_por_id' in solicitacaoData:
        criado_por = User.objects.get(id=int(solicitacaoData['criado_por_id']))
        solicitacao.criado_por = criado_por
    if 'evento_json' in solicitacaoData:
        evento_json = solicitacaoData['evento_json']
        solicitacao.evento_json = evento_json
    if 'motivo_alteracao' in solicitacaoData:
        motivo_alteracao = solicitacaoData['motivo_alteracao']
        solicitacao.motivo_alteracao = motivo_alteracao
    if 'tipo_projeto' in solicitacaoData:
        tipo_projeto = int(solicitacaoData['tipo_projeto'])
        solicitacao.tipo_projeto = tipo_projeto
    if 'publico_evento' in solicitacaoData:
        publico_evento = solicitacaoData['publico_evento']
        solicitacao.publico_evento = publico_evento
    if 'data_solicitacao' in solicitacaoData:
        data_solicitacao = datetime.strptime(
            solicitacaoData['data_solicitacao'], '%Y-%m-%d')
        solicitacao.data_solicitacao = data_solicitacao
    if 'status' in solicitacaoData:
        status = solicitacaoData['status']
        solicitacao.status = status
    if 'briefing' in solicitacaoData:
        briefing = solicitacaoData['briefing']
        solicitacao.briefing = briefing

    solicitacao.save()
    return solicitacao


def updateEntregavel(entregavelData, pk):
    entregavel = Entregaveis.objects.get(id=pk)

    if 'criado_por_id' in entregavelData:
        criado_por = User.objects.get(id=int(entregavelData['criado_por_id']))
        entregavel.criado_por = criado_por
    if 'prazo' in entregavelData:
        prazo = datetime.strptime(entregavelData['prazo'], '%Y-%m-%d').date()
        entregavel.prazo = prazo
    if 'data_solicitacao' in entregavelData:
        data_solicitacao = datetime.strptime(
            entregavelData['data_solicitacao'], '%Y-%m-%d').date()
        entregavel.data_solicitacao = data_solicitacao
    if 'tipo_entregavel' in entregavelData:
        tipo_entregavel = int(entregavelData['tipo_entregavel'])
        entregavel.tipo_entregavel = tipo_entregavel
    if 'tipo_produto' in entregavelData:
        tipo_produto = int(entregavelData['tipo_produto'])
        entregavel.tipo_produto = tipo_produto
    if 'categoria_produto' in entregavelData:
        categoria_produto = entregavelData['categoria_produto']
        entregavel.categoria_produto = categoria_produto
    if 'descricao_audio_visual' in entregavelData:
        descricao_audio_visual = entregavelData['descricao_audio_visual']
        entregavel.descricao_audio_visual = descricao_audio_visual
    if 'observacao' in entregavelData:
        observacao = entregavelData['observacao']
        entregavel.observacao = observacao
    if 'motivo_revisao' in entregavelData:
        motivo_revisao = entregavelData['motivo_revisao']
        entregavel.motivo_revisao = motivo_revisao
    if 'statusEntregavel' in entregavelData:
        status = int(entregavelData['status'])
        entregavel.status = status

    if 'exemplo_arte' in entregavelData:
        url = f"{MEDIA_ROOT}\\{str(entregavel.exemplo_arte)[1:]}"
        if default_storage.exists(url):
            default_storage.delete(url)

        fs = FileSystemStorage()
        exemplo_arte_url = entregavelData['exemplo_arte']
        file_name = os.path.basename(exemplo_arte_url)
        decoded_file = convert(exemplo_arte_url)
        file = ContentFile(decoded_file, name=file_name)
        saved_file_name = fs.save(file.name, file)
        urEntregavel = fs.url(saved_file_name)
        entregavel.exemplo_arte = urEntregavel

    entregavel.save()

    return entregavel


def updateTarefa(tarefaData, pk):
    tarefa = Tarefas.objects.get(id=pk)

    if 'usuario_id' in tarefaData:
        usuario = User.objects.get(id=int(tarefaData['usuario_id']))
        tarefa.usuario = usuario
    if 'titulo_tarefa' in tarefaData:
        titulo_tarefa = tarefaData['titulo_tarefa']
        tarefa.titulo_tarefa = titulo_tarefa
    if 'data_tarefa' in tarefaData:
        data_tarefa = datetime.strptime(
            tarefaData['data_tarefa'], '%Y-%m-%d').date()
        tarefa.data_tarefa = data_tarefa
    if 'prazo_entrega' in tarefaData:
        prazo_entrega = datetime.strptime(
            tarefaData['prazo_entrega'], '%Y-%m-%d').date()
        tarefa.prazo_entrega = prazo_entrega
    if 'data_entrega' in tarefaData:
        data_entrega = datetime.strptime(
            tarefaData['data_entrega'], '%Y-%m-%d').date()
        tarefa.data_entrega = data_entrega
    if 'descricao_tarefa' in tarefaData:
        descricao_tarefa = tarefaData['descricao_tarefa']
        tarefa.descricao_tarefa = descricao_tarefa
    if 'descricao_entrega' in tarefaData:
        descricao_entrega = tarefaData['descricao_entrega']
        tarefa.descricao_entrega = descricao_entrega
    if 'prioridade' in tarefaData:
        prioridade = int(tarefaData['prioridade'])
        tarefa.prioridade = prioridade
    if 'tipo' in tarefaData:
        tipo = int(tarefaData['tipo'])
        tarefa.tipo = tipo
    if 'status' in tarefaData:
        status = int(tarefaData['status'])
        tarefa.status = status

    if 'arquivos' in tarefaData and tarefaData['arquivos'] is not []:
        fs = FileSystemStorage()
        urlArquivosSalvos = []
        arquivos = tarefaData['arquivos']
        for arquivo in arquivos:
            file_name = os.path.basename(arquivo)
            decoded_file = convert(arquivo)
            file = ContentFile(decoded_file, name=file_name)
            saved_file_name = fs.save(file.name, file)
            urlArquivo = fs.url(saved_file_name)
            urlArquivosSalvos.append(urlArquivo)
        tarefa.arquivos = str(urlArquivosSalvos)

    tarefa.save()
    return tarefa


def updateProgramacao(programacaoData, pk):
    programacao = Programacao_Adicional.objects.get(id=pk)
    if 'data' in programacaoData:
        data = datetime.strptime(programacaoData['data'], '%Y-%m-%d').date()
        programacao.data = data
    if 'hora' in programacaoData:
        hora = programacaoData['hora']
        programacao.hora = hora
    if 'hora_final' in programacaoData:
        hora_final = programacaoData['hora_final']
        programacao.hora_final = hora_final
    if 'atividade' in programacaoData:
        atividade = programacaoData['atividade']
        programacao.atividade = atividade

    programacao.save()
    return programacao


def updateNotificacao(notificacaoData, pk):
    notificacao = Notificacoes.objects.get(id=pk)
    if 'data' in notificacaoData:
        data = datetime.strptime(notificacaoData['data'], '%Y-%m-%dT%H:%M:%S')
        notificacao.data = data
    if 'user_id' in notificacaoData:
        user = User.objects.get(id=int(notificacaoData['user_id']))
        notificacao.user = user
    if 'descricao' in notificacaoData:
        descricao = notificacaoData['descricao']
        notificacao.descricao = descricao
    if 'origem' in notificacaoData:
        origem = User.objects.get(id=int(notificacaoData['origem']))
        notificacao.origem = origem
    if 'readonly' in notificacaoData:
        readonly = int(notificacaoData['readonly'])
        notificacao.readonly = readonly

    notificacao.save()
    return notificacao


def getAllInstances(model, serializerClass):
    instances = model.objects.all()
    serializer = serializerClass(instances, many=True)
    myData = serializer.data
    return myData


def getSingleInstance(model, serializerClass, pk):
    instance = model.objects.get(id=pk)
    myData = serializerClass(instance).data
    return myData
