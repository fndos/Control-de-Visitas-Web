from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.db import models

class Sector(models.Model):
    # Información General
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, max_length=200)
    # Campos de auditoria
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateTimeField(auto_now=True) # Fecha de modificación

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
    # Campos de auditoria
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_updated = models.DateTimeField(auto_now=True) # Fecha de modificación

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
    # Type Choices
    PARISH_TYPE_CHOICES = (
      (1, 'Ayacucho'),
      (2, 'Bolívar (Sagrario)'),
      (3, 'Carbo (Concepción)'),
      (4, 'Chongón'),
      (5, 'Febres Cordero'),
      (6, 'García Moreno'),
      (7, 'Letamendi'),
      (8, 'Nueve de Octubre'),
      (9, 'Olmedo (San Alejo)'),
      (10, 'Pascuales'),
      (11, 'Roca'),
      (12, 'Rocafuerte'),
      (13, 'Sucre'),
      (14, 'Tarqui'),
      (15, 'Urdaneta'),
      (16, 'Ximena'),
      (17, 'Juan Gómez Rendón (Progreso)'),
      (18, 'Puná'),
      (19, 'Tenguel'),
      (20, 'Posorja'),
      (21, 'El Morro'),
    )
    # Información General
    amie = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    workday = models.PositiveSmallIntegerField(null=True, choices=WORKDAY_TYPE_CHOICES)
    parish = models.PositiveSmallIntegerField(null=True, choices=PARISH_TYPE_CHOICES)
    priority = models.PositiveSmallIntegerField(null=True, choices=PRIORITY_TYPE_CHOICES)
    ambassador_in = models.CharField(max_length=100)
    # Escuelas agrupadas por sectores o zonas
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    # Campos de auditoria
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateTimeField(auto_now=True) # Fecha de modificación

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
    REQUIREMENT_TYPE_CHOICES = ( # Null, visita pedagógica (Visita Pedagógica)
      (1, 'Periódica'), # Requerimiento creado por tech_leader (Visita Técnica)
      (2, 'Llamada'), # Requerimiento creado por el tech_leader (Visita Técnica)
      (3, 'Incidencia'), # Requerimiento creado por tutor o tutor_leader (Visita Técnica)
    )
    # Información General
    state = models.PositiveSmallIntegerField(null=True, choices=STATE_TYPE_CHOICES, default=1)
    #  Motivo del servicio o requerimiento
    reason = models.TextField()
    type = models.PositiveSmallIntegerField(null=True, choices=REQUIREMENT_TYPE_CHOICES)
    # School ID
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    # Usuario que generó el requerimiento (created_by)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # Campos de auditoria
    # Tech Leader, Tutor o Tutor Leader que generó el requerimiento
    is_active = models.NullBooleanField(null=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateTimeField(auto_now=True) # Fecha de modificación

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
    state = models.PositiveSmallIntegerField(null=True, choices=STATE_TYPE_CHOICES, default=1)
    # Campos de auditoria
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateTimeField(auto_now=True) # Fecha de modificación

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

    def __str__(self):
        return '{}'.format("ID ( " + str(self.id) + ") - " + str(self.date_planned) + " - " +str(self.requirement))

    class Meta:
        db_table = 'visit'

class TechnicalForm(models.Model):
    # Type Choices
    STATE_TYPE_CHOICES = (
      (1, 'En progreso'),
      (2, 'Finalizado')
    )
    # Información General
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, null=True)
    action_taken = models.CharField(max_length=250)
    observation = models.TextField(null=True)
    apci = models.NullBooleanField(null=False)
    internet = models.NullBooleanField(null=False)
    software = models.NullBooleanField(null=False)
    hardware = models.NullBooleanField(null=False)
    electrico = models.NullBooleanField(null=False)
    redes = models.NullBooleanField(null=False)
    state = models.PositiveSmallIntegerField(null=True, choices=STATE_TYPE_CHOICES, default=1)
    # Campos de auditoria
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateTimeField(auto_now=True) # Fecha de modificación

    def __str__(self):
        return '{}'.format("ID ( " + str(self.id) + ") - " + str(self.visit.date_planned) + " - " +str(self.visit.requirement))

    class Meta:
        db_table = 'technical_form'

