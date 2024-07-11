from django.forms import *
from system.models import *



class GaleriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Galeria
        fields = '__all__'
        #labels = {
        #    'title': 'Nombre',
        #    'description': 'Descripción',
        #}
        
        widgets = {      
            'titulo_principal': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un titulo', 
                   
                    
                    }
                ),
            'nombre_boton': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un titulo', 
                    
                    
                    }
                ),
            'url_boton': URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un titulo', 
                    
                    
                    }
                ),
            'sub_section_proyectos': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese una descrpición', 
                    'cols': 3,
                    'rows': 3,
                    
                    }
                ),
            'sub_section_servicios': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese una descrpición', 
                    'cols': 3,
                    'rows': 3,
                    
                    }
                ),
            'sub_section_clientes': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese una descrpición', 
                    'cols': 3,
                    'rows': 3,
                    
                    }
                ),
            'sub_section_cursos': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese una descrpición', 
                    'cols': 3,
                    'rows': 3,
                    
                    }
                ),
            'sub_section_equipo': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese una descrpición', 
                    'cols': 3,
                    'rows': 3,
                    
                    }
                ),
            
            # 'imagen_principal_1': ClearableFileInput(
            #     attrs={
            #         'class': 'form-control', 
            #         'type': 'file',
                
            #         }
            #     ),
            # 'imagen_principal_2': ClearableFileInput(
            #     attrs={
            #         'class': 'form-control', 
            #         'type': 'file',
                
            #         }
            #     ),
            # 'imagen_principal_3': ClearableFileInput(
            #     attrs={
            #         'class': 'form-control', 
            #         'type': 'file',
                
            #         }
            #     ),
            # 'imagen_mision': ClearableFileInput(
            #     attrs={
            #         'class': 'form-control', 
            #         'type': 'file',
                
            #         }
            #     ),
            # 'imagen_vision': ClearableFileInput(
            #     attrs={
            #         'class': 'form-control', 
            #         'type': 'file',
                
            #         }
            #     ),
            #  'nombre_boton': TextInput(
            #     attrs={
            #         'class': 'form-control',
            #         'placeholder': 'Ingrese el nombre del boton', 
            #         }
            #     ),
            #  'url_boton': URLInput(
            #     attrs={
            #         'class': 'form-control',
            #         'placeholder': 'Ingrese un url', 
            #         }
            #     ),
            #  'estado': CheckboxInput(
            #     attrs={
            #         'class': 'form-check',
            #         }
            #     ),
             
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
      
class ImagenGaleriaForm(ModelForm):
    imagen = MultipleFileField(label='Selecciona Imagenes para la portada', required=False)

    class Meta:
        model = ImagenGaleria
        fields = ['imagen']
        
        
        
    def clean(self):
        cleaned_data = super().clean()
        if Compania.objects.exists() and not self.instance.pk:
            raise forms.ValidationError('Solo puede existir una instancia de Compania.')
        return cleaned_data
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