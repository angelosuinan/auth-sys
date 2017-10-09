from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from models import EmployeeProfile, OjtProfile
from annoying.functions import get_object_or_None
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from itertools import chain

# Create your views here.


class Index(View):
    template_name = 'employee/index.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        context = {}

        emp_profiles = EmployeeProfile.objects.all().order_by('pk')
        ojt_profiles = OjtProfile.objects.all().order_by('pk')
        profiles = list(chain(emp_profiles, ojt_profiles))
        context['profiles'] = profiles
        return render(request, self.template_name, context)


class Profile(View):
    template_name = 'employee/profile.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        context = {}
        pk = request.GET.get('q')
        if pk is None:
            pk = str(request.user.id)
            return redirect('/employee/profile?q='+pk)
        user = User.objects.get(pk=pk)
        context['get_user'] = user

        profile= get_object_or_None(EmployeeProfile, user=user)
        if profile is None:
            profile = get_object_or_None(OjtProfile, user=user)
        if profile is None:
            return redirect('/error')
        context['profile'] = profile

        return render(request, self.template_name, context)


class Change(View):
    template_name = 'employee/change.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        context = {}
        pk = request.GET.get('q')
        if pk is None:
            pk = str(request.user.id)
            return redirect('/employee/change?q='+pk)

        user = User.objects.get(pk=pk)
        context['get_user'] = user

        if user != request.user:
            return redirect('/error')

        profile = get_object_or_None(EmployeeProfile, user=user)
        if profile is None:
            profile = get_object_or_None(OjtProfile, user=user)
            context['type'] = 'ojt'
        if profile is None:
            return redirect('/error')
        context['profile'] = profile

        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request):
        pk = request.GET.get('q')
        user = User.objects.get(pk=pk)

        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        contact_number = request.POST.get('contact_number')
        user_type = request.POST.get('type')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        profile = EmployeeProfile.objects.get(user=user)
        if user_type == 'ojt':
            profile = OjtProfile()
        profile.address = address
        profile.contact_number = contact_number
        profile.save()

        url = '/employee/profile?q='+pk
        return redirect(url)


class Password(View):
    template_name = 'employee/password.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request):
        context = {}
        pk = request.GET.get('q')
        if pk is None:
            return redirect('/employee/password?q='+pk)
            pk = str(request.user.id)

        user = User.objects.get(pk=pk)
        context['get_user'] = user

        if user != request.user:
            return redirect('/error')

        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='/login'), )
    def post(self, request):
        context = {}
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        user = request.user

        if user.check_password(current_password):
            user.set_password(new_password)
        else:
            return render(request, self.template_name, context)
        return render(request, self.template_name, context)
