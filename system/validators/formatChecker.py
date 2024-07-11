import os
import re
# from django.core.exceptions import ValidationError
from django.forms import ValidationError
"""
    Same as FileField, but you can specify:
    * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
    * max_upload_size - a number indicating the maximum file size allowed for upload.
        2.5MB - 2621440
        5MB - 5242880
        10MB - 10485760
        20MB - 20971520
        50MB - 5242880
        100MB - 104857600
        250MB - 214958080
        500MB - 429916160
"""

def file_size(value):
    limit = 5242880
    if value.size > limit:
        raise ValidationError('Imagen muy grande. Sube una imagen que no exceda los 5 MB.')
    
def file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.PNG', '.JPG']
    if not ext in valid_extensions:
        raise ValidationError('Tipo de archivo no soportado. Solo se permiten archivos PNG y JPG')


    
# def validate_only_letters(value):
#     if not value.isalpha() != False:
#         raise ValidationError('Este campo solo debe contener letras.')
#     return value
# def validate_only_numbers(value):
#     if not value.isdigit():
#         raise ValidationError('Este campo solo debe contener números.')
#     if len(value) != 9:
#         raise ValidationError('El número de teléfono debe tener 9 dígitos.')
#     return value