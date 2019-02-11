import ipaddress

from constants import PRIVATE_IPS_PREFIX


def is_valid_ip(ip_address):
    """ Check Validity of an IP address """

    try:
        ipaddress.ip_address(u'' + ip_address)
        return True
    except ValueError:
        return False


def is_local_ip(ip_address):
    """ Check if IP is local """

    try:
        ip = ipaddress.ip_address(u'' + ip_address)
        return ip.is_loopback
    except ValueError:
        return None


def get_ip_address_from_request(request):
    """ Makes the best attempt to get the client's real IP or return the loopback """
    ip_address = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for and ',' not in x_forwarded_for:
        if not x_forwarded_for.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_forwarded_for):
            ip_address = x_forwarded_for.strip()
    else:
        ips = [ip.strip() for ip in x_forwarded_for.split(',')]
        for ip in ips:
            if ip.startswith(PRIVATE_IPS_PREFIX):
                continue
            elif not is_valid_ip(ip):
                continue
            else:
                ip_address = ip
                break
    if not ip_address:
        x_real_ip = request.META.get('HTTP_X_REAL_IP', '')
        if x_real_ip:
            if not x_real_ip.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_real_ip):
                ip_address = x_real_ip.strip()
    if not ip_address:
        remote_addr = request.META.get('REMOTE_ADDR', '')
        if remote_addr:
            if not remote_addr.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(remote_addr):
                ip_address = remote_addr.strip()
    if not ip_address:
        ip_address = '127.0.0.1'
    return ip_address
