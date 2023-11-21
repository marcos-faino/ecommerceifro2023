from django.urls import path
from .views import PedidoCreateView, ResumoPedidoTemplateView, ResumoPedidoPdf

urlpatterns = [
    path('add/<int:id>', PedidoCreateView.as_view(), name='addpedido'),
    path('resumo/<idpedido>/', ResumoPedidoTemplateView.as_view(), name='resumopedido'),
    path('pdf/<idpedido>/', ResumoPedidoPdf.as_view(), name='pedidopdf'),
]