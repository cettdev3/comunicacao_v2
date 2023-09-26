from django.urls import path
from .views import Notifications,Notificacoes_User,Get_Notifications,Read_Notify

urlpatterns = [
    path('busca-notificacao',  Notifications),
    path('notificacoes',  Notificacoes_User),
    path('get-notifications',  Get_Notifications),
    path('notify-read',  Read_Notify),
]