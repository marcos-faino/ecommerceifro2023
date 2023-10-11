from django.urls import path
from .views import PedidoCreateView, ResumoPedidoTemplateView, ResumoPedidoPdf

urlpatterns = [
    path('add/', PedidoCreateView.as_view(), name='addpedido'),
    path('resumo/<idpedido>/', ResumoPedidoTemplateView.as_view(), name='resumopedido'),
    path('<idpedido>/pdf/', ResumoPedidoPdf.as_view(), name='pedidopdf'),
]