from django.forms import *
from system.models import *
from system.validators.formatChecker import *
from django_summernote.widgets import SummernoteWidget

class ProyectoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Proyectos
        fields = '__all__'
        
        widgets = {
            'nombre_proyecto': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre del proyecto',
                    
                    }
                ),
            'descripcion_proyecto': SummernoteWidget(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese una descripcion',
                    
                    }
                ),
            'fecha_de_proyecto': DateInput(
                attrs = {
                    'class': 'form-control col-3',
                    'type': 'date',
                }
            ),
            'cliente_id': Select(
                attrs={
                    'class': 'form-control col-3',
                    'placeholder': 'Ingrese el nombre del proyecto',
                    
                    }
                ),
        }

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
      
class ImagenProyectoForm(ModelForm):
    imagen = MultipleFileField(label='Selecciona Imagenes del servicio', required=False, validators=[file_size, file_extension])

    class Meta:
        model = ImagenProyectos
        fields = ['imagen']
    # def save(self, commit=True):
    #     data = {}
    #     form = super()
    #     try:
    #         if form.is_valid():
    #             form.save()
    #         else:
    #             data['error'] = form.errors
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return data