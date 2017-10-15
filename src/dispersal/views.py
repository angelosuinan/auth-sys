from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import View
from models import Customer, Payment, Invoice
from fish.models import Fish
from datetime import datetime
from reports import Report
from stocks import Stocks
# Create your views here.


class Index(View):
    template_name = 'dispersal/index.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        context = {}
        user = request.user
        invoice_list = Invoice.objects.filter(employee=user).order_by('-pk')

        customer_sort = request.GET.get('customer', '')
        if customer_sort:
            invoice_list = invoice_list.filter(customer__name__icontains=customer_sort)

        order_sort = request.GET.get('order', '')
        if order_sort:
            if order_sort == 'desc':
                invoice_list = invoice_list.order_by('pk')

        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        if start_date and end_date:
            invoice_list = invoice_list.filter(date_acquired__range=[start_date, end_date])

        customers = Customer.objects.all()
        fishes = Fish.objects.all()
        paginator = Paginator(invoice_list, 20)
        page = request.GET.get('page')
        if page is None:
            return redirect('/dispersal?page=1')

        try:
            invoices = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            invoices = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            invoices = paginator.page(paginator.num_pages)

        length = len(invoice_list)
        context['length'] = length
        context['invoices'] = invoices
        context['customers'] = customers
        context['fishes'] = fishes
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request):
        context = {}
        page = request.POST.get('page', '')
        url = '/dispersal?page=' + page + '&'
        customer_name = request.POST.get('customer', '')
        url += 'customer=' + customer_name + '&'
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
    template_name = 'dispersal/add.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request,):
        context = {}
        customers = Customer.objects.all()
        fishes = Fish.objects.all()
        context['customers'] = customers
        context['fishes'] = fishes
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request):
        existing_customer = request.POST.get('existing', '')
        customer = ""
        if existing_customer:
            customer = Customer.objects.get(name=existing_customer)
        else:
            customer = Customer()
            customer.name = request.POST.get('name', '')
            customer.gender = request.POST.get('gender', '')
            customer.address = request.POST.get('address', '')
            customer.telephone = request.POST.get('telephone', '')
            customer.region = request.POST.get('region', '')
            customer.organization = request.POST.get('organization', '')

            customer.save()

        counter = int(request.POST.get('counter', ''))

        first_payment = Payment()
        fish_name = request.POST.get('fish', '')
        fish = Fish.objects.get(name=fish_name)
        first_payment.fish = fish
        first_payment.amount = request.POST.get('amount', '')
        first_payment.quantity = request.POST.get('quantity', '')
        payment = request.POST.get('free', '')
        if not payment:
            payment = None
        first_payment.free = payment
        first_payment.nature = request.POST.get('nature', '')
        first_payment.save()

        invoice = Invoice()
        date_acquired = request.POST.get('date_acquired', '')
        date_acquired = datetime.strptime(date_acquired, "%m/%d/%Y").strftime("%Y-%m-%d")
        invoice.date_acquired = date_acquired
        invoice.remarks = request.POST.get('remarks', '')
        invoice.employee = request.user
        invoice.customer = customer
        invoice.total_price = first_payment.amount
        invoice.save()
        invoice.orders.add(first_payment)

        total_price = float(first_payment.amount)
        for index in range(0, counter+1):
            payment = Payment()
            fish_name = request.POST.get('fish'+str(index), '')

            if fish_name:
                fish = Fish.objects.get(name=fish_name)
                payment.fish = fish
            amount = request.POST.get('amount'+str(index), '')
            if amount:
                payment.amount = float(str(amount))
                total_price += float(str(amount))
            quantity = request.POST.get('quantity'+str(index), '')
            if quantity:
                payment.quantity = quantity

            free = request.POST.get('free'+str(index), '')
            if not free:
                free = None
            payment.free = free
            payment.nature = request.POST.get('nature'+str(index), '')
            if amount and quantity and fish_name:
                payment.save()
                invoice.total_price = total_price
                invoice.orders.add(payment)
                invoice.save()
        return redirect('/dispersal/change?id='+str(invoice.id))


