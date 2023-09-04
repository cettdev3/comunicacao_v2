from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.
class Solicitacoes(models.Model):
    choices_projeto = [(1,'EFG'),(2,'COTEC'),(3,'CETT')]
    choices_status = [(1,'Solicitação Criada'),(2,'Aguardando Entregas'),(3,'Concluída'),(4,'Devolvida')]

    id = models.AutoField(primary_key=True)
    evento_json = models.JSONField()
    motivo_alteracao = models.TextField()
    tipo_projeto = models.IntegerField(choices=choices_projeto, blank=False, null=False)
    publico_evento = models.TextField()
    criado_por = models.ForeignKey(User,on_delete=models.CASCADE)
    data_solicitacao = models.DateField(default=timezone.now)
    status = models.IntegerField(choices=choices_status, blank=False, null=False)

    def get_projeto_display(self):
        return dict(self.choices_projeto)[str(self.tipo_projeto)]
    
    def get_status_display(self):
        return dict(self.choices_status)[str(self.status)]
    
    
    class  Meta:
        db_table = 'solicitacoes'
    
class Entregaveis(models.Model):
    choices_tipo = [('1','SAVE THE DATE'),('2','DIVULGAÇÃO'),('3','PROGRAMAÇÃO'),('4','STAND')]
    choices_tipo_produto = [('1','DIGITAL'),('2','IMPRESSO'),('3','AUDIOVISUAL'),('4','COBERTURA DE EVENTO'),('5','PRODUÇÃO DE ÁUDIO VISUAL (ORÇAMENTOS E EXECUÇÕES)')]
    choices_status = [('0','AGUARDANDO ENTREGAS'),('1','EM APROVAÇÃO'),('2','EM REVISÃO'),('3','APROVADO PELO CLIENTE')]

    id = models.AutoField(primary_key=True)
    evento = models.ForeignKey(Solicitacoes,on_delete=models.CASCADE)
    prazo = models.DateField()
    data_solicitacao = models.DateField(default=timezone.now)
    exemplo_arte = models.CharField(max_length=255,default='')
    tipo_entregavel = models.IntegerField(choices=choices_tipo, blank=False, null=False)
    tipo_produto = models.IntegerField(choices=choices_tipo_produto, blank=False, null=False)
    categoria_produto = models.CharField(max_length=255,default='')
    descricao_audio_visual = models.TextField()
    observacao = models.TextField()
    criado_por = models.ForeignKey(User,on_delete=models.CASCADE,related_name='criado_por')
    motivo_revisao = models.TextField(default='')
    status = models.IntegerField(choices=choices_status, blank=False, null=False,default=0)

    def get_status_display(self):
        return dict(self.choices_status)[str(self.status)]

    def get_tipoentregavel_display(self):
        return dict(self.choices_tipo)[str(self.tipo_entregavel)]
    
    def get_tipoproduto_display(self):
        return dict(self.choices_tipo_produto)[str(self.tipo_produto)]
    

    
    class  Meta:
        db_table = 'entregaveis'

class Programacao_Adicional(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField()
    hora = models.CharField(max_length=5,default='')
    hora_final = models.CharField(max_length=5,default='')
    atividade = models.CharField(max_length=100,default='')
    solicitacao = models.ForeignKey(Solicitacoes,models.CASCADE)

    class  Meta:
        db_table = 'programacao_adicional'