# Como usuar CMD y Entrypoint.

Por defecto el Entrypoint en imágenes de Ubuntu es ENTRYPOINT ["/bin/sh", "-C"] y el comando es "/bin/bash", el Entrypoint es el programa que siempre se estará ejecutando y el CMD es la instrucción que es pasada al entrypoint. Se utiliza para convertir una imagen de Docker en un programa.