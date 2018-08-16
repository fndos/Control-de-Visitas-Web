from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.db import models

class Sector(models.Model):
    # Información General
    name = models.CharField(max_length=100)
    # Campos de auditoria
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        db_table = 'sector'

class User(AbstractUser):
    # Type Choices
    USER_TYPE_CHOICES = (
      (1, 'Tutor'),
      (2, 'Técnico'),
      (3, 'Tutor Líder'),
      (4, 'Técnico Líder'),
    )
    # Información General
    dni = models.CharField(max_length=10, unique=True)
    phone_number = PhoneNumberField()
    user_type = models.PositiveSmallIntegerField(null=True, choices=USER_TYPE_CHOICES)
    sector = models.ManyToManyField(Sector)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.first_name + " " + self.last_name)

    class Meta:
        db_table = 'user'

class School(models.Model):
    # Type Choices
    WORKDAY_TYPE_CHOICES = (
      (1, 'Matutina'),
      (2, 'Vespertina'),
      (3, 'Matutina/Vespertina'),
    )
    # Type Choices
    PRIORITY_TYPE_CHOICES = (
      (1, 'No'),
      (2, 'Si'),
    )
    # Información General
    amie = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    workday = models.PositiveSmallIntegerField(null=True, choices=WORKDAY_TYPE_CHOICES)
    parish = models.CharField(max_length=100)
    priority = models.PositiveSmallIntegerField(null=True, choices=PRIORITY_TYPE_CHOICES)
    ambassador_in = models.CharField(max_length=100)
    # Escuelas agrupadas por sectores o zonas
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    # Campos de auditoria
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        db_table = 'school'

class Requirement(models.Model):
    # Type Choices
    STATE_TYPE_CHOICES = (
      (1, 'Pendiente'),
      (2, 'Atendido'),
      (3, 'Rechazado'),
    )
    # Type Choices
    REQUIREMENT_TYPE_CHOICES = (
      (1, 'Periódica'), # Si el requeimiento fue generado por el tech_leader
      (2, 'Llamada'), # Si el requeimiento fue generado por el tech_leader
      (3, 'Incidencia'), # Si el requerimiento fue generado por el tutor o tutor_leader
    )
    # Información General
    #  Motivo del servicio o requerimiento
    reason = models.TextField()
    type = models.PositiveSmallIntegerField(null=True, choices=REQUIREMENT_TYPE_CHOICES)
    # School ID
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    # Usuario que generó el requerimiento (created_by)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # Campos de auditoria
    # Tech Leader, Tutor o Tutor Leader que generó el requerimiento
    state = models.PositiveSmallIntegerField(null=True, choices=STATE_TYPE_CHOICES, default=1)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación

    def __str__(self):
        return '{}'.format(self.reason)

    class Meta:
        db_table = 'requirement'

