from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from  planificacionVisitas.models import (Answer, Requerimiento, Subordinado, SubordinadoAnswer,
                              Subject, User)


class JefeSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_jefe = True
        if commit:
            user.save()
        return user


class SubordinadoSignUpForm(UserCreationForm):
    perfiles = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_subordinado = True
        user.save()
        subordinado = Subordinado.objects.create(user=user)
        subordinado.perfiles.add(*self.cleaned_data.get('perfiles'))
        return user


class SubordinadoPerfilesForm(forms.ModelForm):
    class Meta:
        model = Subordinado
        fields = ('perfiles', )
        widgets = {
            'perfiles': forms.CheckboxSelectMultiple
			
        }


class RequerimientoForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = ('text', )


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeVisitaForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = SubordinadoAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        requerimiento = kwargs.pop('requerimiento')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = requerimiento.answers.order_by('text')
