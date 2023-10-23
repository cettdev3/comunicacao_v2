from django.urls import include, path
from solicitacoes.views import Form_Solicitacoes,Visualizar_Solicitacao,Dados_Gerais_Evento,Ajax_Realiza_Solicitacao,Ajax_Cria_Tarefa,Ajax_Realiza_Entrega,Ajax_Revisa_Task,Ajax_Devolve_Entregavel,Ajax_Endereco_Escola,Permissoes_usuario,Ajax_Negar_Entregavel,Ajax_Altera_Entregavel,Ajax_Alterar_Entregavel,Ajax_Altera_Solicitacao,Ajax_Alterar_Solicitacao,Ajax_Change_Entregavel,Ajax_Add_Entregavel,Ajax_Reenvia_Entregavel,Ajax_Delete_Files


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
    path('ajax/ajax-alterar-entregavel',  Ajax_Alterar_Entregavel),
    path('ajax/alterar-entregavel',  Ajax_Altera_Entregavel),
    path('ajax/alterar-solicitacao',  Ajax_Alterar_Solicitacao),
    path('ajax/altera-entregavel',  Ajax_Altera_Solicitacao),
    path('ajax/change-entregavel',  Ajax_Change_Entregavel),
    path('ajax/add-entregaveis',  Ajax_Add_Entregavel),
    path('ajax/reenviar-entregavel',  Ajax_Reenvia_Entregavel),
    path('ajax/delete-file',  Ajax_Delete_Files),

]