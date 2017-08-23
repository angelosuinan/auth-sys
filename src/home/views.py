from django.shortcuts import render
from django.views.generic import View
# Create your views here.


class Index(View):
    template_name = 'home/index.html'

    def get(self, request,):
        context = {}
        return render(request, self.template_name, context)
