from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from carrinho.carrinho import Carrinho
from pedidos.forms import PedidoModelForm
from usuarios.models import MeuUser
from .models import ItemPedido, Pedido
from .utils import GeraPdfMixin


class PedidoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'pedidos.create.pedido'
    form_class = PedidoModelForm
    success_url = reverse_lazy('resumopedido')
    template_name = 'formpedido.html'

    def form_valid(self, form):
        car = Carrinho(request=self.request)
        print(form.cleaned_data)
        cliente = form.cleaned_data['cliente']
        pedido = form.save(commit=False)
        pedido.cliente = cliente
        pedido.save()
        for item in car:
            ItemPedido.objects.create(pedido=pedido,
                                      produto=item['produto'],
                                      preco=item['preco'],
                                      quantidade=item['quantidade'])
        car.limpar()
        self.request.session['idpedido'] = pedido.id
        return redirect('resumopedido', idpedido=pedido.id)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cliente'] = MeuUser.objects.get(usuario__id=self.kwargs['id'])
        return ctx


class ResumoPedidoTemplateView(TemplateView):
    template_name = 'resumopedido.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pedido'] = Pedido.objects.get(id=self.kwargs['idpedido'])
        return ctx


class ResumoPedidoPdf(View, GeraPdfMixin):

    def get(self, request, idpedido):
        pedido = Pedido.objects.get(id=idpedido)
        ctx = {"pedido": pedido}
        return self.render_to_pdf('resumopedido.html', ctx)
