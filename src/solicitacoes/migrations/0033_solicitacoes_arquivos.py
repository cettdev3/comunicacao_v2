# Generated by Django 4.0.6 on 2023-10-23 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacoes', '0032_solicitacoes_briefing_alter_entregaveis_evento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitacoes',
            name='arquivos',
            field=models.TextField(blank=True, null=True),
        ),
    ]
