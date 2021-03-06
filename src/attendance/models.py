from __future__ import unicode_literals
from django.db import models
from employee.models import EmployeeProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .utils import Helper
from core.models import Base
from datetime import timedelta

helper = Helper()


class Attendance(Base):
    LEAVE_CHOICES = (
        ('OB', 'Official Leave'),
        ('SL', 'Sick Leave'),
        ('VL', 'Vacation Leave'),
        ('SIL', 'Service Incentive Leave'),
        ('ML', 'Maternity Leave'),
        ('PL', 'Paternity Leave'),
        ('PAL', 'Parental Leave'),
        ('RL', 'Rehabilitation Leave'),
        ('STL', 'Study Leave'),
    )
    employee = models.ForeignKey(User, )
    date = models.DateField('Date')
    time_in_am = models.TimeField(blank=True, null=True)
    time_out_am = models.TimeField(blank=True, null=True)
    time_in_pm = models.TimeField(blank=True, null=True)
    time_out_pm = models.TimeField(blank=True, null=True)
    extra_time_in = models.TimeField(blank=True, null=True)
    extra_time_out = models.TimeField(blank=True, null=True)
    total_time = models.CharField(max_length=10, blank=True, null=True)
    approved = models.BooleanField(default="False")
    leave_of_absence = models.CharField(
        max_length=3,
        choices=LEAVE_CHOICES, blank=True,
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('employee', 'date')

    def clean(self):
        time_in_am = self.time_in_am
        time_out_am = self.time_out_am
        sum_time = 0
        if time_in_am and time_out_am:
            time_diff = {}
            time_diff = helper.time_diff(time_in_am, time_out_am)

            if time_diff['fail']:
                raise ValidationError('Time in and time out in AM difference is lower than 5 mins')
            else:
                sum_time += time_diff['difference']
        time_in_pm = self.time_in_pm
        time_out_pm = self.time_out_pm
        if time_in_pm and time_out_pm:
            time_diff = helper.time_diff(time_in_pm, time_out_pm)
            if time_diff['fail']:
                raise ValidationError('time in and time_out PM difference is lower than 5 mins')
            else:
                sum_time += time_diff['difference']
        if time_in_pm and time_out_am:
            time_diff = helper.time_diff(time_out_am, time_in_pm )
            if time_diff['fail']:
                raise ValidationError('time in pm and time_out AM difference is lower than 5 mins')
            else:
                sum_time += time_diff['difference']
        extra_time_in = self.extra_time_in
        extra_time_out = self.extra_time_out
        if extra_time_in and extra_time_out:
            time_diff = helper.time_diff(extra_time_in, extra_time_out)
            if time_diff['fail']:
                raise ValidationError('extra time difference lower than 5 mins')
            else:
                sum_time += time_diff['difference']
        self.total_time = str(timedelta(seconds=sum_time))

    def __str__(self):
        return str(self.employee) + " " +str(self.date)
