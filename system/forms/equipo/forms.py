from django.forms import *
from system.models import *


class EquipoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Equipo
        fields = '__all__'
        
        widgets = {
            'nombre_equipo': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre',
                    
                    }
                ),
            'apellido_equipo': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el apellido',
                    
                    }
                ),
            'cargo': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el cargo',
                    
                    }
                ),
            'descripcion': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese una descripcion',
                    'rows': 3,
                    'cols': 3
                    
                    }
                ),
        }
    def clean(self):
        cleaned_data = super().clean()
        nombre_equipo = cleaned_data.get('nombre_equipo')
        apellido_equipo = cleaned_data.get('apellido_equipo')
        
        if nombre_equipo:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre_equipo):
                self._errors['error'] = self._errors.get('error', self.error_class())
                self._errors['error'].append('Ingrese un nombre válido, solo se permiten letras en este campo')
        if apellido_equipo:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellido_equipo):
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