# Generated by Django 2.2.2 on 2020-11-24 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionario', '0007_delete_remuneracao'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='ativo',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
    ]