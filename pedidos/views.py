from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView

from carrinho.carrinho import Carrinho
from pedidos.forms import PedidoModelForm
from .models import ItemPedido, Pedido
from .utils import GeraPdfMixin


class PedidoCreateView(CreateView):
    form_class = PedidoModelForm
    success_url = reverse_lazy('resumopedido')
    template_name = 'formpedido.html'

    def form_valid(self, form):
        car = Carrinho(request=self.request)
        pedido = form.save()
        for item in car:
            ItemPedido.objects.create(pedido=pedido,
                                      produto=item['produto'],
                                      preco=item['preco'],
                                      quantidade=item['quantidade'])
        car.limpar()
        self.request.session['idpedido'] = pedido.id
        return redirect('resumopedido', idpedido=pedido.id)


class ResumoPedidoTemplateView(TemplateView):
    template_name = 'resumopedido.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pedido'] = Pedido.objects.get(id=self.kwargs['idpedido'])
        return ctx

class ResumoPedidoPdf(View, GeraPdfMixin):

    def get(self, request):
        pedido = Pedido.objects.get(id=self.kwargs['idpedido'])
        ctx = self.context_data()
        ctx['pedido'] = pedido
        return self.render_to_pdf('resumopedido.html', ctx)
