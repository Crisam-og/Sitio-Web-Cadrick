from django.forms import *
from system.models import *
from django_summernote.widgets import SummernoteWidget
import re
class CapacitadorForm(ModelForm):
    class Meta:
        model = Capacitador
        fields = ('nombre_capacitador','apellidos_capacitador','grado_academico','correo','descripcion_c','imagen')
        
        widgets = {
            'nombre_capacitador': TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre del capacitador'
                }
            ),
            'apellidos_capacitador': TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese el apellido del capacitador'
                }
            ),
            
            'grado_academico': Select(
                attrs = {
                    'class': 'form-control col-sm-2 control-label',
                    'placeholder': 'Ingrese el grado academico del capacitador'
                }
            ),
            
            'correo': TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese el correo del capacitador',
                }
            ),
            'descripcion_c': SummernoteWidget(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese una descripción',
                    
                }
                ),
                    
        }
        
    def clean(self):
        cleaned_data = super().clean()
        nombre_capacitador = cleaned_data.get('nombre_capacitador')
        apellidos_capacitador = cleaned_data.get('apellidos_capacitador')

        if nombre_capacitador:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre_capacitador):
                self._errors['error'] = self._errors.get('error', self.error_class())
                self._errors['error'].append('Ingrese un nombre válido, solo se permiten letras en este campo')

        if apellidos_capacitador:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellidos_capacitador):
                self._errors['error'] = self._errors.get('error', self.error_class())
                self._errors['error'].append('Ingrese un apellido válido, solo se permiten letras en este campo')
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