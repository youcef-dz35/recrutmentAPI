from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


# Create your models here.


class EmployerProfile(models.Model):
    # User = User.objects.filter(role="employer")
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)


User = get_user_model()


class EmployeeProfile(models.Model):
    # User =User.objects.filter(role="employee")
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
