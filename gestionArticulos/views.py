from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from gestionArticulos.models import Media, Tag
from gestionUsuarios.models import User, UsuarioInfo, UsuarioUbicacion
from gestionArticulos.forms import MediaForm
from gestionArticulos.enums import CategoriaType

# Create your views here.
# Las vistas se encargarán de gestionar las peticiones y las respuestas de las páginas web de la aplicación.

def articles_results(request):
    """
    Devolverá al usuario 5 resultados por página de los artículos encontrados a traves de su búsqueda con tags o sin tags usando categorías.
    """

    if request.method == 'GET':
        consulta = request.GET.get('consulta')
        categoria = request.GET.get('categoria')
        pag = request.GET.get('p')
        articulos_ppag = 5  # Artículos por página
        articulos = None
        n_pags = None
        n_articulos = None

        if consulta and categoria:
            if categoria == "Usuarios": # Si la categoría es usuarios, le redirigimos a la vista correspondiente en gestionUsuarios para que trate la consulta
                return redirect(('%s?consulta='+consulta) % reverse('gestionUsuarios:usrresults'))

            if not pag:  # Mantenemos que el número de página exista si el usuario la borra de la cabecera o ha hecho una búsqueda
                pag = 1

            # Mantenemos que el número de página se encuentre por encima del límite inferior
            pag = int(pag)
            if pag < 1:
                pag = 1

            # Listamos los tags si se han utilizado. (separados por comas)
            if ',' in consulta:
                taglist = consulta.split(',')
                print(taglist)

            if categoria != "Todas":  # Filtramos por categoría.
                if ',' in consulta:  # Si se encuentran comas en la consulta, la búsqueda será por tags.
                    articulos = Media.objects.filter(categoria__exact=CategoriaType(categoria).name, tags__name__in=taglist, asignado=None)
                else:
                    articulos = Media.objects.filter(categoria__exact=CategoriaType(categoria).name, nombre__icontains=consulta, asignado=None)
            else:
                if ',' in consulta:
                    articulos = Media.objects.filter(tags__name__in=taglist, asignado=None)
                else:
                    articulos = Media.objects.filter(nombre__icontains=consulta, asignado=None)

            # Gestionamos las páginas y los resultados a mostrar en esta
            n_articulos = articulos.count()
            if n_articulos != 0:
                if n_articulos % articulos_ppag < 1.0:
                    n_pags = int(n_articulos/articulos_ppag)
                    if n_pags == 0:  # Si hay menos de 10 artículos, habrá una sola página.
                        n_pags = 1
                else:  # Si el resultado de artículos por página es impar y mayor que uno, añadimos una página más.
                    n_pags = int(n_articulos/articulos_ppag)+1

                if pag > n_pags:  # Mantenemos el número de página debajo del límite superior.
                    pag = n_pags
            else:
                n_pags = 0

            # Recoge los artículos por página a partir del índice especificado entre los artículos.
            # En Django la función de OFFSET para los datos se establece con la sintaxis del array de python. [OFFSET, OFFSET+LIMIT]
            articulos = articulos[(pag-1)*articulos_ppag:(pag-1)*articulos_ppag+articulos_ppag]

    print(articulos)
    return render(request, 'gestionArticulos/articles.html', {'consulta': consulta,
                                                              'categoria': categoria,
                                                              'p': pag,
                                                              'n_pags': n_pags,
                                                              'n_articulos': n_articulos,
                                                              'articulos': articulos})

def article(request):
    """
    Devolverá al usuario el artículo consultado con información del propietario y su ubicación.
    """

    if request.method == 'GET':
        id = request.GET.get('id')
        articulo = None
        usuarioinfo = None
        usuarioub = None

        try:
            if id:
                articulo = Media.objects.get(media_id=id, asignado=None)
                if articulo:
                    usuarioinfo = UsuarioInfo.objects.get(usuario=articulo.propietario)
                    usuarioub = UsuarioUbicacion.objects.get(usuario=articulo.propietario)
        except:
            articulo = None
            usuarioinfo = None
            usuarioub = None

    return render(request, 'gestionArticulos/article.html', {'articulo': articulo, 'usuarioinfo': usuarioinfo, 'usuarioub': usuarioub})

