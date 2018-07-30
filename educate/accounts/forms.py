from django import forms
from . models import User, School

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
            'dni':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'phone_number':forms.TextInput(attrs={'class':'form-control'}),
            'user_type':forms.TextInput(attrs={'class':'form-control'}),
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
            'is_active',
            'date_joined',
            'created_by',
            'sector',
            'tutor',
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
            'is_active': 'Estado',
            'date_joined': 'Fecha de creación',
            'created_by': 'Creado por',
            'sector_id': 'Sector',
            'tutor_id': 'Embajador IN',
            'workday_id': 'Jornada',
        }
        widgets = {
            'amie':forms.TextInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'phone_number':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'reference':forms.TextInput(attrs={'class':'form-control'}),
            'parish':forms.TextInput(attrs={'class':'form-control'}),
            'priority':forms.TextInput(attrs={'class':'form-control'}),
            'is_active':forms.TextInput(attrs={'class':'form-control'}),
            'date_joined':forms.TextInput(attrs={'class':'form-control'}),
            'created_by':forms.TextInput(attrs={'class':'form-control'}),
            'sector_id':forms.Select(attrs={'class':'form-control'}),
            'tutor_id':forms.Select(attrs={'class':'form-control'}),
            'workday_id':forms.Select(attrs={'class':'form-control'}),
        }
