from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()


# Create your models here.
class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
