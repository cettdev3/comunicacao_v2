# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import Solicitacoes

class Solicitacao_Serializar(serializers.ModelSerializer):
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
                "entregaveis_concluidos",
                "entregaveis_totais",
                "entregaveis_pendentes",
                'get_projeto_display',
                'status',
                "get_status_display"]
        depth = 2