class Visit(models.Model):
    # Type Choices
    STATE_TYPE_CHOICES = (
      (1, 'Pendiente'),
      (2, 'Realizada'),
      (3, 'No Realizada'),
    )
    # Type Choices
    VISIT_TYPE_CHOICES = (
      (1, 'Pedagógica'),
      (2, 'Técnica'),
      (3, 'Ambas'),
    )
    #Información General
    date_planned =  models.DateTimeField()
    check_in =  models.DateTimeField(null=True)
    check_out =   models.DateTimeField(null=True)
    coordinates_lat_in = models.CharField(null=True, max_length=100) # latitud
    coordinates_lon_in = models.CharField(null=True, max_length=100) # longitud
    coordinates_lat_out = models.CharField(null=True, max_length=100) # latitud
    coordinates_lon_out = models.CharField(null=True, max_length=100) # longitud
    type = models.PositiveSmallIntegerField(null=True, choices=VISIT_TYPE_CHOICES)
    observation = models.TextField(null=True)
    # ID del requerimieno que generó la visita
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, null=True)
    # Techo, Tutor, Tutor Leader, Tech Leader responsable de realizar la visita
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # Pedagogical Form ID
    # Technical Form ID
    # Campos de auditoria
    state = models.PositiveSmallIntegerField(null=True, choices=STATE_TYPE_CHOICES)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación

    def save(self, *args, **kwargs):
        try:
            requirement = Requirement.objects.get(id=self.requirement.id)
            requirement.state = 2 # Estado Atendido
            requirement.save()
        except Exception as e:
            print (e)

        super(Visit, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        try:
            requirement = Requirement.objects.get(id=self.requirement.id)
            requirement.state = 2 # Estado Atendido
            requirement.save()
        except Exception as e:
            print (e)

        super(Visit, self).update(*args, **kwargs)

    def delete(self):
        try:
            requirement = Requirement.objects.get(id=self.requirement.id)
            requirement.state = 1 # Estado Pendiente
            requirement.save()
        except Exception as e:
            print (e)

        super(Visit, self).delete()

    class Meta:
        db_table = 'visit'

class Activity(models.Model):
    # Información General
    name = models.CharField(max_length=100)
    description = models.CharField(null=True, max_length=100)
    # Campos de auditoria
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        db_table = 'activity'


class TechnicalForm(models.Model):
    # Type Choices
    STATE_TYPE_CHOICES = (
      (1, 'En progreso'),
      (2, 'Finalizado')
    )
    #Información General
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    action_taken = models.CharField(max_length=100)
    observation = models.TextField(null=True)
    activity = models.ManyToManyField(Activity)
    # Campos de auditoria
    state = models.PositiveSmallIntegerField(null=True, choices=STATE_TYPE_CHOICES, default=1)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación

    class Meta:
        db_table = 'technical_form'

class DataApciAcademico(models.Model):
    #Información General
    no_prof_capacitados = models.IntegerField()
    minutos_uso = models.IntegerField(null=True)
    # Campos de auditoria
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación

    class Meta:
        db_table = 'data_apci_academico'

class NoLeccionesAprobadas(models.Model):
    #Información General
    data_apci_academico = models.ForeignKey(DataApciAcademico, on_delete=models.CASCADE)
    curso_egb = models.CharField(max_length=30)
    lenguaje = models.FloatField()
    matematica = models.FloatField()
    # Campos de auditoria
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación

    class Meta:
        db_table = 'no_lecciones_aprobadas'

class NoAlumnosIngresados(models.Model):
    #Información General
    data_apci_academico = models.ForeignKey(DataApciAcademico, on_delete=models.CASCADE)
    curso_egb = models.CharField(max_length=30)
    paralelo_a = models.FloatField()
    paralelo_b = models.FloatField()
    paralelo_c = models.FloatField()
    total = models.FloatField()
    # Campos de auditoria
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación

    class Meta:
        db_table = 'no_alumnos_ingresados'

class PromedioAcademico(models.Model):
    #Información General
    data_apci_academico = models.ForeignKey(DataApciAcademico, on_delete=models.CASCADE)
    curso_egb = models.CharField(max_length=30)
    lenguaje = models.FloatField()
    matematica = models.FloatField()
    # Campos de auditoria
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación

    class Meta:
        db_table = 'promedio_academico'

class NoAlumnosTrabajando(models.Model):
    #Información General
    data_apci_academico = models.ForeignKey(DataApciAcademico, on_delete=models.CASCADE)
    curso_egb = models.CharField(max_length=30)
    lenguaje = models.FloatField()
    matematica = models.FloatField()
    # Campos de auditoria
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación

    class Meta:
        db_table = 'no_alumnos_trabajando'

class PedagogicalForm(models.Model):
    # Type Choices
    INTERNET_TYPE_CHOICES = (
      (1, 'No'),
      (2, 'Si'),
    )
    # Type Choices
    STATE_TYPE_CHOICES = (
      (1, 'En progreso'),
      (2, 'Finalizado')
    )
    #Información General
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, null=True)
    visit_number = models.IntegerField()
    extracurricular = models.TextField(null=True)
    internet = models.PositiveSmallIntegerField(null=True, choices=INTERNET_TYPE_CHOICES)
    action_taken = models.TextField()
    data_apci_academico = models.ForeignKey(DataApciAcademico, on_delete=models.CASCADE, null=True)
    # Campos de auditoria
    state = models.PositiveSmallIntegerField(null=True, choices=STATE_TYPE_CHOICES, default=1)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateField(null=True) # Fecha de modificación

    class Meta:
        db_table = 'pedagogical_form'
