# todo/todo_api/serializers.py
from rest_framework import serializers
from solicitacoes.models import Solicitacoes, Tarefas, Entregaveis, Programacao_Adicional
from menu.models import Notificacoes


class Solicitacao_Serializar_git(serializers.ModelSerializer):
    evento_json = serializers.JSONField(required=False)

    class Meta:
        model = Solicitacoes
        fields = ["id",
                  "evento_json",
                  "motivo_alteracao",
                  "tipo_projeto",
                  "publico_evento",
                  "criado_por",
                  "data_solicitacao",
                  "prazo_entrega",
                  "entregaveis_concluidos",
                  "entregaveis_totais",
                  "entregaveis_pendentes",
                  'get_projeto_display',
                  'status',
                  "status_solicitacao",
                  "get_status_display",
                  ]
        depth = 2


class Tarefas_Serializar(serializers.ModelSerializer):
    class Meta:
        model = Tarefas
        fields = [
            "id",
            "entregavel",
            "titulo_tarefa",
            "data_tarefa",
            "prazo_entrega",
            "data_entrega",
            "descricao_tarefa",
            "descricao_entrega",
            "usuario",
            "usuario_designou",
            "prioridade",
            "tipo",
            "get_tipo_display",
            "get_prioridade_display",
            "calcular_status",
            "calcular_status_entrega",
            "status",
            "arquivos",
        ]


class Programacao_Adicional_Serializar(serializers.ModelSerializer):
    class Meta:
        model = Programacao_Adicional
        fields = [
            "id",
            "data",
            "hora",
            "hora_final",
            "atividade",
        ]


class Entregaveis_Serializar(serializers.ModelSerializer):
    tarefas = Tarefas_Serializar(many=True)

    class Meta:
        model = Entregaveis
        fields = [
            "id",
            "evento",
            "prazo",
            "data_solicitacao",
            "exemplo_arte",
            "tipo_entregavel",
            "tipo_produto",
            "categoria_produto",
            "descricao_audio_visual",
            "observacao",
            "criado_por",
            "motivo_revisao",
            "status_entregaveis",
            "status",
            "get_tipoproduto_display",
            "get_tipoentregavel_display",
            "get_status_display",
            "tarefas",
        ]


class Solicitacao_Serializar(serializers.ModelSerializer):
    evento_json = serializers.JSONField(required=False)
    entregaveis = Entregaveis_Serializar(many=True)
    programacao_adicional = Programacao_Adicional_Serializar(many=True)

    class Meta:
        model = Solicitacoes
        fields = [
            "id",
            "evento_json",
            "motivo_alteracao",
            "tipo_projeto",
            "publico_evento",
            "criado_por",
            "data_solicitacao",
            "entregaveis_concluidos",
            "entregaveis_totais",
            "entregaveis_pendentes",
            'get_projeto_display',
            'status',
            "status_solicitacao",
            "get_status_display",
            "entregaveis",
            "programacao_adicional",
        ]


class Simple_Entregaveis_Serializar(serializers.ModelSerializer):

    class Meta:
        model = Entregaveis
        fields = [
            "id",
            "evento",
            "prazo",
            "data_solicitacao",
            "exemplo_arte",
            "tipo_entregavel",
            "tipo_produto",
            "categoria_produto",
            "descricao_audio_visual",
            "observacao",
            "criado_por",
            "motivo_revisao",
            "status_entregaveis",
            "status",
            "get_tipoproduto_display",
            "get_tipoentregavel_display",
            "get_status_display",
        ]


class Simple_Solicitacao_Serializar(serializers.ModelSerializer):
    evento_json = serializers.JSONField(required=False)

    class Meta:
        model = Solicitacoes
        fields = [
            "id",
            "evento_json",
            "motivo_alteracao",
            "tipo_projeto",
            "publico_evento",
            "criado_por",
            "data_solicitacao",
            "entregaveis_concluidos",
            "entregaveis_totais",
            "entregaveis_pendentes",
            'get_projeto_display',
            'status',
            "status_solicitacao",
            "get_status_display",
        ]


class Notificacao_Serializar(serializers.ModelSerializer):
    class Meta:
        model = Notificacoes
        fields = [
            "id",
            "data",
            "user",
            "descricao",
            "origem",
            "readonly",
        ]
