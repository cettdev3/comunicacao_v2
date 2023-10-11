from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [

    path('solicitacoes',
         views.ListSolicitacaoAPIView.as_view()),
    path('entregaveis',
         views.ListEntregavelAPIView.as_view()),
    path('tarefas',
         views.ListTarefaAPIView.as_view()),
    path('programacao-adicional',
         views.ListProgramacaoAdicionalAPIView.as_view()),
    path('notificacoes',
         views.ListNotificacaoAPIView.as_view()),

    path('solicitacoes/<int:pk>',
         views.DetailSolicitacaoAPIView.as_view()),
    path('entregaveis/<int:pk>',
         views.DetailEntregavelAPIView.as_view()),
    path('tarefas/<int:pk>',
         views.DetailTarefaAPIView.as_view()),
    path('programacao-adicional/<int:pk>',
         views.DetailProgramacaoAdicionalAPIView.as_view()),
    path('notificacoes/<int:pk>',
         views.DetailNotificacaoAPIView.as_view()),

    path('solicitacoes/create', views.CreateSolicitacaoAPIView.as_view()),
    path('entregaveis/create', views.CreatEntregavelAPIView.as_view()),
    path('tarefas/create', views.CreateTarefaAPIView.as_view()),
    path('programacao-adicional/create',
         views.CreateProgramacaoAdicionalAPIView.as_view()),
    path('notificacao/create',
         views.CreateNotificacaoAPIView.as_view()),

    path('solicitacoes/update/<int:pk>',
         views.UpdateSolicitacaoAPIView.as_view()),
    path('entregaveis/update/<int:pk>',
         views.UpdateEntregavelAPIView.as_view()),
    path('tarefas/update/<int:pk>',
         views.UpdateTarefaAPIView.as_view()),
    path('programacao-adicional/update/<int:pk>',
         views.UpdateProgramacaoAdicionalAPIView.as_view()),
    path('notificacao/update/<int:pk>',
         views.UpdateNotificacaoAPIView.as_view()),

    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
]
