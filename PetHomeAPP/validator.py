import re
from django.core.exceptions import ValidationError

def validar_rut(rut):
    rut = rut.strip().replace('.', '').replace('-', '')
    
    # Validar que el RUT contenga solo entre 1 y 8 dígitos
    if not re.match(r'^\d{1,8}$', rut):
        raise ValidationError("Formato de RUT inválido. Debe ser un número de 1 a 8 dígitos.")

    return rut  # Devolver el RUT validado sin modificar
