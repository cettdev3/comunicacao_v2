from django.urls import include, path
from .views import Tasks

urlpatterns = [
    path('tarefas',  Tasks),
    

]