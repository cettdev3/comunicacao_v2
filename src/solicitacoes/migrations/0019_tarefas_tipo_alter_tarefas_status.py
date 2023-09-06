# Generated by Django 4.2.2 on 2023-09-05 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacoes', '0018_alter_entregaveis_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarefas',
            name='tipo',
            field=models.IntegerField(choices=[('1', 'NORMAL'), ('2', 'PRIORIDADE')], default=0),
        ),
        migrations.AlterField(
            model_name='tarefas',
            name='status',
            field=models.IntegerField(choices=[('1', 'NORMAL'), ('2', 'REVISÃO')], default='0'),
        ),
    ]
