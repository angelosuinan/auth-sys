from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator


# Create your views here.


class Index(View):
    template_name = 'home/index.html'

    @method_decorator(login_required(login_url='/login'), )
    def get(self, request,):
        name = request.user
        context = {}
        return render(request, self.template_name, context)


class Login(View):
    template_name = 'home/login.html'

    def get(self, request,):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request):
        username = request.POST.get('Username', '')
        password = request.POST.get('Password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            url = request.GET.get('next', '')
            print url
            return redirect(url)
        return redirect('/login')


class Faq(View):
    template_name = 'home/faq.html'

    def get(self, request,):
        context = {}
        return render(request, self.template_name, context)


class Logout(View):
    template_name = 'home/logout.html'

    def get(self, request,):
        logout(request)
        return redirect('/login')


class Error(View):
    template_name = 'home/error.html'

    def get(self, request, ):
        context = {}
        return render(request, self.template_name, context)
