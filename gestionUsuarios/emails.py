from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from gestionUsuarios.tokens import account_token

# Fichero encargado de informar al usuario por medio de emails para distintos casos de uso

def activation_email(request, usuario, usuario_form):
    """
    Se encargará de enviar un email de activación de la cuenta para el usuario.
    """

    current_site = get_current_site(request)
    mail_subject = 'Activación de la cuenta de usuario en MediaKaanª'
    message = render_to_string('gestionUsuarios/email/email_active.html', {
        'usuario': usuario,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(usuario.pk)),
        'token': account_token.make_token(usuario),
    })
    to_email = usuario_form.cleaned_data.get('email')
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.content_subtype = "html" # Especificamos que el correo eléctronico se envíe en modo html para que respete el cuerpo del mensaje que le hemos asignado
    email.send()

def recovery_email(request, usuario, email_dir):
    """
    Se encargará de enviar un email de recuperación de la cuenta para el usuario.
    """

    current_site = get_current_site(request)
    mail_subject = 'Recuperación de la cuenta de usuario en MediaKaanª'
    message = render_to_string('gestionUsuarios/email/email_recovery.html', {
        'usuario': usuario,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(usuario.pk)),
        'token': account_token.make_token(usuario),
    })
    to_email = email_dir
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.content_subtype = "html" # Especificamos que el correo eléctronico se envíe en modo html para que respete el cuerpo del mensaje que le hemos asignado
    email.send()