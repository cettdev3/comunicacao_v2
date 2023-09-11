from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.
class Solicitacoes(models.Model):
    choices_projeto = [('1','EFG'),('2','COTEC'),('3','CETT')]
    choices_status = [('1','Solicitação Criada'),('2','Aguardando Entregas'),('3','Concluída'),('4','Devolvida')]

    id = models.AutoField(primary_key=True)
    evento_json = models.JSONField()
    motivo_alteracao = models.TextField()
    tipo_projeto = models.IntegerField(choices=choices_projeto, blank=False, null=False)
    publico_evento = models.TextField()
    criado_por = models.ForeignKey(User,on_delete=models.CASCADE)
    data_solicitacao = models.DateField(default=timezone.now)
    status = models.IntegerField(choices=choices_status, blank=False, null=False,default=1)


    
    @property
    def status_solicitacao(self):
        total_entregaveis = self.entregaveis_set.exclude(status=4).count()
        if total_entregaveis  > 0 and self.status != 3:
            self.status = 2
            self.save()
        elif total_entregaveis == 0:
            self.status = 3
            self.save()
        else:
            self.status = 1
            self.save()

    
        return  self.status
    

    def get_status_display(self):
        self.status_solicitacao()
        return dict(self.choices_status)[str(self.status)]
    
   

    @property
    def entregaveis_totais(self):
        total_entregaveis = self.entregaveis_set.count()
        return total_entregaveis

    @property
    def entregaveis_concluidos(self):
        entregaveis_concluidos = self.entregaveis_set.filter(status=4).count()
        return entregaveis_concluidos

    @property
    def entregaveis_pendentes(self):
        entregaveis_pendentes = self.entregaveis_set.exclude(status=4).count()
        return entregaveis_pendentes


    def get_projeto_display(self):
        return dict(self.choices_projeto)[str(self.tipo_projeto)]
    
    def get_status_display(self):
        return dict(self.choices_status)[str(self.status)]
    

    
    class  Meta:
        db_table = 'solicitacoes'
    
class Entregaveis(models.Model):
    choices_tipo = [('1','SAVE THE DATE'),('2','DIVULGAÇÃO'),('3','PROGRAMAÇÃO'),('4','STAND')]
    choices_tipo_produto = [('1','DIGITAL'),('2','IMPRESSO'),('3','AUDIOVISUAL'),('4','COBERTURA DE EVENTO'),('5','PRODUÇÃO DE ÁUDIO VISUAL (ORÇAMENTOS E EXECUÇÕES)')]
    choices_status = [('0','AGUARDANDO ENTREGAS'),('1','AGUARDANDO APROVAÇÃO DA COMUNICAÇÃO'),('2','APROVADA PELA COMUNICAÇÃO, AGUARDANDO APROVAÇÃO DO SOLICITANTE'),('3','DEVOLVIDO'),('4','APROVADO PELO SOLICITANTE')]
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

    @property
    def status_entregaveis(self):
        total_tarefas = self.tarefas_set.exclude(status=3).count()
        total_geral_tarefas =  self.tarefas_set.count()

        if total_tarefas  > 0:
            self.status = 0
            self.save()

        elif total_tarefas == 0 and total_geral_tarefas > 0 and self.status == 0:
            self.status = 1
            self.save()

        elif total_tarefas == 0 and total_geral_tarefas > 0 and self.status == 1:
            self.status = 2
            self.save()
        



 

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

class Tarefas(models.Model):
    choices_status = [('0','A FAZER'),('1','FAZENDO'),('2','EM REVISÃO'),('3','FEITO')]
    choices_prioridade = [('1','NORMAL'),('2','PRIORIDADE')]

    id = models.AutoField(primary_key=True)
    entregavel = models.ForeignKey(Entregaveis,models.CASCADE)
    titulo_tarefa = models.TextField()
    data_tarefa = models.DateField(default=timezone.now)
    prazo_entrega = models.DateField()
    data_entrega = models.DateField(null=True,blank=True)
    descricao_tarefa = models.TextField()
    descricao_entrega = models.TextField()
    usuario = models.ForeignKey(User,models.CASCADE)
    usuario_designou = models.ForeignKey(User,models.CASCADE,related_name='usuario_designou')
    prioridade = models.IntegerField(choices=choices_prioridade, blank=False, null=False,default=0)
    tipo = models.IntegerField(choices=choices_prioridade, blank=False, null=False,default=1)
    status = models.IntegerField()

    def calcular_status(self):
        hoje = datetime.now().date()
        prazo = self.prazo_entrega

        if prazo < hoje:
            return "background:#FF0000;color:#FFF"
        elif prazo == hoje:
            return "background:#FFFF00;color:#000"
        elif prazo - hoje <= timedelta(days=3):
            return "background:#FF8C00;color:#000"
        else:
             return "background:#006400;color:#FFF"
        
    def get_prioridade_display(self):
        return dict(self.choices_prioridade)[str(self.prioridade)]
    
    def get_status_display(self):
        return dict(self.choices_status)[str(self.status)]
    
    def get_tipo_display(self):
        return dict(self.choices_tipo)[str(self.tipo)]
    

    class  Meta:
        db_table = 'tarefas'