from django.shortcuts import render
from django.views.generic import View
# Create your views here.


class Add(View):
    template_name = 'dispersal/add.html'

    def get(self, request,):
        context = {}
        return render(request, self.template_name, context)
