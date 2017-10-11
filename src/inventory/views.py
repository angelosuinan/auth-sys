from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View
from models import Item
from datetime import datetime


class Index(View):
    template_name = 'inventory/index.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        user = request.user
        item_list = Item.objects.filter(employee=user)

        order_sort = request.GET.get('order', '')
        if order_sort:
            if order_sort == 'desc':
                item_list = item_list.order_by('-pk')

        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        if start_date and end_date:
            item_list = item_list.filter(date_acquired__range=[start_date, end_date])

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
        length = len(item_list)
        context['length'] = length
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request):
        context = {}
        page = request.POST.get('page', '')
        url = '/inventory?page=' + page + '&'
        order = request.POST.get('order', '')
        url += 'order=' + order + '&'
        start_date = request.POST.get('start_date', '')
        try:
            start_date = datetime.strptime(start_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        except ValueError:
            pass
        url += 'start_date=' + start_date + '&'
        end_date = request.POST.get('end_date', '')
        try:
            end_date = datetime.strptime(end_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        except ValueError:
            pass
        url += 'end_date=' + end_date + '&'
        return redirect(url)


class Add(View):
    template_name = 'inventory/add.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request,):
        context = {}
        context['employees'] = self.get_employees(request)
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request,):
        context = {}
        context['employees'] = self.get_employees(request)
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        unit = request.POST.get('unit', '')
        quantity = request.POST.get('quantity', '')
        date_acquired = request.POST.get('date_acquired', '')
        amount = request.POST.get('amount', '')
        issued_by = request.POST.get('issued_by', '')
        received_by = request.POST.get('received_by', '')
        remarks = request.POST.get('remarks', '')
        photo = ''
        for filename, file in request.FILES.iteritems():
            photo = request.FILES[filename]
        received_by = User.objects.get(username=received_by)
        issued_by = User.objects.get(username=issued_by)

        date_acquired = datetime.strptime(date_acquired, "%m/%d/%Y").strftime("%Y-%m-%d")
        item = Item(
            employee=request.user, name=name, description=description,
            unit=unit, quantity=quantity,
            date_acquired=date_acquired, amount=amount, issued_by=issued_by,
            received_by=received_by, remarks=remarks, photo=photo)
        item.save()
        return redirect('/inventory?change='+str(item.pk))

    def get_employees(self, request ):
        user = request.user
        employees = User.objects.all()

        return employees


class Change(View):
    template_name = 'inventory/change.html'

    def process(self, request):
        key = request.GET.get('id')
        try:
            item = Item.objects.get(pk=key)
        except ObjectDoesNotExist:
            return redirect('/error')

        if item.employee != request.user:
            return redirect('/error')
        context = {}
        context['item'] = item
        context['date_acquired'] = str(item.date_acquired)
        context['employees'] = self.get_employees(request)
        return context

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        context = self.process(request)
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request):
        key = request.GET.get('id')
        remarks = request.POST.get('remarks', '')
        photo = ''
        for filename, file in request.FILES.iteritems():
            photo = request.FILES[filename]

        item = Item.objects.get(pk=key)
        item.remarks = remarks
        if photo:
            item.photo = photo
        item.save()
        context = self.process(request)
        return render(request, self.template_name, context)

    def get_employees(self, request):
        user = request.user
        employees = User.objects.all()

        return employees
