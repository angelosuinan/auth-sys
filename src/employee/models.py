from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(blank=False, default="", max_length=30)
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default='M',
    )
    address = models.CharField(max_length=150,)
    contact_number = models.CharField(max_length=11)
    finger_print = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='employee/', max_length=250, blank=True, null=True)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def __str__(self):
        print self.user
        return str(self.user) + " " + self.position


class OjtProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(blank=False, default="", max_length=30)
    required_hours = models.CharField(blank=False, default="", max_length=30)
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default='M',
    )
    address = models.CharField(max_length=50,)
    contact_number = models.CharField(max_length=11)
    finger_print = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='employee/', max_length=250, blank=True, null=True)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
