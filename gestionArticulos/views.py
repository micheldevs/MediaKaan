from django.shortcuts import render
from gestionArticulos.models import Media
from gestionUsuarios.models import UsuarioInfo, UsuarioUbicacion
from gestionArticulos.enums import CategoriaType

# Create your views here.
# Las vistas se encargarán de gestionar las peticiones y las respuestas de las páginas web de la aplicación.

def articles_results(request):
    """
    Devolverá al usuario los resultados de los artículos encontrados a traves de su búsqueda.
    """

    if request.method == 'GET':
        consulta = request.GET.get('consulta')
        categoria = request.GET.get('categoria')
        articulos = None

        if consulta and categoria:
            if ',' in consulta:
                taglist = consulta.split(',')
                print(taglist)
            
            if categoria != "Todas":
                if ',' in consulta:
                    articulos=Media.objects.filter(categoria__exact=CategoriaType(categoria).name, tags__name__in=taglist)
                else:
                    articulos=Media.objects.filter(categoria__exact=CategoriaType(categoria).name, nombre__icontains=consulta)
            else:
                if ',' in consulta:
                    articulos=Media.objects.filter(tags__name__in=taglist)
                else:
                    articulos=Media.objects.filter(nombre__icontains=consulta)

            print(articulos)
    return render(request, 'gestionArticulos/articles.html', {'consulta':consulta, 'categoria':categoria, 'articulos':articulos})

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
            articulo=Media.objects.filter(media_id=id)
            if articulo:
                usuarioinfo=UsuarioInfo.objects.filter(usuario=articulo[0].propietario)
                usuarioub=UsuarioUbicacion.objects.filter(usuario=articulo[0].propietario)

    return render(request, 'gestionArticulos/article.html', {'articulo':articulo, 'usuarioinfo':usuarioinfo, 'usuarioub':usuarioub})