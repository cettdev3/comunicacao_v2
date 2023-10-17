from django.contrib.auth.models import User
from gerir_time.models import Permissoes
from menu.models import Notificacoes

#Notifica uma nova solicitação
def nova_notificacao(request,solicitacao_id):
    usuarios_notify = Permissoes.objects.all()
    for usuario in usuarios_notify:
        if '12' in usuario.permissao:
            descricao = f'''<b>Nova Solicitação!</b></br>
                            <b>{request.user.first_name}</b> criou uma nova solicitação!</br></br>
                            Acesse a solicitação clicando <a href='/solicitacoes/visualizar/{solicitacao_id}' target='_blank' >AQUI</a>
                            </br>
                        '''
            notificacao = Notificacoes.objects.create(user_id = usuario.id,descricao = descricao,origem_id = request.user.id,readonly = 1)
    return True

#Notifica designação de nova tarefa
def nova_tarefa(request,solicitacao_id,usuario_designado,tarefa_id,entregavel_id):

    descricao = f'''<b>Nova Tarefa!</b></br>
                    <b>{request.user.first_name}</b> te designou para cumprir uma tarefa!</br></br>
                    Acesse a solicitação clicando <a href='/minhas-tarefas' target='_blank' >AQUI</a>.
                    </br><br>
                    Há e não se esqueça, o id da tarefa é <b>#{tarefa_id}</b> e do entregável é <b>#{entregavel_id}</b> ! :D      

                    '''
    notificacao = Notificacoes.objects.create(user_id = usuario_designado,descricao = descricao,origem_id = request.user.id,readonly = 1)
    return True

#Notifica quando o usuário conclui a tarefa
def tarefa_concluida(request,destinatario,autor,solicitacao_id,entregavel_id,tarefa_id):

    descricao = f'''<b>Tarefa Concluída!</b></br>
                    <b>{request.user.first_name}</b> acabou de concluir uma tarefa!</br></br>
                    Acesse a solicitação clicando <a href='/solicitacoes/visualizar/{solicitacao_id}' target='_blank' >AQUI</a>.
                    </br><br>
                    Há e não se esqueça, o id da tarefa é <b>#{tarefa_id}</b> e do entregável é <b>#{entregavel_id}</b>! :D
                    

                '''
    notificacao = Notificacoes.objects.create(user_id = destinatario.id,descricao = descricao,origem_id = autor,readonly = 1)
    return True

#Notifica designação de nova tarefa
def tarefa_em_revisao(request,solicitacao_id,usuario_designado,tarefa_id,entregavel_id):

    descricao = f'''<b>Revisão de Tarefa!</b></br>
                    <b>{request.user.first_name}</b> te designou corrigir uma tarefa entregue!</br></br>
                    Acesse a solicitação clicando <a href='/minhas-tarefas' target='_blank' >AQUI</a>.
                    </br><br>
                    Há e não se esqueça, o id da tarefa é <b>#{tarefa_id}</b> e do entregável é <b>#{entregavel_id}</b> ! :D      

                    '''
    notificacao = Notificacoes.objects.create(user_id = usuario_designado,descricao = descricao,origem_id = request.user.id,readonly = 1)
    return True

#Notifica a entrega do entregável ao solicitante
def enviar_solicitante(request,solicitacao_id,criado_por,origem,entregavel_id):

    descricao = f'''<b>Você recebeu uma nova entrega!</b></br>
                    <b>{request.user.first_name}</b> acabou de te enviar os dados da solicitação!</br></br>
                    Acesse a solicitação clicando <a href='/solicitacoes/visualizar/{solicitacao_id}' target='_blank' )">AQUI</a>.
                    </br><br>
                    Há e não se esqueça, o id do entregável é <b>#{entregavel_id}</b> ! :D      

                    '''
    notificacao = Notificacoes.objects.create(user_id = criado_por,descricao = descricao,origem_id = origem,readonly = 1)
    return True

#Confirma a entrega do solicitante
def confirmar_recebimento(request,solicitacao_id):
    usuarios_notify = Permissoes.objects.all()
    for usuario in usuarios_notify:
        if '12' in usuario.permissao:
            descricao = f'''<b>Demanda Concluída!</b></br>
                            <b>{request.user.first_name}</b> acabou de informar que está tudo certo com a solicitação, e a mesma ja foi recebida!</br></br>
                            Acesse a solicitação clicando <a href='/solicitacoes/visualizar/{solicitacao_id}' target='_blank' >AQUI</a>.
                        '''
            notificacao = Notificacoes.objects.create(user_id = usuario.id,descricao = descricao,origem_id = request.user.id,readonly = 1)
    return True

