from __future__ import unicode_literals
from django.db import models
from core.models import Base
from django.contrib.auth.models import User
import datetime

issued_by_default = 1
recieved_by_default = 1


class Category(Base):
    name = models.CharField(blank=False, default='', max_length=75)

    def __str__(self):
        return self.name


def increment_property_number():
    now = datetime.datetime.now()
    last_item = Item.objects.all().order_by('id').last()
    if not last_item:
        return str(now.year) + "1
    new_item_no = str(now.year) + '-' + str(int(last_item.id) + 1)
    return new_item_no


class Item(Base):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    property_number = models.CharField(max_length=500, default=increment_property_number, null=True, blank=True)
    name = models.CharField(blank=False, default='', max_length=75)
    description = models.TextField(blank=False)
    category = models.ForeignKey(Category)
    quantity = models.IntegerField(blank=False)
    unit = models.CharField(blank=False, max_length=10)
    date_acquired = models.DateField(blank=False)
    amount = models.FloatField(blank=False)
    received_by = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='recieved_by', default=recieved_by_default)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='issued_by', default=issued_by_default)
    remarks = models.TextField(blank=True)
    photo = models.FileField(upload_to='inventory/', blank=True)
