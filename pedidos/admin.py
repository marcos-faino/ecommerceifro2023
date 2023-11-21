from django.contrib import admin

from .models import Pedido, ItemPedido
import csv
import datetime
from django.http import HttpResponse

class ItemPedidoInLine(admin.TabularInline):
    model = ItemPedido
    raw_id_fields = ['produto']


def exportar_para_csv(modeladmin, request, queryset):
    opt = modeladmin.model._meta
    conteudo_disp = f'attachment; filename={opt.verbose_name_plural}.csv'
    resposta = HttpResponse(content_type='text/csv')
    resposta['Content-Disposition'] = conteudo_disp
    writer = csv.writer(resposta)

    fields = [field for field in opt.get_fields() if not \
              field.many_to_many and not field.one_to_many]
    # Escrever a primeira linha das informações do cabeçalho
    writer.writerow([field.verbose_name for field in fields])
    # Escrevendo as linhas de dados
    for obj in queryset:
        data_row = []
        for f in fields:
            value = getattr(obj, f.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return resposta


exportar_para_csv.short_description = 'Exportar para CSV'


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'pago', 'criado', 'atualizado']
    list_filter = ['pago', 'criado', 'atualizado']
    inlines = [ItemPedidoInLine]
    actions = [exportar_para_csv]
