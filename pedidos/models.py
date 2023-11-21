from django.db import models
from loja.models import Produto
from usuarios.models import MeuUser


class Pedido(models.Model):
    cliente = models.ForeignKey(MeuUser, on_delete=models.SET_NULL, null=True, blank=True)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)
    pago = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ('-criado',)

    def __str__(self):
        return f'Pedido {self.id}'

    def get_total(self):
        return sum(item.get_custo() for item in self.itens_pedido.all())


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens_pedido', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, related_name='itens_produto', on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'

    def __str__(self):
        return f'{self.id}'

    def get_custo(self):
        return self.preco * self.quantidade
