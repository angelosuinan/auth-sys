from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


class Employee(models.Model):
    user = models.OneToOneField(User, related_name="user")
    position = models.CharField(blank=False, default="", max_length=30)
    address = models.CharField(max_length=50,)
    contact_number = models.CharField(max_length=11)
    finger_print = models.BooleanField(default=False)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
