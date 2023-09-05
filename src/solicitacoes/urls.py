from django.urls import include, path
from solicitacoes.views import Form_Solicitacoes,Visualizar_Solicitacao,Dados_Gerais_Evento,Ajax_Realiza_Solicitacao


urlpatterns = [
    #path('solicitacoes',  Solicitacoes),
    path('solicitacoes',  Form_Solicitacoes),
    path('solicitacoes/visualizar/<codigo>',  Visualizar_Solicitacao),
    path('ajax/dados-gerais-evento',  Dados_Gerais_Evento),
    path('ajax/realiza-solicitacao',  Ajax_Realiza_Solicitacao),
]