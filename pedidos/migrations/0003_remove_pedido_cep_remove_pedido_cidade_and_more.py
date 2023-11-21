# Generated by Django 4.2.4 on 2023-11-14 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('pedidos', '0002_pedido_cliente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='cep',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='cidade',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='email',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='endereco',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='sobrenome',
        ),
        migrations.AlterField(
            model_name='pedido',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuarios.meuuser'),
        ),
    ]