from io import BytesIO

import pdfkit
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa


class GeraPdfMixin:

    def render_to_pdf(self, template_end, context_dict={}):
        template = get_template(template_end)
        html = template.render(context_dict)
        result = BytesIO()
        try:
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
            return HttpResponse(result.getvalue(),
                                content_type='application/pdf')
        except Exception as e:
            print(e)
            return None

    """
    def render_to_pdf(self,template, context_dict={}):
        path = b'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path)
        html = render_to_string(request=self.request, template_name=template, context=context_dict)
        # saida = pdfkit.from_url('https://wkhtmltopdf.org/downloads.html', output_path=False, configuration=config)
        saida = pdfkit.from_url('http://127.0.0.1:8000/pedido/resumo/55/', output_path=False, configuration=config)
        response = HttpResponse(content_type='application/pdf', content=saida)
        return response
    """