class Change(View):
    template_name = 'dispersal/change.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        context = {}
        key = request.GET.get('id')
        try:
            invoice = Invoice.objects.get(pk=key)
        except ObjectDoesNotExist:
            return redirect('/error')

        context['invoice'] = invoice
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request):
        context = {}
        key = request.GET.get('id')

        remarks = request.POST.get('remarks', '')
        invoice = Invoice.objects.get(pk=key)
        invoice.remarks = remarks
        invoice.save()

        context['invoice'] = invoice
        return redirect('/dispersal/change?id='+key)


class Chart(View):
    template_name = 'dispersal/charts.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        context = {}
        fishes = Fish.objects.all()
        context['fishes'] = fishes

        fishes = request.GET.get('fish', '')
        fishes_list = ''
        if fishes:
            fishes_list = fishes.split(",")
        context['fishes_list'] = fishes_list
        year = request.GET.get('year', None)
        order = request.GET.get('order', '')
        order = 'monthly'

        if year and order and fishes:
            if (len(year) == 0) or (len(order) == 0) or (len(fishes) == 0):
                context['error'] = 'error'
                return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, context)
        report = Report(year, order, fishes_list)

        xaxis = report.get_headers()[:-1]

        context['xaxis'] = xaxis
        queryset = Invoice.objects.all()
        queryset = queryset.filter(date_acquired__year=year)
        field = 'quantity'
        points, average = report.sample(queryset, field)

        scale = request.GET.get('scale', '')
        context['scale'] = average
        if (len(scale) != 0):
            context['scale'] = scale
        context['points'] = points
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request):
        context = {}
        url = '/dispersal/charts?'
        fishes = request.POST.getlist('fish', '')
        _fishes = ''
        for fish in fishes:
            _fishes += fish + ","
        if _fishes:
            _fishes = _fishes[:-1]
        url += 'fish=' + str(_fishes) + '&'
        order = request.POST.get('order', '')
        url += 'order=' + str(order) + '&'
        year = request.POST.get('year', '')
        url += 'year=' + str(year) + '&'
        scale = request.POST.get('scale', '')
        url += 'scale=' + str(scale) + '&'

        if 'export' in request.POST:
            year = request.GET.get('year', '')
            fishes = request.GET.getlist('fish', '')
            _fishes = []
            for fish in fishes:
                _fishes.append(fish)
            _fishes = fishes[0].split(",")

            queryset = Invoice.objects.all()
            order = 'monthly'

            report = Report(year, order, _fishes)
            field = 'quantity'

            queryset = queryset.filter(date_acquired__year=year)
            points, average = report.sample(queryset, field)

            resp = report.parse(points)
            return resp
        return redirect(url)


class Stock(View):
    template_name = 'dispersal/stocks.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        context = {}
        fishes = Fish.objects.all()
        context['fishes'] = fishes

        fish = request.GET.get('fish', '')

        context['fish'] = fish
        year = request.GET.get('year', None)
        order = request.GET.get('order', '')
        order = 'monthly'

        if year and order and fishes:
            if (len(year) == 0) or (len(order) == 0) or (len(fishes) == 0):
                context['error'] = 'error'
                return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, context)
        print Stock
        stocks = Stocks(year, order, fish)

        xaxis = stocks.get_headers()[:-1]

        context['xaxis'] = xaxis

        points, average = stocks.charts()

        scale = request.GET.get('scale', '')
        context['scale'] = average
        if (len(scale) != 0):
            context['scale'] = scale
        context['points'] = points
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request):
        context = {}
        url = '/dispersal/stocks?'
        fish = request.POST.get('fish', '')

        url += 'fish=' + fish + '&'

        year = request.POST.get('year', '')
        url += 'year=' + str(year) + '&'
        scale = request.POST.get('scale', '')
        url += 'scale=' + str(scale) + '&'

        if 'export' in request.POST:
            year = request.GET.get('year', '')
            fish = request.GET.get('fish', '')

            order = 'monthly'
            stocks = Stocks(year, order, fish)
            points, average = stocks.charts()
            resp = stocks.export(points)
            return resp
        return redirect(url)
