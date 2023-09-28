from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Solicitacoes)
admin.site.register(models.Entregaveis)
admin.site.register(models.Tarefas)
admin.site.register(models.Programacao_Adicional)
