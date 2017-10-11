from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from models import Attendance
from datetime import datetime
# Create your views here.


class Index(View):
    template_name = 'attendance/index.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request,):
        user = request.user
        attendance_list = Attendance.objects.filter(employee=user)

        order_sort = request.GET.get('order', '')

        if order_sort:
            if order_sort == 'desc':
                attendance_list = attendance_list.order_by('-pk')

        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        if start_date and end_date:
            attendance_list = attendance_list.filter(date__range=[start_date, end_date])

        paginator = Paginator(attendance_list, 20)
        page = request.GET.get('page')
        if page is None:
            return redirect('/attendance?page=1')

        try:
            attendances = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            attendances = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            attendances = paginator.page(paginator.num_pages)

        context = {'attendances':attendances}
        length = len(attendance_list)
        context['length'] = length
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request):
        context = {}
        page = request.POST.get('page', '')
        url = '/attendance?page=' + page + '&'
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


class Change(View):
    template_name = 'attendance/change.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request,):
        context = {}
        key = request.GET.get('id')
        try:
            attendance = Attendance.objects.get(pk=key)
        except ObjectDoesNotExist:
            return redirect('/error')

        if attendance.employee != request.user:
            return redirect('/error')
        context['attendance'] = attendance
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request,):
        context = {}
        key = request.GET.get('id')
        try:
            attendance = Attendance.objects.get(pk=key)
        except ObjectDoesNotExist:
            return redirect('/error')

        if attendance.employee != request.user:
            return redirect('/error')

        notes = request.POST.get('notes', '')
        attendance.notes = notes
        print attendance.notes
        attendance.save()

        return redirect('/attendance/change?id='+key)
