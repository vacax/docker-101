# Taller práctico sobre el uso de Docker para Principiates - Docker 101

## Conceptos Básicos

### Problemas en la puesta en marcha de aplicaciones

* Los entornos de desarrollo, prueba y producción son muy diferentes. 
* Garantizar que la aplicación desarrollada y probada tengan el mismo comportamiento es complicado.
* El uso de máquinas virtuales (VM) agrega complejidad a la hora de gestionar las actualizaciones y el incremento de recursos.
* Garantizar el aislamiento de los procesos requiere destinar recursos (VM, equipos físicos, entre otros).
* Cada día el uso de La Nube complejiza los despliegues de las aplicaciones.

### ¿Qué ocurre con las máquinas virtuales?.

* Utilizamos las VM para correr aplicaciones, sacando el mayor rendimiento al hardware. 
* Una manera muy sencilla de brindar aislamiento entre aplicaciones.
* Dicho aislamiento tiene un costo en poder computacional utilizado por el S.O. invitado (Guest).

![Esquema Maquinas Virtuales !](/imagenes/esquema-vm.png)

### ¿Qué son los Contenedores?.

* Tienen como objetivo brindar un ambiente de ejecución homogéneo independiente del S.O o ambiente que lo ejecute.
* Aprovechan las librerías y los recursos del S.O anfitrión eliminando los problemas de las VMs. 
* Tienen como objetivo la estandarización en el transporte y despliegue de aplicaciones.

![Esquema Contenedores !](/imagenes/esquema-contenedor.png)

Realizan una analogía del sistema del transporte Mundial, como es presentando en la imagen más abajo,
por eso su nombre.

![Analogía Contenedores!](/imagenes/analogia-contenedores.png)

--- 
## Docker

### ¿Qué es?

* Es un producto Open Source que implementa los conceptos de contenedores desde el 2013. (Ahora la industria con [Containerd](https://containerd.io/))
* Es el estándar de-facto a la hora de implementar los contenedores.
* Posee mucha documentación y una comunidad muy activa.
* Soporte empresarial.
* Una gran cantidad de proyectos en uso en producción.

### Características de Docker

* Ligeros. 
* Portables.
* Inmutables.
* Basado en Linux para las imágenes o Windows (dependiendo del contenedor).
* Escalabilidad.

### Tecnología de Docker

**Linux Kernel**:
* Cgroups.
* Kernel namespaces. 
* Union File-system.
* Libvirtt y LXC.

**GIT**:
* Controla los cambios en las imágenes.

![Cambios Imagenes!](/imagenes/cambios-imagenes.png)

### Componentes en Docker

* Cliente Docker (CLI).
* Motor de Docker.
* Registro Docker.
* Imágenes
* Contenedores.


![Arquitectura Docker!](/imagenes/arquitectura-docker.png)

### Imágenes de Docker

* Es el fichero binario con toda la estructura del software trabajado que estaremos utilizando como contenedor.
  Representa una plantilla.
* Se utilizan para crear contenedores.
* Nunca cambian una vez creada, cada modificación representa una nueva imagen.
* Utilizando un archivo de configuración (DockerFile) podemos crear imágenes de una manera sencilla.

### Contenedor de Docker

* Usan las imágenes como plantillas y pueden contener uno o más de un proceso.
* Es una instancia de una imagen (muy parecido al concepto de Objeto).
* Están asociados al ciclo de vida de Crear, Destruir, Arrancar, Reiniciar o Parar. 
* Representan el entorno de ejecución.

### Relación Imagen y Contenedor

![Relacion Imagen Contenedor](/imagenes/relacion-imagen-contenedor.png)

## Inicio del Taller

### Cuentas para crear

* Cuenta en Docker Hub: [https://hub.docker.com/](https://hub.docker.com/)
* Play With Docker: [https://labs.play-with-docker.com/](https://labs.play-with-docker.com/)

### Primeros Comandos (Básicos):

* `docker version` - Nos permite visualizar la versión de Docker.
* `docker images` - Nos muestra todas las imágenes descargadas.
* `docker ps` - Nos presenta todos los contenedores activos.
* `docker ps -a` - Muestra todos los contenedores creados sin importar su estatus.

### Descarga de nuestra primera imagen:

* `docker pull busybox` - Descarga la última versión de la imagen de [Busybox](https://es.wikipedia.org/wiki/Busybox) y en [ Hub Docker](https://hub.docker.com/_/busybox).
* `docker images` - Debemos visualizar la imagen descargada.

### Ejecutando nuestra primer contenedor:

* `docker run busybox echo "Hola Mundo en Docker - JConf Dominicana 2022"` - Ejecuta el comando **echo** directamente desde la imagen.  
* `docker ps -a` - Debemos visualizar el contenedor con el estatus finalizado.

Ejecutamos nuevamente el comando y cada ejecución crea un nuevo contenedor y asigna un nombre por aleatorio.

### Modificando nuestra primera imagen

Vamos a crear descargar una imagen de Ubuntu es su ultima versión:

`docker pull ubuntu`

Una vez descargada vamos a trabajar directamente en un contenedor:

`docker run --name u1 -d -it ubuntu` - **--name**, asignamos un nombre a nuestro contenedor, no puede repetirse, **-d** crear el contenedor modo servicio, **-it** modo interactivo.

Verificar que el contenedor está arriba:

`docker ps`

Accedemos al contenedor mediante el comando:

`docker attach u1` - Notar como cambiar la terminar con el ID del contenedor.