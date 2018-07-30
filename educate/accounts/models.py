from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

class User(AbstractUser):
    dni = models.CharField(max_length=10)
    phone_number = PhoneNumberField()

    USER_TYPE_CHOICES = (
      (1, 'tutor'),
      (2, 'tech'),
      (3, 'tutor_leader'),
      (4, 'tech_leader'),
    )

    user_type = models.PositiveSmallIntegerField(null=True, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return '{}'.format(self.first_name + " " +self.last_name)

class Workday(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.name)

class Sector(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.name)

class School(models.Model):
    #Información General
    amie = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    workday = models.ForeignKey(Workday, on_delete=models.CASCADE)
    parish = models.CharField(max_length=100)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    priority = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField()
    date_updated = models.DateField(null=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    #Tutor o Embajador IN o User
    #Cambiar por una instancia de Usuario para Tutor
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