@login_required
def add_article(request):
    """
    Devolverá al usuario una plantilla donde registrar el artículo que desea añadir.
    """

    tagserror = False
    registered = False
    if request.method == 'POST':
        media_form = MediaForm(data=request.POST, files=request.FILES)

        tags = request.POST.get('id_tags')

        if len(tags) <= 159: # Número de caracteres máximos con tags con comas incluídas.
            tag_list = tags.split(',') # Separamos por coma los tags introducidos por el usuario y los metemos en una lista.

            # Comprobamos que haya como máximo 10 tags con 15 caracteres cada uno como máximo.
            if len(tag_list) <= 10:
                for tagname in tag_list:
                    if len(tagname) > 15:
                        tagserror = True
            else:
                tagserror = True
        else:
            tagserror = True
        
        # Comprobamos que el formulario está libre de errores
        if media_form.is_valid() and not tagserror:
            # Creación del artículo
            media = media_form.save(commit=False)
            media.propietario = request.user
            media.avatar = request.FILES['fotoart']
            media.save()

            # Tratamiento de los tags
            for tagname in tag_list:
                try:
                    tag = Tag.objects.get(name=tagname)
                except Tag.DoesNotExist:
                    tag = Tag.objects.create(name=tagname)

                media.tags.add(tag)
            
            media.save()
            registered = True # Guardamos el artículo en la base de datos e informamos al usuario de que la operación se ha completado con éxito
    else:
        media_form = MediaForm()

    return render(request, 'gestionArticulos/addarticle.html', {'media_form': media_form,
                                                                'tagserror': tagserror,
                                                                'registered': registered})

@login_required
def my_articles(request):
    """
    Devolverá al usuario una plantilla con sus artículos y le dejará borrarlos o asignarlos.
    """

    borrado = None
    asignado = None
    erroras = False
    if request.method == "POST":
        articulo = None

        if request.POST.get('eliminar'):
            try:
                id = request.POST.get('eliminar')
                articulo = Media.objects.get(media_id=id, propietario=request.user) # Comprobamos que el usuario es dueño del artículo que desea borrar identificado con su id correspondiente.
                if articulo:
                    borrado = articulo.nombre
                    articulo.delete()
            except:
                articulo = None
        else:
            if request.POST.get('asignar') and request.POST.get('asignado'):
                try:
                    id = request.POST.get('asignar')
                    us_asignado = User.objects.get(username=request.POST.get('asignado'))

                    if us_asignado != request.user: # Evitamos que el usuario se lo asigne a sí mismo.
                        articulo = Media.objects.get(media_id=id, propietario=request.user, asignado=None)
                        articulo.asignado = us_asignado
                        asignado = us_asignado.username
                        articulo.save()
                    else:
                        erroras = True
                except:
                    erroras = True
            else:
                erroras = True

    if Media.objects.filter(propietario=request.user).exists():
        articulos = Media.objects.filter(propietario=request.user)
    else:
        articulos = None

    return render(request, 'gestionArticulos/myarticles.html', {'articulos': articulos, 'borrado': borrado, 'asignado': asignado, 'erroras': erroras})

@login_required
def rec_articles(request):
    """
    Devolverá al usuario una plantilla con los artículos que ha obtenido de otras personas y podrá valorar dichos artículos.
    """

    articulo = None
    propietario = None
    if request.method == "POST":
        try:
            if request.POST.get('valorar') and 0 < int(request.POST.get('selected_rating')) <= 5: # Comprobamos que la valoración del artículo está entre el rango de estrellas
                id = request.POST.get('valorar')
                articulo = Media.objects.get(media_id=id)
                if articulo:
                    propietario = UsuarioInfo.objects.get(usuario=articulo.propietario)
                    if propietario:
                        articulo.valorado = int(request.POST.get('selected_rating'))
                        propietario.valoracion = propietario.valoracion + int(request.POST.get('selected_rating'))
                        propietario.n_valoraciones = propietario.n_valoraciones + 1
                        articulo.save()
                        propietario.save()
        except:
            articulo = None
            propietario = None

    if Media.objects.filter(asignado=request.user).exists():
        articulos = Media.objects.filter(asignado=request.user)
    else:
        articulos = None

    return render(request, 'gestionArticulos/recarticles.html', {'articulos': articulos})