from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from django.db import models

class User(AbstractUser):
    # Type Choices
    USER_TYPE_CHOICES = (
      (1, 'tutor'),
      (2, 'tech'),
      (3, 'tutor_leader'),
      (4, 'tech_leader'),
    )
    # Información General
    dni = models.CharField(max_length=10)
    phone_number = PhoneNumberField()
    user_type = models.PositiveSmallIntegerField(null=True, choices=USER_TYPE_CHOICES)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.first_name + " " +self.last_name)

class School(models.Model):
    # Type Choices
    WORKDAY_TYPE_CHOICES = (
      (1, 'Matutina'),
      (2, 'Vespertina'),
    )
    # Type Choices
    SECTOR_TYPE_CHOICES = (
      (1, 'Norte'),
      (2, 'Centro'),
      (3, 'Vía a la costa'),
      (4, 'Sur'),
    )
    # Información General
    amie = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    workday = models.PositiveSmallIntegerField(null=True, choices=WORKDAY_TYPE_CHOICES)
    parish = models.CharField(max_length=100)
    sector = models.PositiveSmallIntegerField(null=True, choices=SECTOR_TYPE_CHOICES)
    priority = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # Tutor o Embajador IN o User
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    # Campos de auditoria
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateField() # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación

    def __str__(self):
        return '{}'.format(self.name)

class Requirement(models.Model):
    # Type Choices
    STATE_TYPE_CHOICES = (
      (1, 'Pendiente'),
      (2, 'Atendido'),
      (3, 'Rechazado'),
    )
    # Type Choices
    REQUIREMENT_TYPE_CHOICES = (
      (1, 'Periódica'), # Si el requeimiento fue generado por el teech_leader
      (2, 'Llamada'), # Si el requeimiento fue generado por el teech_leader
      (3, 'Incidencia'), # Si el requerimiento fue generado por el tutor o tutor_leader
    )
    # Información General
    #  Motivo del servicio o requerimiento
    reason = models.CharField(max_length=200)
    state = models.PositiveSmallIntegerField(null=True, choices=STATE_TYPE_CHOICES)
    type = models.PositiveSmallIntegerField(null=True, choices=REQUIREMENT_TYPE_CHOICES)
    # School ID
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    # Tutor o Tutor Leader considerado como EMBAJADOR IN
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # Campos de auditoria
    # Tech Leader, Tutor o Tutor Leader que generó el requerimiento
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateField() # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación

    def __str__(self):
        return '{}'.format(self.reason)

class TechnicalForm(models.Model):
    # Información General
    observations = models.CharField(null=True, max_length=200)

class PedagogicalForm(models.Model):
    # Información General
    observations = models.CharField(null=True, max_length=200)

class Visit(models.Model):
    # Type Choices
    STATE_TYPE_CHOICES = (
      (1, 'Pendiente'),
      (2, 'Realizada'),
      (3, 'No Realizada'),
    )
    #Información General
    date_planned =  models.DateTimeField()
    check_in =  models.DateTimeField(null=True)
    check_out =   models.DateTimeField(null=True)
    coordinates_in = models.CharField(null=True, max_length=100) # longitud + latitud
    coordinates_out = models.CharField(null=True, max_length=100) # longitud + latitud
    observations = models.CharField(null=True, max_length=200)
    state = models.PositiveSmallIntegerField(null=True, choices=STATE_TYPE_CHOICES)
    # ID del requerimieno que generó la visita
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, null=True)
    # Techo, Tutor, Tutor Leader, Tech Leader responsable de realizar la visita
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # School ID
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    # Pedagogical Form ID

    # Technical Form ID

    # Campos de auditoria
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación
