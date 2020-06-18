from django import forms
from gestionArticulos.models import Media
from gestionArticulos.enums import AccionType, CategoriaType
from django.core.validators import MinLengthValidator, MaxLengthValidator, FileExtensionValidator
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError

# Creará formularios desde los modelos y hace las validaciones pertinentes

class MediaForm(forms.ModelForm):
    """
    Formulario de los artículos multimedia.
    """
    
    # Texto de ayuda para los campos del formulario
    def __init__(self, *args, **kwargs):
        super(MediaForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].help_text = 'El artículo debe tener un título de entre 15 y 100 caracteres.'
        self.fields['descripcion'].help_text = 'La descripción del artículo debe ser lo que ofrece el artículo o información de él y debe ser de entre 120 y 240 caracteres.'
        self.fields['fotoart'].help_text = 'La foto del artículo debe tener una extensión de imagen válida además de tener unas dimensiones de 720x1280.'
        self.fields['accion'].help_text = 'El tipo de acción para un artículo es lo que el usuario decide hacer con el mismo (donar, intercambiar o prestar).'
        self.fields['categoria'].help_text = 'Será la categoría donde aparezca tu artículo. (Ej: Película, Música, Videojuegos...)'

    # Campo de título del artículo con validadores de longitud entre 15 y 150 caracteres con mensajes de error
    nombre = forms.CharField(widget=forms.TextInput(),
        validators=[
            MinLengthValidator(
                15,
                message='El título del artículo debe tener mínimo 15 caracteres.'),
            MaxLengthValidator(
                100,
                message='El título del artículo debe tener máximo 100 caracteres.')])
    
    # Campo de descripción del artículo con validadores de longitud entre 120 y 240 caracteres con mensajes de error
    descripcion = forms.CharField(widget=forms.Textarea(),
        validators=[
            MinLengthValidator(
                120,
                message='La descripción del artículo debe tener mínimo 120 caracteres.'),
            MaxLengthValidator(
                240,
                message='La descripción del artículo debe tener máximo 240 caracteres.')])

    # Campo de la foto de artículo del usuario con validador de extensión del archivo y mensaje de error
    fotoart = forms.ImageField(widget=forms.FileInput(),
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif'],
                message='La foto de artículo debe tener una extensión válida de imagen (JPG, JPEG, PNG, GIF).')
            ])

    # Campo de acción para el artículo del usuario.
    accion = forms.ChoiceField(choices=AccionType.choices())

    # Campo de categoría para el artículo del usuario.
    categoria = forms.ChoiceField(choices=CategoriaType.choices())

    # Validador adicional del campo de la foto de artículo, valida las dimensiones de la imagen que sube el usuario
    def clean_fotoart(self):
            fotoart = self.cleaned_data.get('fotoart', False)
            width, height = get_image_dimensions(fotoart)
            if fotoart:
                if height > 1280 or width > 720:
                    raise ValidationError("Las dimensiones de la foto del artículo deben ser de 720x1280.")
                return fotoart
            else:
                raise ValidationError("No se ha encontrado cargada ninguna imagen.")

    class Meta():
         model = Media
         fields = ('nombre', 'descripcion', 'fotoart', 'accion', 'categoria')