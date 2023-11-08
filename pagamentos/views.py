from django.shortcuts import render, reverse
from django.urls import reverse_lazy

from django.utils import translation
from django.utils.translation import gettext as _

from ecommerce import settings
from pagamentos.forms import CheckoutForm
from pedidos.models import Pedido
from django.views.generic import TemplateView, FormView
import braintree


class ProcessarPagamento(FormView):
    template_name = 'pagamento/processar.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('pagamento:realizado')

    def dispatch(self, request, *args, **kwargs):
        braintree_env = braintree.Environment.Sandbox
        braintree.Configuration.configure(
            braintree_env,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY
        )
        self.braintree_client_token = braintree.ClientToken.generate({})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['braintree_client_token'] = self.braintree_client_token
        return ctx

    def form_valid(self, form):
        idpedido = self.request.session.get('idpedido')
        pedido = Pedido.objects.get(id=idpedido)
        custo_total = pedido.get_total()
        result = braintree.Transaction.sale({
            'amount': custo_total,
            'payment_method_nonce': form.cleaned_data['payment_method_nonce'],
            'options': {
                'submit_for_settlement': True,
            },
        })
        if result.is_success:
            context = self.get_context_data()
            context['form'] = self.get_form(self.get_form_class())
            context['braintree_error'] = _('Pagamento não processado. Favor verificar os dados.')
            # return self.render_to_response(context)
        return super().form_valid(form)
    """
    def get_success_url(self):
        return reverse('pagamento:realizado')
    """

class PagamentoRealizadoView(TemplateView):
    template_name = 'pagamento/realizado.html'


class PagamentoCanceladoView(TemplateView):
    template_name = 'pagamento/cancelado.html'
