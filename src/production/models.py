from __future__ import unicode_literals
from django.contrib.auth.models import User
from fish.models import Fish
from django.db import models
from core.models import Base
from employee.models import EmployeeProfile
from fish.models import Fish


class AreaHarvested(Base):
    name = models.CharField(max_length=25, blank=False)

    def __str__(self,):
        return self.name


class Harvest(Base):
    fish = models.ForeignKey(Fish, related_name="fish_harvest")
    quantity = models.IntegerField(blank=False)
    date_listed = models.DateField(blank=False)
    area_harvested = models.ForeignKey(AreaHarvested, blank=True, null=True)
    employee_attended = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Employee Assisted")
    remarks = models.TextField(blank=True)
