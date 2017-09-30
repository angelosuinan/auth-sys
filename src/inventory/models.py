from __future__ import unicode_literals
from django.db import models
from core.models import Base
from django.contrib.auth.models import User


issued_by_default = 1
recieved_by_default = 1


class Item(Base):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(blank=False, default='', max_length=75)
    description = models.TextField(blank=False)
    unit = models.IntegerField(blank=False)
    quantity = models.IntegerField(blank=False)
    date_acquired = models.DateField(blank=False)
    amount = models.FloatField(blank=False)
    recieved_by = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='recieved_by', default=recieved_by_default)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='issued_by', default=issued_by_default)
    remarks = models.TextField(blank=True)
