import os

PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', '127.')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_TO_DB = os.path.join(BASE_DIR, "GeoLite2-City.mmdb")
