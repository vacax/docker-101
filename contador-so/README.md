# contador-so

Aplicación de apoyo para la práctica de contenedores de **ICC-331 Sistemas Operativos (PUCMM)**.
Código en <https://github.com/vacax/docker-101/tree/master/contador-so> (Anexo A del enunciado).

Es una aplicación web mínima en Python (un solo archivo, `app.py`) que cuenta visitas en **Redis** y
muestra lo que el proceso "ve" del sistema operativo **desde dentro del contenedor**. La aplicación
ya está terminada: el trabajo de la práctica es **configurarla** (Dockerfile y Docker Compose),
no programar.

```text
$ curl http://localhost/
Hola desde Docker Compose - ICC331
Visitas            : 39
Hostname           : 67973ddd0307          <- namespace UTS (ID del contenedor)
PID                : 1                     <- namespace PID
Usuario (uid:gid)  : 100:101               <- ¿root o no?
Kernel             : 7.0.0-42-generic      <- el mismo del host
memory.max         : 268435456             <- límites del cgroup (256 MB)
cpu.max            : 50000 100000          <-                     (0.5 CPU)
pids.max           : 100                   <-                     (100 procesos)
Capabilities (Eff) : 0000000000000000      <- cap_drop: ALL
Raíz solo lectura  : sí (Read-only file system)
Logs               : /var/log/contador/accesos.log
```

## Configuración

| Variable de ambiente | Por defecto | Uso |
|---|---|---|
| `PUERTO` | `8000` | Puerto HTTP donde escucha |
| `REDIS_HOST` | `redis` | Nombre del servicio Redis (en Compose, el nombre del servicio) |
| `REDIS_PORT` | `6379` | Puerto de Redis |
| `MENSAJE` | `Hola desde un contenedor` | Texto de saludo |
| `DIRECTORIO_LOGS` | `/var/log/contador` | Carpeta del archivo `accesos.log` (debe ser un volumen y el usuario de la app debe poder escribir en ella) |

| Ruta | Respuesta |
|---|---|
| `GET /` | Información del contenedor + contador de visitas |
| `GET /salud` | `200 OK` si Redis responde, `503` si no. Úsela en `HEALTHCHECK` |
| `GET /consumir?mb=N` | Reserva N MB de memoria y no los libera. Sirve para alcanzar el límite del cgroup |

Dependencias: `requirements.txt` (cliente `redis`). Arranque: `python app.py`.
La aplicación maneja `SIGTERM` para cerrar enseguida cuando es el PID 1.

## Ejecutar sin Docker (opcional, para entenderla)

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
docker run -d --name redis-local -p 6379:6379 redis:7.4-alpine
REDIS_HOST=localhost python app.py
curl http://localhost:8000/
```

## Lo que debe configurar en la práctica

1. **Dockerfile multi-stage**: una etapa instala dependencias (`pip install` en un entorno virtual) y la final
   copia solo el entorno y `app.py` sobre una imagen mínima (`python:3.12-alpine` o `-slim`).
   Usuario no root, `ENTRYPOINT` en forma exec, `HEALTHCHECK` contra `/salud`.
   Cree la carpeta de logs en la imagen con el dueño correcto para que el volumen herede los permisos.
2. **Docker Compose**: servicios `app` (única publicada en el host, `ports: "80:8000"`) y `redis`
   (`redis:7.4-alpine`, sin `ports`), una red propia, volúmenes para los datos de Redis y los logs,
   límites de recursos, `read_only`, `tmpfs`, `cap_drop`, `depends_on` con `condition: service_healthy`,
   `restart: unless-stopped` y un archivo `.env`.