class PedagogicalForm(models.Model):
    # Type Choices
    INTERNET_TYPE_CHOICES = (
      (1, 'No'),
      (2, 'Si'),
    )
    # Type Choices
    EXTRA_TYPE_CHOICES = (
      (1, 'No'),
      (2, 'Si'),
    )
    # Type Choices
    STATE_TYPE_CHOICES = (
      (1, 'En progreso'),
      (2, 'Finalizado')
    )
    # Información General
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, null=True)
    extracurricular = models.PositiveSmallIntegerField(null=True, choices=EXTRA_TYPE_CHOICES)
    internet = models.PositiveSmallIntegerField(null=True, choices=INTERNET_TYPE_CHOICES)
    action_taken = models.TextField()
    # Información GRID-APCI
    no_prof_capacitados = models.IntegerField()
    minutos_uso = models.FloatField()
    # ALUMNOS INGRESADOS
    AI_2doEGB_A = models.FloatField()
    AI_2doEGB_B = models.FloatField()
    AI_2doEGB_C = models.FloatField()
    AI_2doEGB_TOTAL = models.FloatField()
    AI_3roEGB_A = models.FloatField()
    AI_3roEGB_B = models.FloatField()
    AI_3roEGB_C = models.FloatField()
    AI_3roEGB_TOTAL = models.FloatField()
    AI_4toEGB_A = models.FloatField()
    AI_4toEGB_B = models.FloatField()
    AI_4toEGB_C = models.FloatField()
    AI_4toEGB_TOTAL = models.FloatField()
    AI_5toEGB_A = models.FloatField()
    AI_5toEGB_B = models.FloatField()
    AI_5toEGB_C = models.FloatField()
    AI_5toEGB_TOTAL = models.FloatField()
    AI_6toEGB_A = models.FloatField()
    AI_6toEGB_B = models.FloatField()
    AI_6toEGB_C = models.FloatField()
    AI_6toEGB_TOTAL = models.FloatField()
    AI_7moEGB_A = models.FloatField()
    AI_7moEGB_B = models.FloatField()
    AI_7moEGB_C = models.FloatField()
    AI_7moEGB_TOTAL = models.FloatField()
    AI_8voEGB_A = models.FloatField()
    AI_8voEGB_B = models.FloatField()
    AI_8voEGB_C = models.FloatField()
    AI_8voEGB_TOTAL = models.FloatField()
    AI_9noEGB_A = models.FloatField()
    AI_9noEGB_B = models.FloatField()
    AI_9noEGB_C = models.FloatField()
    AI_9noEGB_TOTAL = models.FloatField()
    AI_10moEGB_A = models.FloatField()
    AI_10moEGB_B = models.FloatField()
    AI_10moEGB_C = models.FloatField()
    AI_10moEGB_TOTAL = models.FloatField()
    AI_TOTAL_PROMEDIO_A = models.FloatField()
    AI_TOTAL_PROMEDIO_B = models.FloatField()
    AI_TOTAL_PROMEDIO_C = models.FloatField()
    AI_TOTAL_PROMEDIO_TOTAL = models.FloatField()
    # ALUMNOS TRABAJANDO
    AT_2doEGB_LEN = models.FloatField()
    AT_2doEGB_MAT = models.FloatField()
    AT_3roEGB_LEN = models.FloatField()
    AT_3roEGB_MAT = models.FloatField()
    AT_4toEGB_LEN = models.FloatField()
    AT_4toEGB_MAT = models.FloatField()
    AT_5toEGB_LEN = models.FloatField()
    AT_5toEGB_MAT = models.FloatField()
    AT_6toEGB_LEN = models.FloatField()
    AT_6toEGB_MAT = models.FloatField()
    AT_7moEGB_LEN = models.FloatField()
    AT_7moEGB_MAT = models.FloatField()
    AT_8voEGB_LEN = models.FloatField()
    AT_8voEGB_MAT = models.FloatField()
    AT_9noEGB_LEN = models.FloatField()
    AT_9noEGB_MAT = models.FloatField()
    AT_10moEGB_LEN = models.FloatField()
    AT_10moEGB_MAT = models.FloatField()
    AT_TOTAL_PROMEDIO_LEN = models.FloatField()
    AT_TOTAL_PROMEDIO_MAT = models.FloatField()
    # LECCIONES APROBADAS
    LA_2doEGB_LEN = models.FloatField()
    LA_2doEGB_MAT = models.FloatField()
    LA_3roEGB_LEN = models.FloatField()
    LA_3roEGB_MAT = models.FloatField()
    LA_4toEGB_LEN = models.FloatField()
    LA_4toEGB_MAT = models.FloatField()
    LA_5toEGB_LEN = models.FloatField()
    LA_5toEGB_MAT = models.FloatField()
    LA_6toEGB_LEN = models.FloatField()
    LA_6toEGB_MAT = models.FloatField()
    LA_7moEGB_LEN = models.FloatField()
    LA_7moEGB_MAT = models.FloatField()
    LA_8voEGB_LEN = models.FloatField()
    LA_8voEGB_MAT = models.FloatField()
    LA_9noEGB_LEN = models.FloatField()
    LA_9noEGB_MAT = models.FloatField()
    LA_10moEGB_LEN = models.FloatField()
    LA_10moEGB_MAT = models.FloatField()
    LA_TOTAL_PROMEDIO_LEN = models.FloatField()
    LA_TOTAL_PROMEDIO_MAT = models.FloatField()
    # PROMEDIO ACADÉMICO
    PA_2doEGB_LEN = models.FloatField()
    PA_2doEGB_MAT = models.FloatField()
    PA_3roEGB_LEN = models.FloatField()
    PA_3roEGB_MAT = models.FloatField()
    PA_4toEGB_LEN = models.FloatField()
    PA_4toEGB_MAT = models.FloatField()
    PA_5toEGB_LEN = models.FloatField()
    PA_5toEGB_MAT = models.FloatField()
    PA_6toEGB_LEN = models.FloatField()
    PA_6toEGB_MAT = models.FloatField()
    PA_7moEGB_LEN = models.FloatField()
    PA_7moEGB_MAT = models.FloatField()
    PA_8voEGB_LEN = models.FloatField()
    PA_8voEGB_MAT = models.FloatField()
    PA_9noEGB_LEN = models.FloatField()
    PA_9noEGB_MAT = models.FloatField()
    PA_10moEGB_LEN = models.FloatField()
    PA_10moEGB_MAT = models.FloatField()
    PA_TOTAL_PROMEDIO_LEN = models.FloatField()
    PA_TOTAL_PROMEDIO_MAT = models.FloatField()
    state = models.PositiveSmallIntegerField(null=True, choices=STATE_TYPE_CHOICES, default=1)
    # Campos de auditoria
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(null=True, max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True) # Fecha de creación
    date_updated = models.DateTimeField(auto_now=True) # Fecha de modificación

    def __str__(self):
        return '{}'.format("ID ( " + str(self.id) + ") - " + str(self.visit.date_planned) + " - " +str(self.visit.requirement))

    class Meta:
        db_table = 'pedagogical_form'
