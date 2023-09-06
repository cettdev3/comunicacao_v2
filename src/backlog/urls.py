from django.urls import include, path
from .views import Backlog

urlpatterns = [
    path('backlog',  Backlog),
    

]