#Devolve a tarefa para correção
def devolver_correcao_tarefa(request,solicitacao_id,criado_por,origem,entregavel_id):

    descricao = f'''<b>Correção da Solicitação!</b></br>
                    <b>{request.user.first_name}</b> solicitou a correção da solicitação!</br></br>
                    Acesse a solicitação clicando <a href='/solicitacoes/visualizar/{solicitacao_id}' target='_blank' >AQUI</a>.
                    </br><br>
                    Há e não se esqueça, o id do entregável é <b>#{entregavel_id}</b> ! :D      

                    '''
    notificacao = Notificacoes.objects.create(user_id = criado_por,descricao = descricao,origem_id = origem,readonly = 1)
    return True

#Devolve o entregável corrigido a comunicação
def devolver_correcao_entrega(request,solicitacao_id,criado_por,entregavel_id):
    usuarios_notify = Permissoes.objects.all()
    for usuario in usuarios_notify:
        if '12' in usuario.permissao:
            descricao = f'''<b>Entregável Corrigido e Reenviado!</b></br>
                    <b>{request.user.first_name}</b> informou que alterou o entregável e está reenviando novamente!</br></br>
                    Acesse a solicitação clicando <a href='/solicitacoes/visualizar/{solicitacao_id}' target='_blank' >AQUI</a>.
                    </br><br>
                    Há e não se esqueça, o id do entregável é <b>#{entregavel_id}</b>! :D      
                    '''
            notificacao = Notificacoes.objects.create(user_id = usuario.id,descricao = descricao,origem_id = criado_por,readonly = 1)
    return True

#Devolve o entregavel de volta para o solicitante corrigir
def devolver_entregavel_solicitante(request,destinatario,autor,solicitacao_id,entregavel_id):
    descricao = f'''<b>Corrija o Entregável!</b></br>
                <b>{request.user.first_name}</b> solicitou a correção do entregável!</br></br>
                Acesse a solicitação clicando <a href='/solicitacoes/visualizar/{solicitacao_id}' target='_blank' >AQUI</a>.
                </br><br>
                Há e não se esqueça, o id do entregável é <b>#{entregavel_id}</b> ! :D      
                '''
    notificacao = Notificacoes.objects.create(user_id = destinatario,descricao = descricao,origem_id = autor,readonly = 1)
    return True

#Devolve o entregável entregue pela comunicação de volta a comunicação para correção
def devolver_entregavel_comunicacao(request,solicitacao_id,criado_por,entregavel_id):
    usuarios_notify = Permissoes.objects.all()
    for usuario in usuarios_notify:
        if '12' in usuario.permissao:
            descricao = f'''<b>Entrega Incompleta!</b></br>
                    <b>{request.user.first_name}</b> informou que o entregável entregue pela comunicação não está correto e precisa de correções!</br></br>
                    Acesse a solicitação clicando <a href='/solicitacoes/visualizar/{solicitacao_id}' target='_blank' >AQUI</a>.
                    </br><br>
                    Há e não se esqueça, o id do entregável é <b>#{entregavel_id}</b>! :D      
                    '''
            notificacao = Notificacoes.objects.create(user_id = usuario.id,descricao = descricao,origem_id = criado_por,readonly = 1)
    return True

#Devolve o entregavel de volta para o solicitante corrigir
def negar_entregavel_solicitante(request,destinatario,autor,solicitacao_id,entregavel_id):
    descricao = f'''<b>Entregável Negado!</b></br>
                <b>{request.user.first_name}</b> informou que o entregável da solicitação foi negado!</br></br>
                Acesse a solicitação para saber mais clicando <a href='/solicitacoes/visualizar/{solicitacao_id}' target='_blank' >AQUI</a>.
                </br><br>
                Há e não se esqueça, o id do entregável é <b>#{entregavel_id}</b> ! :D      
                '''
    notificacao = Notificacoes.objects.create(user_id = destinatario,descricao = descricao,origem_id = autor,readonly = 1)
    return True