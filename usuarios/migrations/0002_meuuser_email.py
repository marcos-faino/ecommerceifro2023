# Generated by Django 4.2.4 on 2023-11-15 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meuuser',
            name='email',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]