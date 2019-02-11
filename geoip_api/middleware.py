import geoip2.database
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from constants import PATH_TO_DB
from utils import is_local_ip, is_valid_ip, get_ip_address_from_request


class TimezoneMiddleware(MiddlewareMixin):
    reader = geoip2.database.Reader(PATH_TO_DB)

    @classmethod
    def process_request(cls, request):
        tz = request.session.get('django_timezone')
        if not tz:
            # use the default timezone (settings.TIME_ZONE) for localhost
            tz = timezone.get_default_timezone()
            client_ip = get_ip_address_from_request(request)
            ip_addresses = client_ip.split(',')
            for ip in ip_addresses:
                if is_valid_ip(ip) and not is_local_ip(ip):
                    response = cls.reader.city(ip)
                    tz = response.location.time_zone
        if tz:
            timezone.activate(tz)
            request.session['django_timezone'] = str(tz)
        else:
            timezone.deactivate()
