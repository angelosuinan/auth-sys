from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from models import Attendance
# Create your views here.


class Index(View):
    template_name = 'attendance/index.html'

    def get(self, request,):
        user = request.user
        attendance_list = Attendance.objects.filter(employee=user)
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
        return render(request, self.template_name, context)


class Change(View):
    template_name = 'attendance/change.html'

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
