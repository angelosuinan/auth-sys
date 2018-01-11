from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from annoying.functions import get_object_or_None
from django.utils.decorators import method_decorator
from datetime import datetime
from django.contrib.auth.decorators import login_required
from itertools import chain
from files.models import File, Category
import os
# Create your views here.


class Index(View):
    template_name = 'files/index.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        context = {}
        files = File.objects.all().order_by('pk')
        file_extensions = []
        for file in files:
            filename, file_extension = os.path.splitext(str(file.upload))
            if file_extension:
                file_extensions.append(file_extension)
        context['categories'] = Category.objects.all()
        context['files'] = files
        context['extensions'] = file_extensions
        context['users'] = User.objects.all()
        for f, ext in files, file_extensions:
            print f, "ASDASD" , ext
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        url = "/files?"
        user = request.POST.get('user', '')
        url += 'user=' + user + '&'
        category = request.POST.get('category', '')
        url += 'category=' + category + '&'
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
