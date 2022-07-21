# Ejemplo de la diferencia de cmd vs entrypoint.
FROM ubuntu
RUN apt-get update && apt-get install -y --no-install-recommends cowsay
# Indicando el ambiente para usar la librería
ENV PATH "$PATH:/usr/games"
# Típico ejemplo de como cambiar el comportamiento de contenedor, cuando pasameos el comando al contenedor estaremos aplicando el cat.
# en vez del bash. Por defecto si no es especificado el valor es /bin/sh -c
ENTRYPOINT [ "cowsay", "Desde EntryPoint" ]
CMD [" Desde CMD"]
