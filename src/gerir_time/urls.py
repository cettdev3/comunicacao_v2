from django.urls import include, path
from gerir_time.views import Gerir_time,Ajax_load_unidade,Ajax_load_permissoes,Cadastrar_usuario,Ajax_load_usuario,Edita_usuario


urlpatterns = [
    path('gerir-time',  Gerir_time),
    path('cadastrar-usuario',  Cadastrar_usuario),
    path('ajax/load-unidade',  Ajax_load_unidade),
    path('ajax/load-usuario',  Ajax_load_usuario),
    path('editar-usuario',  Edita_usuario),
    path('ajax/load-permissoes',  Ajax_load_permissoes),
]