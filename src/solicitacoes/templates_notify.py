from django.contrib.auth.models import User
from gerir_time.models import Permissoes

#Notifica uma nova solicitação
def nova_notificacao(request,solicitacao_id):
    usuarios_notify = Permissoes.objects.all()
    for usuario in usuarios_notify:
        if '12' in usuario['permissao']:
            descricao = '''<b>Nova Solicitação!</b></br>
                            {request.user.first_name} criou uma nova solicitação!</br></br>
                            Acesse a solicitação clicando <a href='/solicitacoes/visualizar/{solicitacao_id}'>AQUI</a>
                            </br>
                            

                        '''