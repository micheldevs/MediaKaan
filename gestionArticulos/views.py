from django.shortcuts import render
from gestionArticulos.models import Media
from gestionArticulos.enums import CategoriaType

# Create your views here.
# Las vistas se encargarán de gestionar las peticiones y las respuestas de las páginas web de la aplicación.

def articles_results(request):
    """
    Creará una respuesta al usuario mostrando la página índice de la aplicación.
    """

    if request.method == 'GET':
        consulta = request.GET.get('consulta')
        categoria = request.GET.get('categoria')
        articulos = None

        if consulta and categoria:
            if categoria != "Todas":
                articulos=Media.objects.filter(categoria__exact=CategoriaType(categoria).name, nombre__icontains=consulta)
            else:
                articulos=Media.objects.filter(nombre__icontains=consulta)
            print(articulos)
    return render(request, 'gestionArticulos/articles.html', {'consulta':consulta, 'categoria':categoria, 'articulos':articulos})