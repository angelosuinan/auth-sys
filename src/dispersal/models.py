from __future__ import unicode_literals
from django.db import models
from core.models import Base
from employee.models import Employee


issued_by_default = 1
recieved_by_default = 1


class Item(Base):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    unit = models.IntegerField(blank=False)
    quantity = models.IntegerField(blank=False)
    generic_name = models.TextField(blank=False, default='')
    description = models.TextField(blank=False)
    date_acquired = models.DateField(blank=False)
    amount = models.FloatField(blank=False)
    recieved_by = models.ForeignKey(Employee, on_delete=models.CASCADE,
        related_name='recieved_by', default=recieved_by_default)
    issued_by = models.ForeignKey(Employee, on_delete=models.CASCADE,
        related_name='issued_by', default=issued_by_default)
