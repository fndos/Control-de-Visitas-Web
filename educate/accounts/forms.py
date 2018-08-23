from django import forms
from betterforms.multiform import MultiModelForm
from . models import User, School, Requirement, Visit, Sector
from django.db.models import Q

############################### TECH_LEADER (t) ################################

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'dni',
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
            'phone_number',
            'user_type',
            'sector',
        ]
        labels = {
            'dni': 'Cédula',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'username': 'Usuario',
            'password': 'Contraseña',
            'email': 'Correo electrónico',
            'phone_number': 'Teléfono',
            'user_type': 'Tipo de usuario',
        }
        widgets = {
            'dni': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control'}),
            'user_type': forms.Select(attrs={'class':'form-control'}),
        }

    sector = forms.ModelMultipleChoiceField(
        queryset=Sector.objects.all(),
        label='Sectores',
        widget=forms.CheckboxSelectMultiple,
        )

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = [
            'id',
            'name',
            'description',
        ]
        labels = {
            'id': 'ID',
            'name': 'Nombre',
            'description': 'Descripción',
        }
        widgets = {
            'id': forms.TextInput(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
        }

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            'amie',
            'name',
            'phone_number',
            'address',
            'reference',
            'parish',
            'priority',
            'sector',
            'ambassador_in',
            'workday',
        ]
        labels = {
            'amie': 'AMIE',
            'name': 'Nombre',
            'phone_number': 'Teléfono',
            'address': 'Dirección',
            'reference': 'Referencia',
            'parish': 'Parroquia',
            'priority': 'Prioridad',
            'sector': 'Zona',
            'ambassador_in': 'Embajador IN',
            'workday': 'Jornada',
        }
        widgets = {
            'amie': forms.TextInput(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'reference': forms.TextInput(attrs={'class':'form-control'}),
            'parish': forms.TextInput(attrs={'class':'form-control'}),
            'priority': forms.Select(attrs={'class':'form-control'}),
            'sector': forms.Select(attrs={'class':'form-control'}),
            'ambassador_in': forms.TextInput(attrs={'class':'form-control'}),
            'workday': forms.Select(attrs={'class':'form-control'}),
        }

class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = [
            'reason',
            'school',
            'type',
        ]
        labels = {
            'reason': 'Motivo',
            'school': 'Escuela',
            'type': 'Tipo',
        }
        widgets = {
            'reason': forms.TextInput(attrs={'class':'form-control'}),
            'school': forms.Select(attrs={'class':'form-control'}),
            'type': forms.Select(attrs={'class':'form-control'}),
        }

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = [
            'date_planned',
            'requirement',
            'user',
        ]
        labels = {
            'date_planned': 'Fecha',
        }
        widgets = {
            'date_planned': forms.TextInput(attrs={'class':'form-control', 'type':'datetime'}),
        }

    requirement = forms.ModelChoiceField(
        queryset=Requirement.objects.filter(state=1),
        label='Motivo',
        widget=forms.Select(attrs={'class':'form-control'}),
        )

    user = forms.ModelChoiceField(
        queryset=User.objects.filter(Q(user_type=2) | Q(user_type=4)), # Si el usuario es Tech o Tech Leader
        label='Responsable',
        widget=forms.Select(attrs={'class':'form-control'}),
        )

############################### TUTOR_LEADER (r) ###############################

class RequirementCreateForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = [
            'reason',
            'school',
        ]
        labels = {
            'reason': 'Motivo',
            'school': 'Escuela',
        }
        widgets = {
            'reason': forms.TextInput(attrs={'class':'form-control'}),
            'school': forms.Select(attrs={'class':'form-control'}),
        }

class VisitCreateForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = [
            'date_planned',
            'requirement',
            'user',
        ]
        labels = {
            'date_planned': 'Fecha',
        }
        widgets = {
            'date_planned': forms.TextInput(attrs={'class':'form-control', 'type':'datetime'}),
        }

    requirement = forms.ModelChoiceField(
        queryset=Requirement.objects.filter(state=1),
        label='Motivo',
        widget=forms.Select(attrs={'class':'form-control'}),
        )

    user = forms.ModelChoiceField(
        queryset=User.objects.filter(Q(user_type=1) | Q(user_type=3)), # Si el usuario es Tutor o Tutor Leader
        label='Responsable',
        widget=forms.Select(attrs={'class':'form-control'}),
        )

class VisitUpdateForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = [
            'date_planned',
            'user',
        ]
        labels = {
            'date_planned': 'Fecha',
        }
        widgets = {
            'date_planned': forms.TextInput(attrs={'class':'form-control', 'type':'datetime'}),
        }

    user = forms.ModelChoiceField(
        queryset=User.objects.filter(Q(user_type=1) | Q(user_type=3)), # Si el usuario es Tutor o Tutor Leader
        label='Responsable',
        widget=forms.Select(attrs={'class':'form-control'}),
        )
