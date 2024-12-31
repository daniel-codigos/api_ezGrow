from ipwhois import IPWhois
from django.http import HttpResponseForbidden

class RestrictIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtén la dirección IP del cliente
        ip_address = request.META.get('REMOTE_ADDR')
        print(ip_address)
        try:
            if not ip_address.startswith('192.168.'):
                # Obtiene la información de geolocalización para la dirección IP
                obj = IPWhois(ip_address)
                result = obj.lookup_rdap()
                print(result)
                # Verifica si el país es España o si la IP está en el rango 192.168.x.x
                country_code = result.get('asn_country_code')
                print(country_code)
                if not (country_code == 'ES') and ip_address not in ['54.38.180.107','45.135.180.216']:
                    return HttpResponseForbidden("Acceso denegado. Solo se permite acceso desde España o desde la red interna.")


        except Exception as e:
            print(f"Error al obtener la información de geolocalización: {e}")

        return self.get_response(request)
