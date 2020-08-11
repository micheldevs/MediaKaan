from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from gestionArticulos.models import Media, Tag
from gestionUsuarios.models import User, UsuarioInfo, UsuarioUbicacion
from gestionArticulos.forms import MediaForm
from gestionArticulos.enums import CategoriaType

# Create your views here.
# Las vistas se encargarán de gestionar las peticiones y las respuestas de las páginas web de la aplicación.

# Vistas de consulta de artículos

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

        if not pag:  # Mantenemos que el número de página exista si el usuario la borra de la cabecera o ha hecho una búsqueda
            pag = 1

        # Mantenemos que el número de página se encuentre por encima del límite inferior
        pag = int(pag)
        if pag < 1:
            pag = 1

        if consulta and categoria:
            if categoria == "Usuarios":  # Si la categoría es usuarios, le redirigimos a la vista correspondiente en gestionUsuarios para que trate la consulta
                return redirect(('%s?consulta='+consulta) % reverse('gestionUsuarios:usrresults'))

            # Listamos los tags si se han utilizado. (separados por comas)
            if ',' in consulta:
                taglist = consulta.split(',')
                print(taglist)

            if categoria != "Todas":  # Filtramos por categoría.
                if ',' in consulta:  # Si se encuentran comas en la consulta, la búsqueda será por tags.
                    articulos = Media.objects.filter(categoria__exact=CategoriaType(categoria).name, tags__name__in=taglist, asignado=None).distinct()
                else:
                    articulos = Media.objects.filter(categoria__exact=CategoriaType(categoria).name, nombre__icontains=consulta, asignado=None).distinct()
            else:
                if ',' in consulta:
                    articulos = Media.objects.filter(tags__name__in=taglist, asignado=None).distinct()
                else:
                    articulos = Media.objects.filter(nombre__icontains=consulta, asignado=None).distinct()
        elif categoria and categoria != "Todas" and categoria != "Usuarios":
            articulos = Media.objects.filter(categoria__exact=CategoriaType(categoria).name, asignado=None).distinct()

        if articulos:
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
            articulos = articulos[(pag-1)*articulos_ppag:(pag-1) * articulos_ppag+articulos_ppag]
        else:
            n_articulos = 0


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

        if id and Media.objects.filter(media_id=id, asignado=None).exists():
            articulo = Media.objects.get(media_id=id, asignado=None)
            usuarioinfo = UsuarioInfo.objects.get(usuario=articulo.propietario)
            usuarioub = usuarioinfo.ubicacion

    return render(request, 'gestionArticulos/article.html', {'articulo': articulo, 'usuarioinfo': usuarioinfo, 'usuarioub': usuarioub})

# Vistas del panel de usuario relacionadas con artículos

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

        # Número de caracteres máximos con tags con comas incluídas.
        if len(tags) <= 159:
            # Separamos por coma los tags introducidos por el usuario y los metemos en una lista.
            tag_list = tags.split(',')

            # Comprobamos que haya como máximo 10 tags con 15 caracteres cada uno como máximo.
            if len(tag_list) <= 10:
                for tagname in tag_list:
                    if len(tagname) > 15:
                        tagserror = True
                        break
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
                if Tag.objects.filter(name=tagname).exists(): # Si el tag ya existe en la base de datos, creamos uno nuevo para el artículo y lo añadimos al artículo
                    tag = Tag.objects.get(name=tagname)
                else:
                    tag = Tag.objects.create(name=tagname)

                media.tags.add(tag)

            media.save() # Guardamos el artículo en la base de datos

            # Insertamos el artículo del usuario en el vector embebido en su documento, que quedará referenciado por una id
            usuarioinfo = UsuarioInfo.objects.get(usuario=request.user)
            usuarioinfo.articulos.add(media)
            usuarioinfo.save()

            registered = True  # Guardamos el artículo en la base de datos e informamos al usuario de que la operación se ha completado con éxito
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
    usuarioinfo = UsuarioInfo.objects.get(usuario=request.user) # Devolvemos a partir de la información del usuario los artículos del mismo

    borrado = None
    asignado = None
    erroras = False
    if request.method == "POST":
        articulo = None

        if request.POST.get('eliminar'):
            id = request.POST.get('eliminar')
            # Comprobamos que el usuario es dueño del artículo que desea borrar identificado con su id correspondiente.
            if Media.objects.filter(media_id=id, propietario=request.user).exists():
                articulo = Media.objects.get(media_id=id, propietario=request.user)
                usuarioinfo.articulos.remove(articulo) # Borramos la referencia del artículo del usuario
                if articulo.asignado: # Si estaba asignado borramos su referencia de los artículos asignados del usuario
                    us_asignado = UsuarioInfo.objects.get(usuario=articulo.asignado)
                    us_asignado.articulos_rec.remove(articulo)
                    us_asignado.save()
                borrado = articulo.nombre
                articulo.delete() # Borramos finalmente el artículo y guardamos
                usuarioinfo.save()
        else:
            if request.POST.get('asignar') and request.POST.get('asignado'):
                id = request.POST.get('asignar')
                if User.objects.filter(username=request.POST.get('asignado')).exists():
                    us_asignado = UsuarioInfo.objects.get(usuario__username=request.POST.get('asignado'))
                    if us_asignado.usuario != request.user and Media.objects.filter(media_id=id, propietario=request.user, asignado=None).exists():  # Evitamos que el usuario se lo asigne a sí mismo y vemos si el artículo no está asignado.
                        articulo = Media.objects.get(media_id=id, propietario=request.user, asignado=None)
                        articulo.asignado = us_asignado.usuario
                        asignado = us_asignado.usuario.username
                        articulo.save()
                        us_asignado.articulos_rec.add(articulo)
                        us_asignado.save()
                    else:
                        erroras = True
                else:
                    erroras = True
            else:
                erroras = True

    return render(request, 'gestionArticulos/myarticles.html', {'articulos': usuarioinfo.articulos.all, 'borrado': borrado, 'asignado': asignado, 'erroras': erroras})

@login_required
def rec_articles(request):
    """
    Devolverá al usuario una plantilla con los artículos que ha obtenido de otras personas y podrá valorar dichos artículos.
    """

    articulo = None
    propietario = None
    if request.method == "POST":
        id = request.POST.get('valorar')
        val = int(request.POST.get('selected_rating_'+id))
        if id and 0 < val <= 5:  # Comprobamos que la valoración del artículo está entre el rango de estrellas
            if Media.objects.filter(media_id=id, asignado=request.user).exists(): # Comprobamos que existe el artículo con dicho id que se le asignó al usuario
                articulo = Media.objects.get(media_id=id, asignado=request.user)
                if UsuarioInfo.objects.filter(usuario=articulo.propietario).exists(): # Comprobamos si existe su propietario
                    propietario = UsuarioInfo.objects.get(usuario=articulo.propietario)
                    articulo.valorado = val # Asignamos la valoración al artículo
                    propietario.valoracion = propietario.valoracion + val # Asignamos a la valoración global del usuario una adición con la del artículo
                    propietario.n_valoraciones = propietario.n_valoraciones + 1 # Añadimos al número de valoraciones una más por el usuario
                    articulo.save()
                    propietario.save()

    usuarioinfo = UsuarioInfo.objects.get(usuario=request.user) # Cogemos la información del usuario para devolverle aquellos artículos donde se le ha asignado

    return render(request, 'gestionArticulos/recarticles.html', {'articulos': usuarioinfo.articulos_rec.all})