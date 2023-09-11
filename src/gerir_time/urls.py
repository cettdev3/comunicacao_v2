from django.urls import include, path
from gerir_time.views import Gerir_time,Ajax_load_unidade,Ajax_load_permissoes


urlpatterns = [
    path('gerir-time',  Gerir_time),
    path('ajax/load-unidade',  Ajax_load_unidade),
    path('ajax/load-permissoes',  Ajax_load_permissoes),
]