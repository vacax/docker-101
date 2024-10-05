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
`docker exec -it u1 /bin/bash` - Podemos ejecutar un comando en el contenedor.

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
Entre al contenedor creado.

![Esquema de Comunicación](/imagenes/diagrama-conexion.png)

Si entramos al contenedor `docker attach mi-u1` y una vez dentro ejecutamos los siguientes
comandos: `service apache2 start && nmap localhost`. Puede verificar mediante la dirección
[http://localhost:8080/](http://localhost:8080/) que el servicio está respondiendo

### Volúmenes en los contenedores

* Toda la información que es almacenada en el contenedor, una vez es destruido se pierde para siempre.
* Los volúmenes son como discos duros virtuales administrados por Docker. Docker maneja el almacenamiento en disco (generalmente en /var/lib/docker/volumes/)
* Docker nos permite habilitar volúmenes de datos donde asociamos una carpeta del host con una del contenedor.
* Los volúmenes tienen una relación bidireccional, es decir, si se modifica en el host se modifica en el contenedor y viceversa.
* Para gestionar los volúmenes tenemos el comando `docker volume help` y visualizamos todas las opciones.

Para crear un volumen podemos usar el comando: `docker volume create nombre-volumen` o asociarlo directamente 
al contenedor indicando la carpeta en el host, con el parámetro **-v carpeta-host:carpeta-contenedor**.

Vamos a trabajar con nuestro ejemplo, con el siguiente comando:

`docker run --name mi-u1 -d -it --rm -p 8080:80 -v /website:/var/www/html mi-primera-imagen` - Verificar que el parámetro
**-v**, donde en el host tendremos la carpeta del **website** asociada a la carpeta **/var/www/html mi-primera-imagen**.

Vamos a modificar el site de inicio con el siguiente mensaje:

`echo "JCONF DOMINICANA 2022" > /website/index.html`

Accediendo a la ruta [http://localhost:8080/](http://localhost:8080/) podremos ver el mensaje.

Si eliminamos el contenedor con el comando `docker stop mi-u1` notaremos que la carpeta e información estará disponible en el host y
si creamos nuevamente el contenedor e iniciamos el servicio tendremos la información almacenada.

Otra forma de aplicar los mismos conceptos es mediante la creación del volumen no vinculante a aun carpeta,
mediante el comando `docker volume create vol-website` y sustituyendo previo por el siguiente: `docker run --name mi-u1 -d -it --rm -p 8080:80 -v vol-website:/var/www/html mi-primera-imagen` 
con el comando `docker inspect mi-u1`, buscamos la sección **Mounts** y podemos ver donde se almacena la información. 

### Comunicación entre contenedores

* Los contenedores no ven la IP externa del host al cual están conectados de forma directa.
* Cada contenedor tiene su propio esquema de direccionamiento IP, desde el contenedor el nombre localhost representa el mismo contenedor, no el host.
* Docker maneja el direccionamiento interno de las peticiones entre contenedores siempre y cuando pertenezcan a una misma red.
* Para la creación de la red, nos auxiliamos del comando `docker network create <<nombre-de-la-red>>`.
* Cada contenedor que estará comunicándose es requerido indicar el parámetro **-network** en la definición del contenedor.

Para realizar la comunicación entre los contenedores, vamos a trabajar con el siguiente esquema: 

![Relacion Contenedores por Red](/imagenes/esquema-app-red.png)

Las imágenes que estaremos son las siguientes:

* `docker pull mysql:5.7.38`
* `docker pull vacax/micro-servicio-estudiante:latest` - Ver fuente: [https://github.com/vacax/micro-servicios-estudiante](https://github.com/vacax/micro-servicios-estudiante)

Vamos a crear una red que permita la comunicación entre los dos contenedores:

`docker network create mi-red`

La creación de los contenedores de la base de datos:

`docker run --name mysql-interno -v ~/datadir_mysq_otrol:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=12345678 -e MYSQL_DATABASE=micro_estudiante -d --rm --network mi-red mysql:5.7.38` -
Ver el parámetro **network** con el valor **mi-red** y la introducción de variables de ambientes para el contenedor
con el parámetro **-e** con los valores **MYSQL_ROOT_PASSWORD** para mencionar uno. Notar que no está abierto el puerto para el host.

La creación de la aplicación:

`docker run --name bo-micro-estudiante -e spring.datasource.url="jdbc:mysql://mysql-interno:3306/micro_estudiante" -p 8090:8080 --rm -d --network mi-red vacax/micro-servicio-estudiante`

Los logs de cada una de los contenedores podemos de verlo de:

* `docker logs -f bo-micro-estudiante`
* `docker logs -f mysql-interno`

El servicio está funcionando y podemos interactuar con el servicio:

`curl -X POST <<URL>>
-H 'Content-Type: application/json'
-d '{"matricula":20011136,"nombre":"Carlos Camacho", "carrera": "ITT"}'`

### Los recursos utilizados

Para ver los recursos y la relación de los procesos podemos utilizar el comando: 

`docker stats`

Puedo limitar el uso la memoria con el parámetro **--memory valor** o la cpu con **--cpuset-cpus valor** 

## Archivo Dockerfile

* Nos permite agilizar y automatizar la creación de imágenes para nuestros contenedores.
* Creamos un archivo con las instrucciones necesarias para crear nuestra imagen.
* El archivo se llama Dockerfile y utilizamos una serie de instrucciones para uso.

### Instrucciones 

- `FROM` - Indicamos la imagen que estaremos utilizando y su versión. Conviene especificar versión para que el contenedor funcione si la versión de la imagen se modifica. Recomendación de utilizar imágenes basadas en `alpine` (como `tag`) por su poco *overhead* agregado a las aplicaciones.
- `WORKDIR` - Declara la ruta en la que se va a trabajar dentro del contenedor, si no existe, se creará.
- `COPY` - Copia todos los archivos que se le indiquen a una ruta determinada del contenedor. `COPY . .` copia todos los archivos de nuestra carpeta al `WORKDIR`.
- `RUN` - Comando que se ejecuta al construir la imagen del contenedor.
- `CMD` - Comando que se ejecuta por defecto cuando se ejecuta la imagen del contenedor
- `ENTRYPOINT` - Permite dejar abierto un comando para pasarle argumentos. Al hacer `docker run` habrá que pasarle un argumento, tal que: `docker run argumento`.
- `EXPOSE` - Indica los puertos que estaremos permitiendo conexión al contenedor.
- `ENV` - Crear variables de ambiente en el contenedor.
- `ADD` - Añade un fichero de la máquina host a la imagen y permite consultas a URL.
- `VOLUME` - Permite crear un punto de montaje externo al contenedor, se utiliza para persistir la información generada por los contenedores.

### ¿Entrypoint o CMD?

* Los contenedores están diseñados para ejecutar una tarea o un proceso, no para "hostiar" un sistemas operativo.
* Cuando el proceso o tarea termina el contenedor termina.
* En Docker tenemos las instrucciones CMD o ENTRYPOINT para definir un comando que se ejecutará por defecto.
* ENTRYPOINT es la aplicación principal y el CMD será los parámetros que estaremos enviando.

Vamos a ejecutar el archivo [Dockerfile EntryPoint](cmd-entrypoint/Dockerfile), para construir una imagen 
desde un archivo Dockerfile utilizamos el siguiente comando `docker build -t mi-dockerfile .` donde se encuentra el
archivo Dockerfile. 

Si ejecutamos `docker images` podemos la imagen creada. Si ejecutamos un contenedor `docker run mi-dockerfile`, notar la salida.
Si ejecutamos `docker run mi-dockerfile "JCONF Dominicana 2022"` ver como sobreescribimos el segundo parámetro de CMD.

### Dockerfile de nuestra imagen web

Ejecutar el archivo [Dockerfile ServidorWeb](archivo/Dockerfile), para construir nuestra imagen lista para servir páginas web.
Ejecutamos el comando `docker build -t mi-apache .` y corremos el contenedor `docker run -p 8080:80 --rm -d mi-apache`.

### Uso de .dockerignore

Ver la información en [Uso de Dockerignore](/uso-dockerignore/README.md)

### Subir nuestra imagen a Docker Hub

* Es necesario disponer de un usuario, registrase en el servicio. 
* Para preparar una imagen aplicamos el siguiente comando: `sudo docker tag nombre_imagen_local id_usuario/nombre_a_subir`. 
* Para enviar una imagen:  `sudo docker push id_usuario/nombre_a_subir`.

### Multistage build en Docker

Fue incluido en la versión 17.05 permitiendo que podamos separar la fase de preparación o compilación
de nuestro código evitando que nuestras imágenes sean muy grandes. Anteriormente el esquema utilizado es "todo en uno".

Veamos un ejemplo de un DockerFile del tipo **Todo en Uno** en el siguiente enlace:
[Dockerfile Todo en Uno](https://github.com/vacax/orm-jpa/blob/master/Dockerfile-todoenuno). Si compilamos la imagen y 
validamos el tamaño con `docker images <<nombre-imagen>>`, notarán su gran tamaño.

Utilizando el concepto de Multistage, podemos evitar la descarga o carga en la imagen de software de compilación
que no tienen sentido una vez se ejecuta la imagen, ver ejemplo en siguiente enlace: [Docker Multistage](/multi-stage/Dockerfile).
Notar nuevamente tamaño y compararlo con la otra imagen generada.


## Docker Compose

### ¿Qué es?

* Es una herramienta para facilitar el proceso de creación y gestión de los contenedores Docker que están asociados entre sí en un **Host**.
* Es representado por un archivo de en formato YAML donde permite configurar los contenedores con una sintaxis mucho más simple, llamado por defecto `docker-compose.yaml`.
* La instalación y documentación puede ser accedida desde: https://docs.docker.com/compose/ y https://docs.docker.com/compose/install/, no es parte del motor de Docker.
* Permite la configuración de las variables de ambientes: https://docs.docker.com/compose/environment-variables/

### Estructura del Archivo 

El archivo `docker-compose.yaml`, está estructurado en secciones las más relevantes son:

* `version` - La versión de la sintaxis de lo que se está incluyendo en el archivo yaml.
* `services` - Indica los servicios (contenedores) que estaremos utilizando.
* `networks` - Permite definir las redes que estarán utilizando los contenedores. De forma implícita todos los servicios pertenecen a la misma red.
* `volumes` - Permite la creación de los volúmenes de datos.

### Ejemplo un servicio con Docker compose

Ver la configuración en docker-compose para nuestro ejemplo que hemos estado trabajando 
en el siguiente enlace: [Servicio Docker Compose](/docker-compose/docker-compose.yaml).
El proyecto original se encuentra en https://github.com/vacax/micro-servicios-estudiante. 

Del archivo podemos notar como la información de configuración para cada servicio utilizamos
variables de ambientes, disponemos de la instrucción `depends_on` donde indicamos el orden de 
inicialización de los servicios.

El esquema estaremos utilizando:

![Esquema Docker Compose](/imagenes/esquema-docker-compose.png)

### Ejecución del Docker Compose

* `docker compose up -d` - La opción `-d` permite que los servicios se ejecuten como servicios.

### Para del servicio y eliminar instancias

* `docker compose down` - Borrará todo el contenido y la red, pero los datos persistirán si se comparte un volumen.

### Comandos útiles de docker-compose

- `docker compose up`
- `docker compose stop`
- `docker compose start`
- `docker compose down`
- `docker compose ps`
- `docker compose logs` 
