from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gestionUsuarios.models import User
from gestionArticulos.models import Media, Tag
from gestionMensajeria.models import Chat, Mensaje

# Create your views here.
# Las vistas se encargarán de gestionar las peticiones y las respuestas de las páginas web de la aplicación.

# Vistas para envío y consulta de mensajes

@login_required
def message(request):
    """
    Devolverá al usuario una de las conversaciones abiertas junto las demás a elegir y podrá leer o escribir mensajes a los propietarios/interesados de los artículos.
    """

    chats_pr = Chat.objects.filter(interesado=request.user)
    chats_in = Chat.objects.filter(articulo__propietario=request.user)

    media_id = request.GET.get('media_id')
    chat_id = request.GET.get('chat_id')
    chat_ac = None
    if media_id and Media.objects.filter(media_id=media_id).exists():
        articulo = Media.objects.get(media_id=media_id)

        if Chat.objects.filter(articulo=articulo, articulo__propietario=request.user).exists(): # Caso de chat de propietario con interesado
            chat_ac = Chat.objects.get(chat_id=chat_id)
        else: # Caso de chat de interesado con propietario
            if Chat.objects.filter(articulo=articulo, interesado=request.user).exists():
                if Chat.objects.filter(articulo=articulo, chat_id=chat_id).exists():
                    chat_ac = Chat.objects.get(chat_id=chat_id)
                else:
                    chat_ac = Chat.objects.filter(articulo=articulo, interesado=request.user)
            else:
                chat_ac = Chat.objects.create(articulo=articulo, interesado=request.user)

    if request.method == 'POST':
        texto = request.POST.get('enviar')
        print('¿Llego aquí?')
        if chat_ac and articulo and texto:
            if articulo.propietario == request.user:
                mensaje = Mensaje.objects.create(chat=chat_ac, contenido=texto, escribe=request.user, recibe=chat_ac.interesado)
            elif chat_ac.interesado == request.user:
                mensaje = Mensaje.objects.create(chat=chat_ac, contenido=texto, escribe=request.user, recibe=articulo.propietario)
            
            chat_ac.msgs.add(mensaje)
            chat_ac.save()

    return render(request, 'gestionMensajeria/messages.html', {'chats_pr': chats_pr, 'chats_in': chats_in, 'chat_ac': chat_ac})