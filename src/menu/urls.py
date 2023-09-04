from django.urls import path
from . import views

urlpatterns = [
    path('ajax-ler-notificacao',views.marcar_notificacao_lida, name='marcar_notificacao_lida')
]