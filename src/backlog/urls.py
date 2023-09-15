from django.urls import include, path
from .views import Backlog,Ajax_View_Task,Ajax_Move_Task,Ajax_Edit_Task,Ajax_Altera_Task,Ajax_Task_For_Task

urlpatterns = [
    path('minhas-tarefas',  Backlog),
    path('ajax/view-task',  Ajax_View_Task),
    path('ajax/move-task',  Ajax_Move_Task),
    path('ajax/edit-task',  Ajax_Edit_Task),
    path('ajax/realiza-alteracao-task',  Ajax_Altera_Task),
    path('ajax/view-task-ftask',  Ajax_Task_For_Task),
    

]