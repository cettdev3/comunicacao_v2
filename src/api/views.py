from django.shortcuts import render
from rest_framework.views import APIView
from solicitacoes.models import Entregaveis, Solicitacoes, Tarefas, Programacao_Adicional
from . import serializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from datetime import datetime
import json
from django.core.files.storage import FileSystemStorage
from django.forms.models import model_to_dict
from .util import createEntregavel, createTarefa, createSolicitacao, createProgramacao, updateEntregavel, updateSolicitacao, updateTarefa, updateProgramacao, getAllInstances, getSingleInstance


class CreateSolicitacaoAPIView(APIView):
    def post(self, request):
        solicitacaoData = request.data

        if 'entregaveis' not in solicitacaoData or len(solicitacaoData['entregaveis']) is 0:
            return Response(data={"error": "solicitação sem nenhum entregavel"}, status=status.HTTP_400_BAD_REQUEST)

        solicitacao = createSolicitacao(solicitacaoData)

        for entregavelData in solicitacaoData['entregaveis']:
            entregavel = createEntregavel(entregavelData, solicitacao)
            if 'tarefas' in entregavelData and entregavelData['tarefas'] is not []:
                for tarefaData in entregavelData['tarefas']:
                    createTarefa(tarefaData, entregavel)

        if 'programacao_adicional' in solicitacaoData and solicitacaoData['programacao_adicional'] is not []:
            for programacaoData in solicitacaoData['programacao_adicional']:
                createProgramacao(programacaoData, solicitacao)

        serializer = serializers.Solicitacao_Serializar(solicitacao)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CreatEntregavelAPIView(APIView):
    def post(self, request):
        entregavelData = request.data
        entregavel = createEntregavel(entregavelData, None)
        serializer = serializers.Simple_Entregaveis_Serializar(entregavel)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CreateTarefaAPIView(APIView):
    def post(self, request):
        tarefaData = request.data
        tarefa = createTarefa(tarefaData, None)
        serializer = serializers.Tarefas_Serializar(tarefa)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CreateProgramacaoAdicionalAPIView(APIView):
    def post(self, request):
        programacaoAdicionalData = request.data
        programacao = createProgramacao(programacaoAdicionalData, None)
        serializer = serializers.Programacao_Adicional_Serializar(programacao)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UpdateSolicitacaoAPIView(APIView):

    def post(self, request, pk):
        if not Solicitacoes.objects.filter(id=pk).exists():
            return Response(data={"error": f"solicitação de id {pk} inexistente"}, status=status.HTTP_404_NOT_FOUND)
        solicitacaoData = request.data
        solicitacao = updateSolicitacao(solicitacaoData, pk)
        serializer = serializers.Simple_Solicitacao_Serializar(solicitacao)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UpdateEntregavelAPIView(APIView):

    def post(self, request, pk):
        if not Entregaveis.objects.filter(id=pk).exists():
            return Response(data={"error": f"Entregavel de id {pk} inexistente"}, status=status.HTTP_404_NOT_FOUND)
        entregavelData = request.data
        # new_exemplo_arte_file = request.data['new_exemplo_arte']
        entregavel = updateEntregavel(
            entregavelData, pk)
        serializer = serializers.Simple_Entregaveis_Serializar(entregavel)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UpdateTarefaAPIView(APIView):

    def post(self, request, pk):
        if not Tarefas.objects.filter(id=pk).exists():
            return Response(data={"error": f"Tarefa de id {pk} inexistente"}, status=status.HTTP_404_NOT_FOUND)
        tarefaData = request.data
        tarefa = updateTarefa(tarefaData, pk)
        serializer = serializers.Tarefas_Serializar(tarefa)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UpdateProgramacaoAdicionalAPIView(APIView):

    def post(self, request, pk):
        if not Programacao_Adicional.objects.filter(id=pk).exists():
            return Response(data={"error": f"Programação de id {pk} inexistente"}, status=status.HTTP_404_NOT_FOUND)
        programacaoData = request.data
        programacao = updateProgramacao(programacaoData, pk)
        serializer = serializers.Programacao_Adicional_Serializar(programacao)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ListSolicitacaoAPIView(APIView):

    def get(self, request):
        data = getAllInstances(
            model=Solicitacoes, serializerClass=serializers.Solicitacao_Serializar)
        return Response(data=data)


class ListEntregavelAPIView(APIView):

    def get(self, request):
        data = getAllInstances(
            model=Entregaveis, serializerClass=serializers.Entregaveis_Serializar)
        return Response(data=data)


class ListTarefaAPIView(APIView):

    def get(self, request):
        data = getAllInstances(
            model=Tarefas, serializerClass=serializers.Tarefas_Serializar)
        return Response(data=data)


class ListProgramacaoAdicionalAPIView(APIView):

    def get(self, request):
        data = getAllInstances(
            model=Programacao_Adicional, serializerClass=serializers.Programacao_Adicional_Serializar)
        return Response(data=data)


class DetailSolicitacaoAPIView(APIView):

    def get(self, request, pk):
        if not Solicitacoes.objects.filter(id=pk).exists():
            return Response(data={"error": f"solicitação de id {pk} inexistente"}, status=status.HTTP_404_NOT_FOUND)
        data = getSingleInstance(model=Solicitacoes,
                                 serializerClass=serializers.Solicitacao_Serializar, pk=pk)
        return Response(data)


class DetailEntregavelAPIView(APIView):

    def get(self, request, pk):
        if not Entregaveis.objects.filter(id=pk).exists():
            return Response(data={"error": f"Entregavel de id {pk} inexistente"}, status=status.HTTP_404_NOT_FOUND)
        data = getSingleInstance(model=Entregaveis,
                                 serializerClass=serializers.Entregaveis_Serializar, pk=pk)
        return Response(data)


class DetailTarefaAPIView(APIView):

    def get(self, request, pk):
        if not Tarefas.objects.filter(id=pk).exists():
            return Response(data={"error": f"Tarefa de id {pk} inexistente"}, status=status.HTTP_404_NOT_FOUND)
        data = getSingleInstance(model=Tarefas,
                                 serializerClass=serializers.Tarefas_Serializar, pk=pk)
        return Response(data)


class DetailProgramacaoAdicionalAPIView(APIView):

    def get(self, request, pk):
        if not Programacao_Adicional.objects.filter(id=pk).exists():
            return Response(data={"error": f"Programação adicional de id {pk} inexistente"}, status=status.HTTP_404_NOT_FOUND)
        data = getSingleInstance(model=Programacao_Adicional,
                                 serializerClass=serializers.Programacao_Adicional_Serializar, pk=pk)
        return Response(data)
