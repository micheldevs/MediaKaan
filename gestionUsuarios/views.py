from django.shortcuts import render
from gestionUsuarios.forms import UsuarioForm, UsuarioInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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
def special(request):
    """
    Informará a través de un string al usuario de que esté ya se encuentra logueado.
    """
    return HttpResponse("Ya te encuentras logueado.")

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
        usuario_form = UsuarioForm(data=request.POST)
        infous_form = UsuarioInfoForm(data=request.POST, files=request.FILES)
        if usuario_form.is_valid() and infous_form.is_valid():
            usuario = usuario_form.save()
            usuario.set_password(usuario.password)
            usuario.save()
            infous = infous_form.save(commit=False)
            infous.set_usuario(usuario.get_username())
            infous.avatar = request.FILES['avatar']
            infous.save()
            registered = True
        else:
            print(usuario_form.errors, infous_form.errors)
    else:
        usuario_form = UsuarioForm()
        infous_form = UsuarioInfoForm()
    
    return render(request,'gestionUsuarios/signup.html',
                          {'usuario_form':usuario_form,
                           'infous_form':infous_form,
                           'registered':registered})
                           
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                warning = "Tu cuenta está inactiva. Por favor consulte al administrador."
                return render(request, 'gestionUsuarios/signin.html', {'warning': warning})
        else:
            error = "El nombre de usuario o la contraseña son incorrectas."
            return render(request, 'gestionUsuarios/signin.html', {'error': error})
    else:
        return render(request, 'gestionUsuarios/signin.html', {})
