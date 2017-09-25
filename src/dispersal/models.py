from __future__ import unicode_literals
from django.db import models
from core.models import Base
from employee.models import EmployeeProfile
from fish.models import Fish


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class Payment(Base):
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE, related_name="fish_order")
    amount = models.FloatField(max_length=10, blank=False)
    quantity = models.IntegerField(blank=False)
    free = models.BooleanField(default=False)
    nature = models.TextField(blank=True, default='')


    def __str__(self,):
        return 'payment id =' + str(self.id) + ', amount = ' + str(self.amount) + 'php'

    def to_dict(self):
        return {
            'fish': self.fish,
        }


class Invoice(Base):
    orders = models.ManyToManyField(Payment)
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="employee")
    date_acquired = models.DateField(blank=False)
    customer_name = models.CharField(blank=False, max_length=30)
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default='M',
    )
    address = models.CharField(max_length=50, blank=False)
    telephone = models.CharField(max_length=11, blank=False)
    region = models.CharField(max_length=20, blank=False)
    remarks = models.TextField(blank=True)
