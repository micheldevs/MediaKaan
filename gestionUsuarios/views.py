from django.shortcuts import render
from gestionUsuarios.forms import UsuarioForm, UsuarioInfoForm, UsuarioUbicacionForm
from gestionUsuarios.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from gestionUsuarios.tokens import account_activation_token

# Create your views here.
# Las vistas se encargarán de gestionar las peticiones y las respuestas de las páginas web de la aplicación.

def index(request):
    """
    Creará una respuesta al usuario mostrando la página índice de la aplicación.
    """
    return render(request,'index.html')

def about(request):
    """
    Creará una respuesta al usuario mostrando la página de información de la aplicación.
    """
    return render(request,'about.html')

@login_required
def user_logout(request):
    """
    Deslogueará al usuario y lo devolverá a la página índice de la aplicación.
    """
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    """
    Registrará al usuario con las oportunas validaciones del formulario de registro.
    """

    registered = False
    if request.method == 'POST':
        usuario_form = UsuarioForm(data=request.POST) # Tomamos el formulario de los datos identificativos del usuario
        infous_form = UsuarioInfoForm(data=request.POST, files=request.FILES) # Tomamos el formulario de los datos adicionales del usuario
        ubus_form = UsuarioUbicacionForm(data=request.POST) # Tomamos el formulario de la ubicación del usuario

        # Comprobamos que todos los formularios son correctos, si no son validos la capa cliente
        # mostrará los errores correspondientes de cada campo del formulario.
        if usuario_form.is_valid() and infous_form.is_valid() and ubus_form.is_valid():
            # Creación del usuario
            usuario = usuario_form.save()
            usuario.set_password(usuario.password)
            usuario.is_active = False # Dejamos desactivada la cuenta para que el usuario la active por medio de un email
            usuario.save()

            # Creación del perfil de información del usuario
            infous = infous_form.save(commit=False)
            infous.usuario = usuario
            infous.avatar = request.FILES['avatar']
            infous.save()

            # Creación de la ubicación del usuario
            ubus = ubus_form.save(commit=False)
            ubus.usuario = usuario
            ubus.save()

            # Envío del email para activar la cuenta
            current_site = get_current_site(request)
            mail_subject = 'Activación de la cuenta de usuario en MediaKaanª'
            message = render_to_string('gestionUsuarios/email/email_active.html', {
                'usuario': usuario,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(usuario.pk)),
                'token': account_activation_token.make_token(usuario),
            })
            to_email = usuario_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html" # Especificamos que el correo eléctronico se envíe en modo html para que respete el cuerpo del mensaje que le hemos asignado
            email.send()

            registered = True
        else:
            print(usuario_form.errors, infous_form.errors, ubus_form.errors)
    else:
        usuario_form = UsuarioForm()
        infous_form = UsuarioInfoForm()
        ubus_form = UsuarioUbicacionForm(data=request.POST)
    
    return render(request,'gestionUsuarios/signup.html',
                          {'usuario_form':usuario_form,
                           'infous_form':infous_form,
                           'ubus_form':ubus_form,
                           'registered':registered})

def activate(request, uidb64, token):
    """
    Renderiza la página de activación de la cuenta y activa aquellas cuentas que no estén aún activadas por medio de su token correspondiente.
    """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        usuario = User.objects.get(pk=uid)
    except:
        usuario = None

    if usuario is not None and account_activation_token.check_token(usuario, token):
        usuario.is_active = True
        usuario.save()
        success = True
    else:
        success = False
    
    return render(request,'gestionUsuarios/activateacc.html',
                          {'success':success})

                           
def user_login(request):
    """
    Renderizará la página de inicio de sesión del usuario y gestionará el inicio de sesión.
    """

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                warning = "Tu cuenta está inactiva. Confirmela desde su correo eléctronico y vuelva a iniciar sesión."
                return render(request, 'gestionUsuarios/signin.html', {'warning': warning})
        else:
            error = "El nombre de usuario o la contraseña son incorrectas o su cuenta necesita activación."
            return render(request, 'gestionUsuarios/signin.html', {'error': error})
    else:
        return render(request, 'gestionUsuarios/signin.html', {})
