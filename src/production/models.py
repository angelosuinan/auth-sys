from __future__ import unicode_literals
from django.contrib.auth.models import User
from fish.models import Fish
from django.db import models
from core.models import Base
from employee.models import EmployeeProfile
from fish.models import Fish


class Harvest(Base):
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE,
        related_name="fish_harvest")
    quantity = models.IntegerField(blank=False)
    date_listed = models.DateField(blank=False)
    employee_attended = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True)
