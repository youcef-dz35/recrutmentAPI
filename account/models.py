from django.contrib.auth.models import AbstractUser
from django.db import models

from account.managers import CustomUserManager

JOB_TYPE = (
    ('M', "Male"),
    ('F', "Female"),

)

ROLE = (
    ('employer', "Employer"),
    ('employee', "Employee"),
)
civil_status = (
    ('M', "Married"),
    ('S', "single")
)
active = (
    ('yes', "Active"),
    ('no', "Inactive")
)


# this is for the candidate search for the project
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    role = models.CharField(choices=ROLE, max_length=10)
    gender = models.CharField(choices=JOB_TYPE, max_length=1)
    isActive = models.CharField(choices=active, max_length=5, default="yes")
    operate = models.CharField(choices=active, max_length=5, default="yes")
    civil = models.CharField(choices=civil_status, max_length=30, default="Single")

    telephone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=1024, blank=True, null=True)

    zip_code = models.CharField(max_length=12, blank=True, null=True)
    city = models.CharField(max_length=1024, blank=True, null=True)
    image = models.ImageField(null=True, upload_to='media', blank=True)
    is_employee = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    objects = CustomUserManager()


class cv(models.Model):
    name = models.CharField(max_length=1024, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # experience = models.ForeignKey(Experience, related_name='experience', on_delete=models.CASCADE, blank=True, null=True)
    # competence = models.ForeignKey(Competence, related_name='comp' ,on_delete=models.CASCADE, blank=True, null=True)
    # formation = models.ForeignKey(Formation, related_name='formation', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self, experience=None):
        return str(self.name)


class Experience(models.Model):
    name = models.CharField(max_length=15, blank=True, null=True)
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    poste = models.CharField(max_length=1024, blank=True, null=True)
    fonction = models.CharField(max_length=1024, blank=True, null=True)
    entreprise = models.CharField(max_length=1024, blank=True, null=True)
    type_entreprise = models.CharField(max_length=1024, blank=True, null=True)
    description_deposte = models.CharField(max_length=1024, blank=True, null=True)
    cv = models.ForeignKey(cv, related_name='ecv', on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.name)


class Formation(models.Model):
    name = models.CharField(max_length=15, blank=True, null=True)
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    domain = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    etude = models.CharField(max_length=100, blank=True, null=True)
    ecole = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=1024, blank=True, null=True)
    cv = models.ForeignKey(cv, related_name='fcv', on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.etude)


class Competence(models.Model):
    competence = models.CharField(max_length=1024, blank=True, null=True)
    cv = models.ForeignKey(cv, related_name='ccv', on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.competence)


