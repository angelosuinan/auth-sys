from __future__ import unicode_literals

from django.db import models
from core.models import Base


class Fish(Base):
    name = models.CharField(max_length=30, blank=False)
    scientific_name = models.CharField(max_length=75, blank=True)
    image = models.ImageField(max_length=150, blank=True)

    def __str__(self):
        return self.name
