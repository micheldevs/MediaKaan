from django import forms
from gestionUsuarios.models import UsuarioInfo, User
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, FileExtensionValidator
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
from datetime import datetime

# Creará formularios desde los modelos y hace las validaciones pertinentes

class UsuarioForm(forms.ModelForm):
    """
    Formulario del usuario.
    """

    # Texto de ayuda para los campos del formulario
    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['password'].help_text = 'La contraseña debe tener al menos una letra o número y una longitud como mínimo con 8 caracteres.'

    # Campo de la contraseña con validador de su expresión regular y mensaje de error
    password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex='^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
                message='La contraseña debe tener mínimo 8 caracteres y al menos una letra o número.')])
    
    passwordRep = forms.CharField(widget=forms.PasswordInput()) # Campo para repetir la contraseña

    # Validador de la repetición de contraseña con mensaje de error
    def clean_passwordRep(self):
        password = self.cleaned_data.get('password', False)
        passwordRep = self.cleaned_data.get('passwordRep', False)

        if password and password != passwordRep:
            raise forms.ValidationError("Las contraseñas deben coincidir.")
        return passwordRep
    
    class Meta():
        model = User
        fields = ('username','email','password')

class UsuarioInfoForm(forms.ModelForm):
    """
    Formulario de la información adicional del usuario.
    """
    
    # Texto de ayuda para los campos del formulario
    def __init__(self, *args, **kwargs):
        super(UsuarioInfoForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].help_text = 'El avatar debe ser una imagen con dimensiones 500x500.'
        self.fields['fechaNacimiento'].help_text = 'El usuario debe tener 18 años para poder utilizar la aplicación.'

    # Campo de biografía con validadores de longitud entre 100 y 150 caracteres con mensajes de error
    bio = forms.CharField(widget=forms.Textarea(),
        validators=[
            MinLengthValidator(
                100,
                message='La biografía del usuario debe tener al menos 100 caracteres.'),
            MaxLengthValidator(
                150,
                message='La biografía del usuario debe tener como máximo 150 caracteres.')])

    # Campo del avatar del usuario con validador de extensión del archivo y mensaje de error
    avatar = forms.ImageField(widget=forms.FileInput(),
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif'],
                message='El avatar debe tener una extensión válida de imagen (JPG, JPEG, PNG, GIF).')
            ])

    # Campo de fecha de nacimiento
    fechaNacimiento = forms.DateField(widget=forms.DateInput())

    # Validador adicional del campo avatar, valida las dimensiones de la imagen que sube el usuario
    def clean_avatar(self):
            avatar = self.cleaned_data.get('avatar', False)
            width, height = get_image_dimensions(avatar)
            if avatar:
                if height > 500 or width > 500:
                    raise ValidationError("Las dimensiones del avatar deben ser de 500x500.")
                return avatar
            else:
                raise ValidationError("No se ha encontrado cargada ninguna imagen.")
    
    # Validador de fecha de nacimiento, donde el usuario debe tener 18 años
    def clean_fechaNacimiento(self):
        fechaNacimiento = self.cleaned_data.get('fechaNacimiento', False)
        edad = datetime.now().date() - fechaNacimiento
        if edad.days < 18*365 :
            raise forms.ValidationError("La edad del usuario debe ser igual o mayor a 18 años para usar la aplicación.")
        return fechaNacimiento

    class Meta():
         model = UsuarioInfo
         fields = ('avatar', 'bio', 'fechaNacimiento')