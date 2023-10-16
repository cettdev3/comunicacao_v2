from django.urls import path
from .views import Notifications,Notificacoes_User,Get_Notifications,Read_Notify,Send_Notify,Read_Notification

urlpatterns = [
    path('busca-notificacao',  Notifications),
    path('notificacoes',  Notificacoes_User),
    path('get-notifications',  Get_Notifications),
    path('notify-read',  Read_Notify),
    path('notify-send',  Send_Notify),
    path('read-notifications',  Read_Notification),
]