from django.forms import *
from system.models import *
from django.utils.safestring import mark_safe

class CustomClearableFileInput(ClearableFileInput):
    template_with_initial = (
        '%(initial_text)s: %(initial)s %(clear_template)s<br />%(input_text)s: %(input)s'
    )

    def render(self, name, value, attrs=None, renderer=None):
        substitutions = {
            'initial': '',
            'input': super().render(name, value, attrs, renderer),
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
        }
        template = '%(input)s'
        if value and hasattr(value, "url"):
            substitutions['initial'] = (
                '<a href="%s" target="_blank">%s</a>' % (value.url, value)
            )
            substitutions['clear_template'] = self.clear_checkbox_label
            substitutions['clear_checkbox_name'] = self.clear_checkbox_name(name)
            substitutions['clear_checkbox_id'] = self.clear_checkbox_id(attrs['id'])
            template = self.template_with_initial
        return mark_safe(template % substitutions)

class ClientesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Clientes
        fields = '__all__'
        
        widgets = {
            'nombre_cliente': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre del servicio',
                    
                    }
                ),
            'imagen': ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'type': 'file',
                    
                    }
                ),
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