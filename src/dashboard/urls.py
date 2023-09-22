from django.urls import include, path
from dashboard.views import Dashboard,Filter,Filter_Concluido

urlpatterns = [
    path('solicitacoes',  Dashboard),
    path('filter-project',  Filter,name='filter-project'),
    path('filter-project-concluido',  Filter_Concluido,name='filter-project'),
]