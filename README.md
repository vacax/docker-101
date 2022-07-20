# Taller práctico sobre uso de Docker para Principiantes - Docker 101

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

`docker attach u1` - Notar como cambia la terminal con el ID del contenedor.

Dentro del contenedor ejecutar el siguiente comando:
`echo "Informacion en Ubuntu U1" > mi_archivo.txt`

Ejecute el comando `exit`, visualice los contenedores activos y vea el estatus del contenedor.

Vamos a inicializar el contenedor nuevamente, para ello usamos el comando:

`docker start u1` - Inicializamos nuevamente el contenedor por su nombre o ID.

Entramos al contenedor **u1**, con el comando:

`docker attach u1`

Dentro del contendor podemos visualizar que el archivo creado está disponible, ejecutar el comando `ls -l`. 
La forma correcta para salir del contenedor intectativo, sin cerrar el contenedor (entrypoint) es utilizando la combinación **crtl + p + q**

Vamos a crear un nuevo contenedor basado en la imagen de ubuntu:

`docker run --name u2 -d -it ubuntu `

Acceda dentro del contenedor y notará que el archivo anteriormente creado no está disponible. Cada contenedor es diferente uno de otro. 
La información almacenada una vez eliminado el contenedor se perderá. 
Cuando trabajamos con información que debe ser persistente trabajamos con **volúmenes**. 

### Creando nuestra primera imagen

Conectados al contener llamado **u1**, vamos a instalar algunos software que necesitamos:

`TZ=America/Santo_Domingo && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && apt update && apt install -y apache2 nmap systemd && systemctl enable apache2 && service apache2 start `

Ejecute el comando `nmap localhost`, debe ver el puerto 80 abierto. Salga del contenedor con el comando `exit` y ejecute el siguiente comando:

`docker commit u1 mi-primera-imagen`

Si ejecutamos el comando `docker images` notaremos nuestra nueva imagen creada. Es importante verificar el tamaño, 
representa la diferencia de la imagen base y los cambios que incluimos.

### Creando nuestro primer contenedor de nuestra imagen

Una vez contamos con una imagen, podemos generar cuanto contenedores necesitemos, para ellos utilizamos nuestro comando `docker run`,
probemos con el siguiente:

`docker run --name mi-u1 -d -it --rm mi-primera-imagen` - La opción **--rm** elimina el contenedor una vez concluya su proceso activo (entrypoint).

Si entramos al contenedor creado con el comando `docker attach mi-u1`, podemos ver que tenemos disponibles los comandos 
y servicios previamente instalados. Ejecute el siguiente comando:

`service apache2 start && nmap localhost`

Debe visualizar que el puerto 80 está activo. ¿Cómo accedemos a ese servicio?, es necesario abrir el puerto del contenedor
para acceder desde el host. Salga del contenedor con el comando: `exit`. Notar que el contenedor fue eliminado una vez detenido.

### Abriendo los puertos del contenedor

* Cada contenedor está aislado incluyendo la red.
* Es necesario indicar de forma explícita los puertos que estaremos abriendo.

Para nuestro caso, volvamos a crear un nuevo contenedor utilizando nuestra imagen, bajo el comando:

`docker run --name mi-u1 -d -it --rm -p 8080:80 mi-primera-imagen` - El parámetro **-p** indica el puerto abierto en el host
asociado al puerto del contenedor, en nuestro caso puerto 8080 del host con el puerto 80 del contenedor. 
Entre al contenedor creado

### Conexión entre contenedores

*