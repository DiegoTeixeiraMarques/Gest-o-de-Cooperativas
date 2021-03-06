# Generated by Django 2.2.2 on 2020-09-07 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fechamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricula', models.CharField(blank=True, max_length=6, null=True, verbose_name='Matrícula')),
                ('nome', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome')),
                ('funcao', models.CharField(blank=True, max_length=20, null=True, verbose_name='Função')),
                ('meta', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Meta')),
                ('salario', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Salário')),
                ('producaoTotal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Produção Total')),
                ('vrPagoKG', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Vr KG')),
                ('premio', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Prêmio')),
                ('referencia', models.DateField(blank=True, null=True, verbose_name='Referência')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=' Criado em ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name=' Atualizado em ')),
            ],
            options={
                'verbose_name': 'Fechamento',
                'verbose_name_plural': 'Fechamentos',
            },
        ),
    ]
