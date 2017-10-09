from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View
from models import Harvest
from fish.models import Fish
from datetime import datetime


class Index(View):
    template_name = 'production/index.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        context = {}
        user = request.user
        harvest_list = Harvest.objects.all()

        fish_sort = request.GET.get('fish', '')
        if fish_sort:
            harvest_list = harvest_list.filter(fish__name__icontains=fish_sort)

        order_sort = request.GET.get('order', '')

        if order_sort:
            if order_sort == 'desc':
                harvest_list = harvest_list.order_by('-pk')

        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        if start_date and end_date:
            harvest_list = harvest_list.filter(date_listed__range=[start_date, end_date])

        fishes = Fish.objects.all()
        paginator = Paginator(harvest_list, 20)
        page = request.GET.get('page', '')
        if page is None:
            return redirect('/production?page=1')

        try:
            harvests = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            harvests= paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            harvests = paginator.page(paginator.num_pages)

        context['harvests'] = harvests
        context['fishes'] = fishes
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request):
        context = {}
        page = request.POST.get('page', '')
        url = '/production?page=' + page + '&'
        fish_name = request.POST.get('fish', '')
        url += 'fish=' + fish_name + '&'
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
    template_name = 'production/add.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        context = {}
        context['fishes'] = Fish.objects.all()
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request,):
        context = {}

        fish_name = request.POST.get('fish', '')
        quantity = request.POST.get('quantity', '')
        date_listed = request.POST.get('date_listed', '')
        remarks = request.POST.get('remarks', '')
        employee = request.user

        fish = Fish.objects.get(name=fish_name)

        date_listed = datetime.strptime(date_listed, "%m/%d/%Y").strftime("%Y-%m-%d")
        harvest = Harvest()
        harvest.fish = fish
        harvest.quantity = quantity
        harvest.date_listed = date_listed
        harvest.remarks = remarks
        harvest.employee_attended = employee
        harvest.save()

        return redirect('/production/change?id='+str(harvest.id))


class Change(View):
    template_name = 'production/change.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        context = {}
        key = request.GET.get('id')
        try:
            harvest = Harvest.objects.get(pk=key)
        except ObjectDoesNotExist:
            return redirect('/error')

        context['harvest'] = harvest
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request):
        context = {}
        key = request.GET.get('id')

        remarks = request.POST.get('remarks', '')
        harvest = Harvest.objects.get(pk=key)
        harvest.remarks = remarks
        harvest.save()

        context['harvest'] = harvest
        return redirect('/production/change?id='+key)


class Chart(View):
    template_name = 'production/charts.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        context = {}

        harvests = Harvest.objects.all()
        context['harvests'] = harvests.filter().order_by('-pk')
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request):
        context = {}
        return render(request, self.template_name, context)
