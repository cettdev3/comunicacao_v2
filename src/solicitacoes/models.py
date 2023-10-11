from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta

# Create your models here.


class Solicitacoes(models.Model):
    choices_projeto = [('1', 'EFG'), ('2', 'COTEC'),('3', 'CETT'), ('4', 'BASILEU')]
    choices_status = [('1', 'Solicitação Criada'), ('2','Aguardando Entregas'), ('3', 'Concluída'), ('4', 'Devolvida')]

    id = models.AutoField(primary_key=True)
    evento_json = models.JSONField(null=True, blank=True)
    motivo_alteracao = models.TextField(null=True, blank=True)
    tipo_projeto = models.IntegerField(
        choices=choices_projeto, blank=False, null=False)
    publico_evento = models.TextField(null=True, blank=True)
    criado_por = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    data_solicitacao = models.DateField(
        default=timezone.now, null=True, blank=True)
    prazo_entrega = models.DateField(null=True, blank=True)
    briefing = models.TextField(null=True, blank=True)
    status = models.IntegerField(
        choices=choices_status, blank=False, null=False, default=1)
    

    @property
    def status_solicitacao(self):
        total_entregaveis = self.entregaveis.exclude(
            status=4).exclude(status=6).count()
        if total_entregaveis > 0 and self.status != 3:
            self.status = 2
            self.save()
        elif total_entregaveis == 0:
            self.status = 3
            self.save()
        else:
            self.status = 1
            self.save()

        return self.status

    def get_status_display(self):
        self.status_solicitacao()
        return dict(self.choices_status)[str(self.status)]

    @property
    def entregaveis_totais(self):
        total_entregaveis = self.entregaveis.exclude(status=6).count()
        return total_entregaveis

    @property
    def entregaveis_concluidos(self):
        print(self.entregaveis)
        entregaveis_concluidos = self.entregaveis.filter(status=4).count()
        print(entregaveis_concluidos)
        return entregaveis_concluidos

    @property
    def entregaveis_pendentes(self):
        entregaveis_pendentes = self.entregaveis.exclude(
            status=4).exclude(status=6).count()
        return entregaveis_pendentes

    def get_projeto_display(self):
        return dict(self.choices_projeto)[str(self.tipo_projeto)]

    def get_status_display(self):
        return dict(self.choices_status)[str(self.status)]

    class Meta:
        db_table = 'solicitacoes'


class Entregaveis(models.Model):
    choices_tipo = [('1', 'SAVE THE DATE'), ('2', 'DIVULGAÇÃO'),
                    ('3', 'PROGRAMAÇÃO'), ('4', 'STAND')]
    choices_tipo_produto = [('1', 'DIGITAL'), ('2', 'IMPRESSO'), ('3', 'AUDIOVISUAL'), ('4', 'COBERTURA DE EVENTO'), (
        '5', 'PRODUÇÃO (ORÇAMENTOS E EXECUÇÕES)'), ('6', 'IDENTIDADE VISUAL'), ('7', 'PLANEJAMENTO'), ('8', 'BRINDES'), ('9', 'COMUNICAÇÃO VISUAL')]
    choices_status = [('0', 'AGUARDANDO ENTREGAS'), ('1', 'AGUARDANDO APROVAÇÃO DA COMUNICAÇÃO'), ('2', 'APROVADA PELA COMUNICAÇÃO, AGUARDANDO APROVAÇÃO DO SOLICITANTE'),
                      ('3', 'DEVOLVIDO'), ('4', 'APROVADO PELO SOLICITANTE'), ('5', 'DEVOLVIDO P/ SOLICITANTE'), ('6', 'NEGADO')]
    id = models.AutoField(primary_key=True)
    evento = models.ForeignKey(Solicitacoes, on_delete=models.CASCADE,
                               null=True, blank=True, related_name='entregaveis')
    prazo = models.DateField(null=True, blank=True)
    data_solicitacao = models.DateField(
        default=timezone.now, null=True, blank=True)
    exemplo_arte = models.CharField(
        max_length=255, default='', null=True, blank=True)
    tipo_entregavel = models.IntegerField(
        choices=choices_tipo, blank=True, null=True)
    tipo_produto = models.IntegerField(
        choices=choices_tipo_produto, blank=True, null=True, default=5)
    categoria_produto = models.CharField(
        max_length=255, default='', null=True, blank=True)
    descricao_audio_visual = models.TextField(
        null=True, blank=True, default='')
    observacao = models.TextField(null=True, blank=True)
    criado_por = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='criado_por', null=True, blank=True)
    motivo_revisao = models.TextField(default='', null=True, blank=True)
    status = models.IntegerField(
        choices=choices_status, blank=True, null=True, default=0)

    @property
    def status_entregaveis(self):
        total_geral_tarefas = self.tarefas.count()
        total_tarefas = self.tarefas.exclude(
            status=3).exclude(status=4).count()

        if total_tarefas > 0:
            self.status = 0
            self.save()

        elif total_tarefas == 0 and total_geral_tarefas > 0 and self.status == 0:
            self.status = 1
            self.save()


 

    def get_status_display(self):
        return dict(self.choices_status)[str(self.status)]

    def get_tipoentregavel_display(self):
        return dict(self.choices_tipo)[str(self.tipo_entregavel)]

    def get_tipoproduto_display(self):

        return dict(self.choices_tipo_produto)[str(self.tipo_produto)]

    class Meta:
        db_table = 'entregaveis'


