from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from employee.models import EmployeeProfile
from attendance.models import Attendance
from django.db import IntegrityError
import requests
import datetime


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
        username = request.data.get('username', '')
        employee = EmployeeProfile.objects.filter(user__username=username)

        if not employee:
            return Response({'success': 'False', 'error': 'employee profile DoesNotExist'})
        user = User.objects.filter(username=username)
        today = datetime.date.today()
        new_attendance = Attendance(employee=user[0], date=today)

        try:
            new_attendance.save()
            new_attendance.time_in_am = datetime.datetime.now()
            new_attendance.save()
        except IntegrityError:
            employee_attendance = Attendance.objects.filter(employee=user[0], date=today)[0]
            if employee_attendance.time_out_am is None:
                employee_attendance.time_out_am = datetime.datetime.now().strftime('%H:%M:%S')
                employee_attendance.clean()
                employee_attendance.save()
                return Response({'success': 'True'})
            if employee_attendance.time_in_pm is None:
                employee_attendance.time_in_pm = str(datetime.datetime.now())[11:-7]
                employee_attendance.clean()
                employee_attendance.save()
                return Response({'success': 'True'})
            if employee_attendance.time_out_pm is None:
                employee_attendance.time_out_pm = str(datetime.datetime.now())[11:-7]
                employee_attendance.clean()
                employee_attendance.save()
                return Response({'success': 'True'})
            if employee_attendance.extra_time_in is None:
                employee_attendance.extra_time_in = str(datetime.datetime.now())[11:-7]
                employee_attendance.clean()
                employee_attendance.save()
                return Response({'success': 'True'})
            if employee_attendance.extra_time_out is None:
                employee_attendance.extra_time_out = str(datetime.datetime.now())[11:-7]
                employee_attendance.clean()
                employee_attendance.save()
                return Response({'success': 'True'})
            return Response({'success': 'False', 'error': 'the employee exceeded punch per day'})
        return Response({'success': 'True'})
