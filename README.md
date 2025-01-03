# 1. **Descripción**
 Esta es la API junto al backend de la app de mi huerto. Aqui se puede ver como interactuamos con MQTT para recoger la info de los sensores, como almacenamos la informacion interesante el la base de datos para asi despues poder usarla y mostrarla.
 Tambien usamos un repositorio para interactuar con meross ya que usamos las regletas WiFi de meross, pero he complementado el repo con una pequeña actualizacion para crear y modificar rutinas. Esto lo he podido lograr haciendo una pequeña ing. inversa a la API, ya que en el repositorio que uso explican como funciona tanto la API como MQTT de meross. Con burp suite he interceptado las urls necesarias y he implementado las rutinas.
 Tambien destacar mi codigo C para los arduino ya que funciona mediante tokens. pasar url al git de mi codigo de mqtt de dht22 por ejemplo.

 # 2. **Instalación**

 Importante si se usa con Djongo, instalar los requeriments y tener cuidado con las versiones por tema de compatibilidad.
 ```
pip install -r requeriments.txt
```
# 3. **Configuración**
Dentro de Auth/Auth/ hay varios archivos para configurar:
Para configurar la base de datos
Archivo settings.py:
```
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'NAMEDB',
        'ENFORCE_SCHEMA': False,
        "CLIENT": {
            'host': 'mongodb://USSER:PASSWORD@IPDB:PORTDB/NAMEDB',
        }
    }
}

```

Seguridad:

Archivo mw.py
```
if not ip_address.startswith('192.168.'):
```
Esta linea revisa si la conexion procede de red interna local.

```
if not (country_code == 'ES') and ip_address not in ['54.38.180.107','45.135.180.216']:
```
Si no es local, revisa que la conexion sea Española y que sea de nuestros servidores, si no es asi error.
En caso de no querer usar esto anterior dentro de Auth/settings.py dentro de los MiddleWare:
```
MIDDLEWARE = [
    'auth.mw.RestrictIPMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```
Quitar la linea de "'auth.mw.RestrictIPMiddleware'," y listo.
