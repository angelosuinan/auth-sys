from django.shortcuts import render
from django.views.generic import View
from models import Customer
# Create your views here.


class Index(View):
    template_name = 'dispersal/index.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class Add(View):
    template_name = 'dispersal/add.html'

    def get(self, request,):
        context = {}
        customers = Customer.objects.all()
        context['customers'] = customers
        return render(request, self.template_name, context)
