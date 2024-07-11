from django import forms
from django.core.validators import RegexValidator
from system.models import *
import re
class IncripcionesForm(forms.ModelForm):

    class Meta:
        model = Inscripciones
        fields = ['nombre_ins', 'apellidos_ins', 'telefono', 'correo', 'profesion', 'grado_academico', 'curso_id', 'consulta']
        
        
        widgets = {
            'nombre_ins': forms.TextInput(attrs={
                'class': 'form-control',
                'name': 'name',
                'placeholder': 'Ingrese su nombre',
                'label': 'Nombre'

            }),
            'apellidos_ins': forms.TextInput(attrs={
                'class': 'form-control',
                'name': 'name',
                'placeholder': 'Ingrese su apellido',
                'label': 'Apellidos'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'name': 'name',
                'placeholder': 'Ingrese su numero de telefono',
            }),
            'correo': forms.TextInput(attrs={
                'class': 'form-control',
                'name': 'email',
                'placeholder': 'Ingrese su correo',
            }),
            'profesion': forms.TextInput(attrs={
                'class': 'form-control',
                'name': 'name',
                'placeholder': 'Ingrese su profesión',
            }),
            'grado_academico': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione su grado academico',
            }),
            'curso_id': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione su grado academico',
            }),
            'consulta': forms.Textarea(attrs={
                'class': 'form-control',
                'name': 'comment',
                'placeholder': 'Consulta*'
            }),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        nombre_ins = cleaned_data.get('nombre_ins')
        apellidos_ins = cleaned_data.get('apellidos_ins')
        telefono = cleaned_data.get('telefono')
        profesion = cleaned_data.get('profesion')

        if nombre_ins:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre_ins):
                self._errors['error'] = self._errors.get('error', self.error_class())
                self._errors['error'].append('Ingrese un nombre válido, solo se permiten letras en este campo')

        if apellidos_ins:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellidos_ins):
                self._errors['error'] = self._errors.get('error', self.error_class())
                self._errors['error'].append('Ingrese un apellido válido, solo se permiten letras en este campo')

        if telefono:
            if not re.match(r'^\d{9}$', telefono):
                self._errors['error'] = self._errors.get('error', self.error_class())
                self._errors['error'].append('Ingrese un numero de telefóno valido, solo se permiten numeros en este campo y un limite de 9 digitos')
        
        if profesion:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', profesion):
                self._errors['error'] = self._errors.get('error', self.error_class())
                self._errors['error'].append('Ingrese una profesión válida, solo se permiten letras en este campo')
        return cleaned_data
    
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data