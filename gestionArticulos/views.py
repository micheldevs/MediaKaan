from django.shortcuts import render
from gestionArticulos.models import Media
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