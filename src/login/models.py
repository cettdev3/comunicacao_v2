from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Usuarios(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    permissoes = models.CharField(max_length=255,default=None,null=True)

    class  Meta:
        db_table = 'usuarios'