import pytz
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # make sure they are authenticated so we know we have their tz info.
        if request.user.is_authenticated:
            # we are getting the users timezone string that in this case is stored in
            # a user's profile
            tz_str = request.user.country.code
            if tz_str:
                time_zone_countries = pytz.country_timezones(tz_str)
                for time_zone_l in time_zone_countries:
                    timezone.activate(pytz.timezone(time_zone_l))
            else:
                timezone.deactivate()
        # otherwise deactivate and the default time zone will be used anyway
        else:
            timezone.deactivate()

        response = self.get_response(request)
        return response


class UpdateLastActivityMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            request.user.last_activity_date = timezone.now()
            request.user.save()


class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                stored_session_key = request.user.logged_in_user.session_key
            except:
                logout(request)
            try:
                if stored_session_key and stored_session_key != request.session.session_key:
                    Session.objects.get(session_key=stored_session_key).delete()
            except:
                pass
            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()
        response = self.get_response(request)
        return response
