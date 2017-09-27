from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from core.models import Base
from django.contrib.auth.models import User
from employee.models import EmployeeProfile
from fish.models import Fish


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Organization')
)

REGION_CHOICES = (
    ('I', 'REGION I (Ilocos Region) in Luzon'),
    ('II', 'REGION 2 (Cagayan Valley) in Luzon'),
    ('III', 'REGION III (Central Luzon)'),
    ('IV-A', 'REGION IV-A (CALABARZON) Luzon'),
    ('IV-B', 'REGION IV-B(MIMAROPA) 17th region Visayas'),
    ('V', 'REGION V(Bicol Region) Luzon'),
    ('VI', 'REGION VI (Western Visayas'),
    ('VII', 'REGION VII (Central Visayas'),
    ('VIII', 'REGION VIII (Eastern Visayas)'),
    ('IX', 'REGION IX (Zamboanga Peninsula)'),
    ('X', 'REGION X (Northern Mindanao)'),
    ('XI', 'REGION XI (Davao Region)'),
    ('XII', 'REGION XII (Soccsksargen)'),
    ('XIII', 'REGION XIII (CARAGA)'),
    ('NCR', '(NCR) National Capital Region in Luzon'),
    ('XIV', 'REGION 14 Cordillera Administrative Region (CAR) in Luzon'),
    ('XV', 'REGION XV - Autonomous Region in Muslim Mindanao (ARMM)'),
    ('XVIII', 'Region XVIII - NIR - Negros Island Region'),
)


class Customer(Base):
    name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=100, blank=False)
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default='M',
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
    free = models.IntegerField(blank=True)
    nature = models.TextField(blank=True, default='')

    def __str__(self,):
        return 'payment id =' + str(self.id) + ', amount = ' + str(self.amount) + 'php'

    def to_dict(self):
        return {
            'fish': self.fish,
        }


class Invoice(Base):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer")
    orders = models.ManyToManyField(Payment)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee")
    date_acquired = models.DateField(blank=False)
    total_price = models.FloatField(blank=False)
    remarks = models.TextField(blank=True)
