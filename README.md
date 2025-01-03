# 1. **Descripción**
 Esta es la API junto al backend de la app de mi huerto. Aqui se puede ver como interactuamos con MQTT para recoger la info de los sensores, como almacenamos la informacion interesante el la base de datos para asi despues poder usarla y mostrarla.
 Tambien usamos un repositorio para interactuar con meross ya que usamos las regletas WiFi de meross, pero he complementado el repo con una pequeña actualizacion para crear y modificar rutinas. Esto lo he podido lograr haciendo una pequeña ing. inversa a la API, ya que en el repositorio que uso explican como funciona tanto la API como MQTT de meross. Con burp suite he interceptado las urls necesarias y he implementado las rutinas.
 Tambien destacar mi codigo C para los arduino ya que funciona mediante tokens. pasar url al git de mi codigo de mqtt de dht22 por ejemplo.

 
