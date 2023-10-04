import weasyprint
from django.http import HttpResponse
from django.template.loader import render_to_string


class GeraPdfMixin:

    def render_to_pdf(self, template, context_dict={}):
        html = render_to_string(template, context_dict)
        response = HttpResponse(content_type='application/pdf')
        weasyprint.HTML(string=html).write_pdf(response,
                                               stylsheets=[])
        return response