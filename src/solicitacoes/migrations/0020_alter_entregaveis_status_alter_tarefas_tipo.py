# Generated by Django 4.0.6 on 2023-09-06 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacoes', '0019_tarefas_tipo_alter_tarefas_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entregaveis',
            name='status',
            field=models.IntegerField(choices=[('0', 'AGUARDANDO ENTREGAS'), ('1', 'AGUARDANDO APROVAÇÃO DA COMUNICAÇÃO'), ('2', 'APROVADA PELA COMUNICAÇÃO, AGUARDANDO APROVAÇÃO DO SOLICITANTE'), ('3', 'DEVOLVIDA'), ('4', 'APROVADO PELO SOLICITANTE')], default=0),
        ),
        migrations.AlterField(
            model_name='tarefas',
            name='tipo',
            field=models.IntegerField(choices=[('1', 'NORMAL'), ('2', 'PRIORIDADE')], default=1),
        ),
    ]
