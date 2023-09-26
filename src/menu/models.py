from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Notificacoes(models.Model):
    choice_readonly = [('1','Não Lido'),('2','Lido')]
    id = models.AutoField(primary_key=True)
    data = models.DateTimeField(default=timezone.now,null=True,blank=True)
    user = models.ForeignKey(User,models.CASCADE,null=True,blank=True)
    descricao = models.TextField(null=True,blank=True)
    origem =  models.ForeignKey(User,models.CASCADE,null=True,blank=True, related_name='origem')
    readonly = models.IntegerField(choices=choice_readonly, blank=False, null=False)

    class  Meta:
        db_table = 'notificacoes'