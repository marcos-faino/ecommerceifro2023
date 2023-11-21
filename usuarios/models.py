from django.contrib.auth import get_user_model
from django.db import models


class MeuUser(models.Model):
    usuario = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    endereco = models.CharField(max_length=255)
    cep = models.CharField(max_length=10)
    cidade = models.CharField(max_length=100)
    email = models.CharField(max_length=200, blank=True)