class Programacao_Adicional(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField(null=True, blank=True)
    hora = models.CharField(max_length=5, default='', null=True, blank=True)
    hora_final = models.CharField(
        max_length=5, default='', null=True, blank=True)
    atividade = models.CharField(
        max_length=100, default='', null=True, blank=True)
    solicitacao = models.ForeignKey(
        Solicitacoes, models.CASCADE, null=True, blank=True, related_name='programacao_adicional')

    class Meta:
        db_table = 'programacao_adicional'


class Tarefas(models.Model):
    choices_status = [('0', 'A FAZER'), ('1', 'FAZENDO'),
                      ('2', 'EM REVISÃO'), ('3', 'FEITO'), ('4', 'ARQUIVADO')]
    choices_prioridade = [('1', 'NORMAL'), ('2', 'PRIORIDADE')]

    id = models.AutoField(primary_key=True)
    entregavel = models.ForeignKey(
        Entregaveis, models.CASCADE, null=True, blank=True, related_name='tarefas')
    titulo_tarefa = models.TextField(null=True, blank=True)
    data_tarefa = models.DateField(default=timezone.now, null=True, blank=True)
    prazo_entrega = models.DateField(null=True, blank=True)
    data_entrega = models.DateField(null=True, blank=True)
    descricao_tarefa = models.TextField(null=True, blank=True)
    descricao_entrega = models.TextField(null=True, blank=True)
    arquivos = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(User, models.CASCADE, null=True, blank=True)
    usuario_designou = models.ForeignKey(
        User, models.CASCADE, related_name='usuario_designou', null=True, blank=True)
    prioridade = models.IntegerField(
        choices=choices_prioridade, blank=False, null=False, default=0)
    tipo = models.IntegerField(
        choices=choices_prioridade, blank=False, null=False, default=1)
    status = models.IntegerField(null=True, blank=True)

    def calcular_status(self):
        hoje = datetime.now().date()
        prazo = self.prazo_entrega

        if prazo < hoje:
            return "background:#FBEFEF;color:#000"
        elif prazo == hoje:
            return "background:#FBFBEF;color:#000"
        elif prazo - hoje <= timedelta(days=3):
            return "background:#F8EFFB;color:#000"
        else:
            return "background:#EFFBEF;color:#000"

    def calcular_status_entrega(self):
        entrega = self.data_entrega
        prazo = self.prazo_entrega
        if entrega:
            if entrega > prazo:
                return "background:#FBEFEF;color:#000"
            else:
                return "background:#EFFBEF;color:#000"
        else:
            return "background:#ffffff;color:#000"

    def get_prioridade_display(self):
        return dict(self.choices_prioridade)[str(self.prioridade)]

    def get_status_display(self):
        return dict(self.choices_status)[str(self.status)]

    class Meta:
        db_table = 'tarefas'

# Create your models here.


class Escolas(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    logradouro = models.CharField(max_length=255, null=True, blank=True)
    cep = models.CharField(max_length=255, null=True, blank=True)
    cidade = models.CharField(max_length=255, null=True, blank=True)
    complemento = models.CharField(max_length=255, default=False, null=False)
    convenio = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'escolas'

# Sinal que será acionado quando um entregável for marcado como concluído


@receiver(post_save, sender=Entregaveis)
def atualizar_status_tarefas(sender, instance, **kwargs):
    if instance.status == '4':
        # Atualiza o status de todas as tarefas relacionadas ao entregável para "concluído"
        Tarefas.objects.filter(entregavel_id=instance.id).update(status=4)
