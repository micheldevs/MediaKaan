from django.shortcuts import render
from gestionUsuarios.forms import UsuarioForm, UsuarioInfoForm, UsuarioUbicacionForm
from gestionUsuarios.models import User, UsuarioInfo, UsuarioUbicacion
from gestionArticulos.models import Media
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from gestionUsuarios.emails import activation_email, recovery_email, suggestion_email
from gestionUsuarios.tokens import account_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


# Create your views here.
# Las vistas se encargarán de gestionar las peticiones y las respuestas de las páginas web de la aplicación. (renderizará plantillas)

# Vistas generales

def index(request):
    """
    Creará una respuesta al usuario mostrando la página índice de la aplicación.
    """
    return render(request,'index.html')

def about(request):
    """
    Creará una respuesta al usuario mostrando la página de información de la aplicación y dejando al usuario o invitado enviar una sugerencia al desarrollador.
    """

    if request.method == 'POST':
        suggestion = False

        sugerencia = request.POST.get('sugerencia')

        if len(sugerencia) >= 30 and len(sugerencia) <= 150:
            suggestion_email(request, sugerencia) # Enviamos la sugerencia al correo del desarrollador.
            suggestion = True
        
        return render(request,'about.html', {'suggestion': suggestion})
    else:
        return render(request,'about.html', {})

# Vistas de gestión de creación o logueo del usuario

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
            activation_email(request, usuario, usuario_form)

            registered = True
        else:
            print(usuario_form.errors, infous_form.errors, ubus_form.errors)
    else:
        usuario_form = UsuarioForm()
        infous_form = UsuarioInfoForm()
        ubus_form = UsuarioUbicacionForm()
    
    return render(request,'gestionUsuarios/signup.html',
                          {'usuario_form': usuario_form,
                           'infous_form': infous_form,
                           'ubus_form': ubus_form,
                           'registered': registered})

def activate(request, uidb64, token):
    """
    Renderiza la página de activación de la cuenta y activa aquellas cuentas que no estén aún activadas por medio de su token correspondiente.
    """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        usuario = User.objects.get(pk=uid)
    except:
        usuario = None

    if usuario is not None and account_token.check_token(usuario, token):
        usuario.is_active = True
        usuario.save()
        success = True
    else:
        success = False
    
    return render(request,'gestionUsuarios/activateacc.html',
                          {'success': success})

def forget_pass(request):
    """
    Renderiza la página de recuperación de la cuenta del usuario a partir de un formulario donde el usuario deberá introducir su correo electrónico.
    """
    
    if request.method == 'POST':
        reset = False
        email_dir = request.POST.get('email')

        try:
            usuario = User.objects.get(email=email_dir)
        except:
            usuario = None

        if usuario:
            # Envío de correo de recuperación (seguimos la misma estrategia que con el correo de activación)
            recovery_email(request, usuario, email_dir)
            reset = True

        return render(request,'gestionUsuarios/forgetpass.html', {'reset': reset})
    else:
        return render(request,'gestionUsuarios/forgetpass.html', {})

def change_pass(request, uidb64, token):
    """
    Renderiza la página de cambio de contraseña para el usuario con su token correspondiente para hacerlo.
    """

    changed = None
    if request.method == 'POST':
        usuario_form = UsuarioForm(data=request.POST)

        if not usuario_form['password'].errors and not usuario_form['passwordRep'].errors: # Comprobamos si ha habido errores en los campos del formulario

            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                usuario = User.objects.get(pk=uid)
            except:
                usuario = None

            if usuario is not None and account_token.check_token(usuario, token):
                usuario.set_password(usuario_form.cleaned_data.get('password'))
                usuario.save()
                changed = True
            else:
                changed = False
        else:
            print(usuario_form.errors)
    else:
        usuario_form = UsuarioForm()
    
    return render(request,'gestionUsuarios/changepass.html',
                          {'usuario_form': usuario_form,
                           'changed': changed})
                           
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

# Vistas de los paneles del usuario

