# Generated by Django 4.0.6 on 2023-09-11 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerir_time', '0005_permissoes_departamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissoes',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gerir_time.departamentos'),
        ),
    ]
