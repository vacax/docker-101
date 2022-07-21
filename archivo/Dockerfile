#
FROM ubuntu
#Creando al variable de ambiente necesario para evitar la configuración del Timezone de la librería tzdata.
# Tomado de https://rtfm.co.ua/en/docker-configure-tzdata-and-timezone-during-build/
ENV TZ=America/Santo_Domingo
#Creando los archivos necesarios.
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# Ejecutando la instalación de apache.
RUN apt update && apt install -y apache2 systemd && systemctl enable apache2
# Indicando el puerto para exponer por la imagen.
EXPOSE 80
# Moviendo el archivos a la ruta por defecto para apache.
COPY index.html /var/www/html/

# Ejecutando apache2 como servicio.
ENTRYPOINT ["apachectl", "-D", "FOREGROUND"]