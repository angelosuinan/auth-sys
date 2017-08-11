from __future__ import unicode_literals
from django.db import models
from employee.models import Employee
from django.core.exceptions import ValidationError
from .utils import Helper

helper = Helper()


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    time_in_am = models.TimeField(blank=True, null=True)
    time_out_am = models.TimeField(blank=True, null=True)
    time_in_pm = models.TimeField(blank=True, null=True)
    time_out_pm = models.TimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('employee', 'date')

    def clean(self):
        time_in_am = self.time_in_am
        time_out_am = self.time_out_am
        print helper.time_diff(time_in_am, time_out_am)
        if helper.time_diff(time_in_am, time_out_am):
            raise ValidationError('Time_in and time_out difference low')
