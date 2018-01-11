from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from core.models import Base


class Category(Base):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self,):
        return self.name


# Create your models here.
class File(Base):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    category = models.ForeignKey(Category)
    # file will be uploaded to MEDIA_ROOT/uploads
    upload = models.FileField(upload_to='files/')
    remarks = models.TextField(max_length=50, )
