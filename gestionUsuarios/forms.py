from django import forms
from gestionUsuarios.models import UsuarioInfo
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from datetime import datetime

# Creará formularios desde los modelos

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex='^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
                message='La contraseña debe tener mínimo 8 caracteres y al menos una letra o número.')])
    class Meta():
        model = User
        fields = ('username','email','password')
        help_texts = {
            'password': 'La contraseña debe tener al menos una letra o número y una longitud como mínimo con 8 caracteres.'
        }

class UsuarioInfoForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(),
        validators=[
            MinLengthValidator(
                100,
                message='La biografía del usuario debe tener al menos 100 caracteres.'),
            MaxLengthValidator(
                150,
                message='La biografía del usuario debe tener como máximo 150 caracteres.')])
    avatar = forms.ImageField(widget=forms.FileInput(),
        validators=[
            FileExtensionValidator(
                allowed_extensions=['.jpg', '.jpeg', '.png', '.gif'],
                message='El avatar debe tener una extensión válida de imagen (JPG, JPEG, PNG, GIF).')
            ])

    fechaNacimiento = forms.DateField(widget=forms.DateInput())

    def clean_avatar(self):
            avatar = self.cleaned_data.get('avatar', False)
            if avatar:
                if avatar._height != 500 or avatar._width != 500:
                    raise ValidationError("Las dimensiones del avatar deben ser de 500x500.")
                return avatar
            else:
                raise ValidationError("No se ha encontrado cargada ninguna imagen.")
    
    def clean_birth_date(self):
        fechaNacimiento = self.cleaned_data.get('fechaNacimiento', False)
        edad = datetime.now() - fechaNacimiento
        if edad < 18 :
            raise forms.ValidationError("La edad del usuario debe ser igual o mayor a 18 años para usar la aplicación.")
        return fechaNacimiento

    class Meta():
         model = UsuarioInfo
         fields = ('avatar', 'bio', 'fechaNacimiento')
         help_texts = {
             'avatar': 'El avatar debe ser una imagen con dimensiones 500x500.',
             'fechaNacimiento': 'El usuario debe tener 18 años para poder utilizar la aplicación.'
         }