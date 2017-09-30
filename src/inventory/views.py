from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View
from models import Item


class Index(View):
    template_name = 'inventory/index.html'

    def get(self, request):
        user = request.user
        item_list = Item.objects.filter(employee=user)
        paginator = Paginator(item_list, 20)

        page = request.GET.get('page')
        if page is None:
            return redirect('/inventory?page=1')

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)

        context = {'items': items}
        return render(request, self.template_name, context)


class Add(View):
    template_name = 'inventory/add.html'

    def get(self, request,):
        context = {}
        user = request.user
        employees = User.objects.all()
        context['employees'] = employees
        print employees
        return render(request, self.template_name, context)
