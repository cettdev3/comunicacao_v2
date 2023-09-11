from django.db import models
from solicitacoes.models import Escolas
from django.contrib.auth.models import User

class Departamentos(models.Model):

    id = models.AutoField(primary_key=True)
    departamento = models.TextField()
    class  Meta:
        db_table = 'departamentos'

# Create your models here.
class Permissoes(models.Model):
    
    id = models.AutoField(primary_key=True)
    permissao = models.TextField(default='')
    unidade = models.ForeignKey(Escolas,on_delete=models.CASCADE)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamentos,on_delete=models.CASCADE)
    class  Meta:
        db_table = 'permissoes'