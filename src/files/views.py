from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from annoying.functions import get_object_or_None
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from itertools import chain
from files.models import File
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
        context['files'] = files
        context['extensions'] = file_extensions
        for f, ext in files, file_extensions:
            print f, "ASDASD" , ext
        return render(request, self.template_name, context)
