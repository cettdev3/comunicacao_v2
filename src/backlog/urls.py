from django.urls import include, path
from .views import Backlog,Ajax_View_Task,Ajax_Move_Task

urlpatterns = [
    path('backlog',  Backlog),
    path('ajax/view-task',  Ajax_View_Task),
    path('ajax/move-task',  Ajax_Move_Task),
    

]