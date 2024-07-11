from django.forms import *
from system.models import *
from django_summernote.widgets import SummernoteWidget

class CursosForm(ModelForm):
    class Meta:
        model = Cursos
        fields = '__all__'
        
        widgets = {
            'nombre_curso': TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre del capacitador'
                }
            ),
            'descripcion': SummernoteWidget(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese la descripcion del curso',

                }
            ),
            
            'fecha_de_inicio': DateInput(
                attrs = {
                    'class': 'form-control col-3',
                    'type': 'date',
                }
            ),
            
            'horario': TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese el horario del curso - Ejm: Lun - Viernes de 8pm a 10pm',
                }
            ),
            'duracion': TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese la duracion del curso - Ejm: 3 meses',
                }
            ),
            'costo': TextInput(
                attrs = {
                    'class': 'form-control col-3',
                    'placeholder': 'Ingrese el costo del curso - Ejm: 3500',
                    
                }
            ),
            'capacitador_id': Select(
                attrs = {
                    'class': 'form-control col-3',
                    'style': 'width: 100%'
                }
            )
                    
        }
        
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