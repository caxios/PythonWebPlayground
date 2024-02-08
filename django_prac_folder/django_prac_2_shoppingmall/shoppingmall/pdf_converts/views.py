from django.shortcuts import render
from products.models import Product
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.
def showProducts(request):
    products = Product.objects.all()

    context = {"products":products}

    return render(request, "pdf_converts/showInfo.html", context=context)

def pdf_report_create(request):
    products = Product.objects.all()
    template_path = 'pdf_converts/pdfReport.html'
    context = {"products":products}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="products_report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    #create pdf file
    pisa_status = pisa.CreatePDF(html, dest=response) # dest:destination
    if pisa_status.err:
        return HttpResponse('we had some errors <pre>' + html + '</pre>')
    return response