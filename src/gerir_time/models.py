from django.db import models
from solicitacoes.models import Escolas
from django.contrib.auth.models import User

# Create your models here.
class Permissoes(models.Model):
    id = models.AutoField(primary_key=True)
    permissao = models.TextField(default='')
    unidade = models.ForeignKey(Escolas,on_delete=models.CASCADE)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    
    class  Meta:
        db_table = 'permissoes'