from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gestionArticulos.models import Media, Tag
from gestionUsuarios.models import UsuarioInfo, UsuarioUbicacion
from gestionArticulos.forms import MediaForm
from gestionArticulos.enums import CategoriaType

# Create your views here.
# Las vistas se encargarán de gestionar las peticiones y las respuestas de las páginas web de la aplicación.

def articles_results(request):
    """
    Devolverá al usuario 10 resultados por página de los artículos encontrados a traves de su búsqueda con tags o sin tags usando categorías.
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
                    articulos = Media.objects.filter(categoria__exact=CategoriaType(categoria).name, tags__name__in=taglist)
                else:
                    articulos = Media.objects.filter(categoria__exact=CategoriaType(categoria).name, nombre__icontains=consulta)
            else:
                if ',' in consulta:
                    articulos = Media.objects.filter(tags__name__in=taglist)
                else:
                    articulos = Media.objects.filter(nombre__icontains=consulta)

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

        if id:
            articulo = Media.objects.filter(media_id=id)
            if articulo:
                usuarioinfo = UsuarioInfo.objects.filter(usuario=articulo[0].propietario)
                usuarioub = UsuarioUbicacion.objects.filter(usuario=articulo[0].propietario)

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
                if Tag.objects.get(name=tagname): # Comprobamos si ya existe el tag que se quiere añadir y si no existe lo creamos.
                    tag = Tag.objects.get(name=tagname)
                else:
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
    Devolverá al usuario una plantilla con sus artículos.
    """

    try:
        if request.method == "POST":
            print(request.POST.get('eliminar'))
            print(request.POST.get('asignar'))
        articulos = Media.objects.filter(propietario=request.user)
    except:
        articulos = None

    return render(request, 'gestionArticulos/myarticles.html', {'articulos': articulos})
