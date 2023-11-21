from django import forms
from .models import Pedido


class PedidoModelForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = ['cliente']
        raw_id_fields = ('cliente',)

