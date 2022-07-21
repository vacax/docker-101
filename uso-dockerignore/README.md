# Uso del dockerignore para trabajar con la creación de images

Cuando trabajamos con la construcción de la imagen todos los ficheros donde se encuentra el archivo
se estará enviando al contexto de docker aunque no se utilicen. Para evitar eso trabajamos con
`.dockerignore`.

Si ejecutamos si creamos la imagen:

`docker build -t mi-java .` - Notar lo rápido que estará generando la imagen.

¿Qué pasa si tenemos archivos no necesarios para generación de la imagen?.

`fallocate -l 5G muchos-archivos`

Tratamos nuevamente de generar la imagen:

`docker build -t mi-java .` - Notar el tiempo que demora en completar el contexto y peso de los archivos del contexto.

Con el archivo `.dockerignore`, muy parecido al gitignore podemos excluir los archivos que no deben
estar en el contexto de la imagen. Descomentar la línea dentro del archivo y volver a generar la imagen.
Notar el tamaño de los archivos que participan en el contexto, vuelve a disminuir el tiempo.
