from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from employee.models import EmployeeProfile


class Register(APIView):
    def get(self, request,):
        return Response({"Register an Fingerprint ": "v1",
        "Instruction             ":"Post the username to register his/her fingerprint",
        "Format                  ":' {"username" :  "sample" }   #remove the forwad slash'})

    def post(self, request,):
        username = request.data.get('username', '')
        user = User.objects.filter(username=username)
        if not user:
            return Response({'success': 'False', 'error': 'username DoesNotExist'})

        employee = EmployeeProfile.objects.filter(user=user[0])
        if not employee:
            return Response({'success': 'False', 'error': 'employee profile DoesNotExist'})
        employee[0].finger_print = True
        employee[0].save()
        return Response({'success': 'True'})


class Punch(APIView):
    def get(self, request):
        return Response({"Register an Fingerprint ": "v1",
        "Instruction             ":"Post the username to register his/her fingerprint",
        "Format                  ": ' {"username" :  "sample" }   #remove the forwad slash'})

    def post(self, request):
        pass
