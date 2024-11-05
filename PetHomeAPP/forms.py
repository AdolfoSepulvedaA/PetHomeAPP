# forms.py
from django import forms
from .models import Animal, Usuario
from .validator import validar_rut
from django.contrib.auth.forms import AuthenticationForm

class RegistroAnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nombre', 'especie', 'edad', 'caracteristicas']
        widgets = {
            'caracteristicas': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descripción de las características'}),
        }



class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña", min_length=6)

    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'correo', 'celular', 'password', 'tipo_cuenta']  # Elimina 'username'

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not validar_rut(rut):
            raise forms.ValidationError("RUT inválido")
        return rut

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return password

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = self.cleaned_data['correo']  
        usuario.set_password(self.cleaned_data['password'])  # Establecer la contraseña encriptada
        if commit:
            usuario.save()
        return usuario
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Correo electrónico")