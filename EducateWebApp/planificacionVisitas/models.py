from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_subordinado = models.BooleanField(default=False)
    is_jefe = models.BooleanField(default=False)


class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Visita(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visitas')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='visitas')

    def __str__(self):
        return self.name


class Requerimiento(models.Model):
    visita = models.ForeignKey(Visita, on_delete=models.CASCADE, related_name='requerimientos')
    text = models.CharField('Requerimiento', max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Subordinado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    visitas = models.ManyToManyField(Visita, through='TakenVisita')
    perfiles = models.ManyToManyField(Subject, related_name='perfil_subordinados')

    def get_unanswered_requerimientos(self, visita):
        answered_requerimientos = self.visita_answers \
            .filter(answer__requerimiento__visita=visita) \
            .values_list('answer__requerimiento__pk', flat=True)
        requerimientos = visita.requerimientos.exclude(pk__in=answered_requerimientos).order_by('text')
        return requerimientos

    def __str__(self):
        return self.user.username


class TakenVisita(models.Model):
    subordinado = models.ForeignKey(Subordinado, on_delete=models.CASCADE, related_name='taken_visitas')
    visita = models.ForeignKey(Visita, on_delete=models.CASCADE, related_name='taken_visitas')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class SubordinadoAnswer(models.Model):
    subordinado = models.ForeignKey(Subordinado, on_delete=models.CASCADE, related_name='visita_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