@login_required
def my_profile(request):
    """
    Renderizará el perfil del usuario, donde se darán opciones para editar datos.
    """

    updated = False
    fieldUp = [False]*6
    oldPassEr = False
    try:
        usuarioinfo = UsuarioInfo.objects.get(usuario=request.user)
    except:
        usuarioinfo = None
    
    if request.method == 'POST':
        usuario_form = UsuarioForm(data=request.POST)
        infous_form = UsuarioInfoForm(data=request.POST, files=request.FILES)
        ubus_form = UsuarioUbicacionForm(data=request.POST)

        if infous_form['fechaNacimiento'].value(): # fieldUp 0 - Fecha de nacimiento cambiada
            fieldUp[0] = True
            if not infous_form['fechaNacimiento'].errors:
                usuarioinfo.fechaNacimiento = infous_form['fechaNacimiento'].value()
                updated = True
        elif infous_form['avatar'].value(): # fieldUp 1 - Avatar cambiado
            fieldUp[1] = True
            if not infous_form['avatar'].errors:
                usuarioinfo.avatar = request.FILES['avatar']
                updated = True
        elif infous_form['bio'].value(): # fieldUp 2 - Bio cambiada
            fieldUp[2] = True
            if not infous_form['bio'].errors:
                usuarioinfo.bio = infous_form['bio'].value()
                updated = True
        elif usuario_form['email'].value(): # fieldUp 3 - Email cambiado
            fieldUp[3] = True
            if not usuario_form['email'].errors:
               request.user.email = usuario_form['email'].value()
               updated = True
        elif request.POST.get('passwordOld'): # fieldUp 4 - Contraseña cambiada
            fieldUp[4] = True
            if authenticate(username=request.user.username, password=request.POST.get('passwordOld')):
                if not usuario_form['password'].errors and not usuario_form['passwordRep'].errors:
                    request.user.set_password(usuario_form['password'].value())
                    updated = True
            else:
                oldPassEr = True
        elif ubus_form['latUb'].value() and ubus_form['lngUb'].value(): # fieldUp 5 - Ubicación cambiada
            fieldUp[5] = True
            if not ubus_form['latUb'].errors:
                usuarioub = UsuarioUbicacion.objects.get(usuario=request.user)
                usuarioub.latUb = float(ubus_form['latUb'].value())
                usuarioub.lngUb = float(ubus_form['lngUb'].value())
                usuarioub.save()
                updated = True

        if updated:
            request.user.save()
            usuarioinfo.save()

    else:
        usuario_form = UsuarioForm()
        infous_form = UsuarioInfoForm()
        ubus_form = UsuarioUbicacionForm()


    return render(request, 'gestionUsuarios/userprofile.html',
                        {'usuarioinfo': usuarioinfo,
                        'usuario_form': usuario_form,
                        'infous_form': infous_form,
                        'ubus_form': ubus_form,
                        'updated': updated,
                        'fieldUp': fieldUp,
                        'oldPassEr': oldPassEr})

@login_required
def delete_user(request):
    """
    Renderizará el campo de contraseña del usuario junto a un botón para eliminar la cuenta del usuario.
    """
    
    delerror = False
    if request.method == 'POST':
        try:
            password = request.POST.get('password')

            usuario = authenticate(username=request.user.username, password=password)

            if usuario:
                usuario.delete()
                logout(request)
                return HttpResponseRedirect(reverse('index'))
            else:
                delerror = True
        except:
            delerror = True


    return render(request, 'gestionUsuarios/deleteprofile.html', {'delerror': delerror})

# Vistas de consulta de usuarios
def users_results(request):
    """
    Devolverá al usuario 5 resultados por página de los usuarios encontrados a traves de su búsqueda del username.
    """

    if request.method == 'GET':
        consulta = request.GET.get('consulta')
        pag = request.GET.get('p')
        usuarios_ppag = 5  # Usuarios por página
        usuarios = None
        n_pags = None
        n_usuarios = None

        if consulta:
            if not pag:  # Mantenemos que el número de página exista si el usuario la borra de la cabecera o ha hecho una búsqueda
                pag = 1

            # Mantenemos que el número de página se encuentre por encima del límite inferior
            pag = int(pag)
            if pag < 1:
                pag = 1

            usuarios = UsuarioInfo.objects.filter(usuario__username__icontains=consulta)

            # Gestionamos las páginas y los resultados a mostrar en esta
            n_usuarios = usuarios.count()
            if n_usuarios != 0:
                if n_usuarios % usuarios_ppag < 1.0:
                    n_pags = int(n_usuarios/usuarios_ppag)
                    if n_pags == 0:  # Si hay menos de 10 artículos, habrá una sola página.
                        n_pags = 1
                else:  # Si el resultado de artículos por página es impar y mayor que uno, añadimos una página más.
                    n_pags = int(n_usuarios/usuarios_ppag)+1

                if pag > n_pags:  # Mantenemos el número de página debajo del límite superior.
                    pag = n_pags
            else:
                n_pags = 0

            # Recoge los artículos por página a partir del índice especificado entre los artículos.
            # En Django la función de OFFSET para los datos se establece con la sintaxis del array de python. [OFFSET, OFFSET+LIMIT]
            usuarios = usuarios[(pag-1)*usuarios_ppag:(pag-1)*usuarios_ppag+usuarios_ppag]

    print(usuarios)
    return render(request, 'gestionUsuarios/users.html', {'consulta': consulta,
                                                              'p': pag,
                                                              'n_pags': n_pags,
                                                              'n_usuarios': n_usuarios,
                                                              'usuarios': usuarios})

def user(request):
    """
    Devolverá al usuario el usuario consultado con información de él y sus artículos.
    """

    if request.method == 'GET':
        username = request.GET.get('username')
        articulos = None
        usuarioinfo = None
        usuarioub = None

        try:
            if username:
                usuarioinfo = UsuarioInfo.objects.get(usuario__username=username)
                usuarioub = UsuarioUbicacion.objects.get(usuario__username=username)
                if usuarioinfo and usuarioub:
                    articulos = Media.objects.filter(propietario=usuarioinfo.usuario, asignado=None)
        except:
            articulos = None
            usuarioinfo = None
            usuarioub = None
    
    return render(request, 'gestionUsuarios/user.html', {'articulos': articulos, 'usuarioinfo': usuarioinfo, 'usuarioub': usuarioub})