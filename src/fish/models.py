from __future__ import unicode_literals

from django.db import models
from core.models import Base


class Category(Base):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self,):
        return self.name


class Fish(Base):
    name = models.CharField(max_length=50, blank=False, unique=True)
    scientific_name = models.CharField(max_length=75, blank=True)
    image = models.FileField(upload_to='fish/', blank=True, null=True)
    cost_multiplier = models.FloatField(blank=False, default=1)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.name
