import datetime

from django.conf import settings
from rest_framework.authtoken.models import Token

MAX_LEN = 12


def token_expire_handler(request):
    """
    This check is for a user who login into their account only (request.user).
    If the user creates a one-time account, takes the token, and does not return to their account,
    the token will still be valid until their account is deleted based on their account destruction period.
    """
    token_obj = Token.objects.filter(user=request.user)
    token_values_list = token_obj.values_list("created", flat=True)[0].date()
    today = datetime.date.today()
    time_elapsed = (today - token_values_list).days
    if time_elapsed > settings.TOKEN_EXPIRATION_PERIOD:
        token_obj.delete()
        token_obj.create(user=request.user)
