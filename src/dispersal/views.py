from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import View
from models import Customer, Payment, Invoice

from fish.models import Fish
# Create your views here.


class Index(View):
    template_name = 'dispersal/index.html'

    def get(self, request):
        context = {}
        user = request.user
        invoice_list = Invoice.objects.filter(employee=user)
        paginator = Paginator(invoice_list, 20)

        page = request.GET.get('page')
        if page is None:
            return redirect('/invoice?page=1')

        try:
            invoices = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            invoices = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            invoices = paginator.page(paginator.num_pages)

        context['invoices'] = invoices
        return render(request, self.template_name, context)


class Add(View):
    template_name = 'dispersal/add.html'

    def get(self, request,):
        context = {}
        customers = Customer.objects.all()
        fishes = Fish.objects.all()
        context['customers'] = customers
        context['fishes'] = fishes
        return render(request, self.template_name, context)

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
            customer.save()

        counter = int(request.POST.get('counter', ''))
        print counter
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
        invoice.date_acquired = request.POST.get('date_acquired', '')
        invoice.remarks = request.POST.get('remarks', '')
        invoice.employee = request.user
        invoice.customer = customer
        invoice.total_price = 0
        invoice.save()
        total_price = 0
        for index in range(0, counter+1):
            payment = Payment()
            fish_name = request.POST.get('fish'+str(index), '')

            if fish_name:
                fish = Fish.objects.get(name=fish_name)
                payment.fish = fish
            amount = request.POST.get('amount'+str(index), '')
            if amount:
                payment.amount = float(amount)
                total_price += float(amount)
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
        return redirect('/dispersal')
