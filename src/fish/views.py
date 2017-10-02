from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from models import Fish


class Index(View):
    template_name = "fish/index.html"

    def get(self, request):
        context = {}

        fishes = Fish.objects.all()
        context['fishes'] = fishes
        return render(request, self.template_name, context)
