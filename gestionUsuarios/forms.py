from django import forms
from gestionUsuarios.models import UsuarioInfo
from django.contrib.auth.models import User

# Creará formularios desde los modelos

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','email','password')

class UsuarioInfoForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea())
    class Meta():
         model = UsuarioInfo
         fields = ('avatar', 'bio', 'fechaNacimiento')