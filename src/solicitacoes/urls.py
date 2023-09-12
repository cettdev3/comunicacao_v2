from django.urls import include, path
from solicitacoes.views import Form_Solicitacoes,Visualizar_Solicitacao,Dados_Gerais_Evento,Ajax_Realiza_Solicitacao,Ajax_Cria_Tarefa,Ajax_Realiza_Entrega,Ajax_Revisa_Task,Ajax_Devolve_Entregavel,Ajax_Endereco_Escola,Permissoes_usuario,Ajax_Negar_Entregavel,Ajax_Altera_Entregavel


urlpatterns = [
    #path('solicitacoes',  Solicitacoes),
    path('realizar-solicitacoes',  Form_Solicitacoes),
    path('solicitacoes/visualizar/<codigo>',  Visualizar_Solicitacao),
    path('ajax/dados-gerais-evento',  Dados_Gerais_Evento),
    path('permissoes-acesso',  Permissoes_usuario),
    path('ajax/load-endereco-escola',  Ajax_Endereco_Escola),
    path('ajax/realiza-solicitacao',  Ajax_Realiza_Solicitacao),
    path('ajax/criar-tarefas',  Ajax_Cria_Tarefa),
    path('ajax/ajax-confirmar-entrega',  Ajax_Realiza_Entrega),
    path('ajax/ajax-revisao-task',  Ajax_Revisa_Task),
    path('ajax/ajax-devolver-entregavel',  Ajax_Devolve_Entregavel),
    path('ajax/negar-entregavel',  Ajax_Negar_Entregavel),
    path('ajax/alterar-entregavel',  Ajax_Altera_Entregavel),
]