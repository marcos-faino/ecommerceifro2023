from io import BytesIO
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import render_to_string, get_template


class GeraPdfMixin:

    def render_to_pdf(self, template, context_dict={}):
        temp = get_template(template)
        html = temp.render(context_dict)
        result = BytesIO()
        try:
            pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
            return HttpResponse(content=result.getvalue(),
                                content_type='application/pdf')
        except Exception as e:
            print(e)
            return None
