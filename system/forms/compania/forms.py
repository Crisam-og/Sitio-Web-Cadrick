from django.forms import *
from system.models import *
from django_summernote.widgets import SummernoteWidget

class CompaniaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Compania
        fields = '__all__'
        
        widgets = {
            
            'nombre_compania': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre',
                    
                    }
                ),
            'email': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un correo',
                    
                    }
                ),
            'telefono': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el telefono',
                    
                    }
                ),
            'direccion': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese una dirección',
                    
                    }
                ),
            'url_whatsapp': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el link de Whatsapp',
                    
                    }
                ),
            'url_googlemaps': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el url de google maps',
                    
                    }
                ),
            'historia': SummernoteWidget(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese una historia', 
                    }
                ),
            'mision': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese una mision', 
                    'rows': 3,
                    'cols': 3 
                    }
                ),
             'vision': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese una vision', 
                    'rows': 3,
                    'cols': 3 
                    }
                ),
            
        }
        
    def clean(self):
        cleaned_data = super().clean()
        if Compania.objects.exists() and not self.instance.pk:
            raise forms.ValidationError('Solo puede existir una instancia de Compania.')
        return cleaned_data
# class ConfigForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#     class Meta:
#         model = Configuraciones
#         fields = '__all__'
#         exclude = ['nombre_config']
        
#         widgets = {
#             'nombre_config': TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'placeholder': 'Ingrese el nombre de configuracion',
#                     'disabled': True,
#                     'required':False,
                    
#                     }
#                 ),
#             'valor': TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'placeholder': 'Ingrese el valor',
                    
#                     }
#                 ),
#         }
#     def save(self, commit=True):
#         data = {}
#         form = super()
#         try:
#             if form.is_valid():
#                 form.save()
#             else:
#                 data['error'] = form.errors
#         except Exception as e:
#             data['error'] = str(e)
#         return data