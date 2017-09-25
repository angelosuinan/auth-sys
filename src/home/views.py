from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
# Create your views here.


class Index(View):
    template_name = 'home/index.html'

    def get(self, request,):
        name = request.user
        context = {'user': str(name)}
        if request.user:
            return render(request, self.template_name, context)
        return redirect('/login')


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
            return redirect('/')
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
