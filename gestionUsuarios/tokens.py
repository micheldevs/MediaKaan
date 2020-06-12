from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, usuario, timestamp):
        return (
            six.text_type(usuario.pk) + six.text_type(timestamp) +
            six.text_type(usuario.is_active)
        )

account_token = TokenGenerator()
