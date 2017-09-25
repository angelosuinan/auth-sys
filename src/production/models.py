from __future__ import unicode_literals
from employee.models import EmployeeProfile
from fish.models import Fish
from django.db import models
from core.models import Base


class Harvest(Base):
    date_listed = models.DateField(blank=False)
    employee_attended = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="employee_attended")
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE, related_name="fish_harvest")
    quantity = models.IntegerField(blank=False)
