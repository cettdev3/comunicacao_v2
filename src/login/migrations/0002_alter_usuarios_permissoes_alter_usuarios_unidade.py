# Generated by Django 4.0.6 on 2023-04-25 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacoes', '0003_alter_entregaveis_protocolo_user'),
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='permissoes',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='unidade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='solicitacoes.escolas'),
        ),
    ]
