from __future__ import unicode_literals
from django.db import models
from employee.models import Employee
from django.core.exceptions import ValidationError
from .utils import Helper
from core.models import Base

shelper = Helper()


class Attendance(Base):
    employee = models.ForeignKey(Employee)
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
        if helper.time_diff(time_in_am, time_out_am):
            raise ValidationError('Time in and time out difference low')
