from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from core.models import Base
from django.contrib.auth.models import User
from employee.models import EmployeeProfile
from fish.models import Fish
from datetime import datetime


def increment_invoice_number():
    now = datetime.now()
    last_invoice = Invoice.objects.all().order_by('id').last()
    if not last_invoice:
        return 'bfarniftc-'+str(now.year) + str(now.month) + str(now.day) + '1'
    invoice_no = last_invoice.invoice_number
    invoice_int = int(invoice_no.split('BFARNIFTC-')[-1])
    new_invoice_int = last_invoice.id
    new_invoice_no = 'bfarniftc-'+str(now.year) + str(now.month) + str(now.day) + str(new_invoice_int)
    return new_invoice_no


class Customer(Base):
    REGION_CHOICES = (
        ('I', 'REGION I (Ilocos Region)'),
        ('II', 'REGION 2 (Cagayan Valley)'),
        ('III', 'REGION III (Central Luzon)'),
        ('IV-A', 'REGION IV-A (CALABARZON)'),
        ('IV-B', 'REGION IV-B(MIMAROPA)'),
        ('V', 'REGION V(Bicol Region)'),
        ('VI', 'REGION VI (Western Visayas'),
        ('VII', 'REGION VII (Central Visayas'),
        ('VIII', 'REGION VIII (Eastern Visayas)'),
        ('IX', 'REGION IX (Zamboanga Peninsula)'),
        ('X', 'REGION X (Northern Mindanao)'),
        ('XI', 'REGION XI (Davao Region)'),
        ('XII', 'REGION XII (Soccsksargen)'),
        ('XIII', 'REGION XIII (CARAGA)'),
        ('NCR', '(NCR) National Capital Region'),
        ('XIV', 'REGION 14 Cordillera Administrative Region (CAR)'),
        ('XV', 'REGION XV - Autonomous Region in Muslim Mindanao (ARMM)'),
        ('XVIII', 'Region XVIII - NIR - Negros Island Region'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Organization')
    )
    name = models.CharField(max_length=75, blank=False)
    organization = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=100, blank=False)
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default='M',
        verbose_name="Sex"
    )
    telephone = models.CharField(max_length=11, blank=False)
    region = models.CharField(
        max_length=5,
        choices=REGION_CHOICES,
        default='NCR',
    )

    def __str__(self):
        return self.name


class Payment(Base):
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE, related_name="fish_order")
    amount = models.FloatField(max_length=10, blank=False)
    quantity = models.IntegerField(blank=False)
    free = models.IntegerField(blank=True, null=True)
    nature = models.TextField(blank=True, null=True)

    def __str__(self,):
        return 'payment id =' + str(self.id) + ', amount = ' + str(self.amount) + 'php'

    def to_dict(self):
        return {
            'fish': self.fish,
        }


class Invoice(Base):
    invoice_number = models.CharField(max_length=500, default=increment_invoice_number, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer")
    orders = models.ManyToManyField(Payment)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee")
    date_acquired = models.DateField(blank=False)
    total_price = models.FloatField(blank=False)
    remarks = models.TextField(blank=True)
