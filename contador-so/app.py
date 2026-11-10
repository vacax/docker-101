"""
contador-so: aplicación web mínima para la práctica de contenedores de ICC-331.

Cuenta visitas en Redis y muestra lo que el proceso "ve" del sistema operativo
desde dentro del contenedor: hostname, PID, usuario, kernel, límites del cgroup,
capabilities y si el sistema de archivos raíz es de solo lectura.

Configuración (variables de ambiente):
    PUERTO          puerto HTTP                         (por defecto 8000)
    REDIS_HOST      host de Redis                       (por defecto redis)
    REDIS_PORT      puerto de Redis                     (por defecto 6379)
    MENSAJE         texto de saludo                     (por defecto "Hola desde un contenedor")
    DIRECTORIO_LOGS carpeta del archivo de accesos      (por defecto /var/log/contador)

Rutas:
    GET /                 información del contenedor + contador de visitas
    GET /salud            200 si Redis responde, 503 si no (para HEALTHCHECK)
    GET /consumir?mb=N    reserva N MB de memoria (para probar el límite del cgroup)
"""
import os
import signal
import socket
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import redis

PUERTO = int(os.getenv("PUERTO", "8000"))
MENSAJE = os.getenv("MENSAJE", "Hola desde un contenedor")
DIRECTORIO_LOGS = os.getenv("DIRECTORIO_LOGS", "/var/log/contador")

bd = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=int(os.getenv("REDIS_PORT", "6379")),
                 socket_timeout=2, socket_connect_timeout=2)
memoria_reservada = []


def leer(ruta, por_defecto="(no disponible)"):
    try:
        with open(ruta) as f:
            return f.read().strip()
    except OSError:
        return por_defecto


def capabilities():
    for linea in leer("/proc/self/status", "").splitlines():
        if linea.startswith("CapEff:"):
            return linea.split()[1]
    return "?"


def raiz_solo_lectura():
    try:
        with open("/.prueba-escritura", "w") as f:
            f.write("x")
        os.remove("/.prueba-escritura")
        return "no"
    except OSError as e:
        return f"sí ({e.strerror})"


def registrar(linea):
    try:
        os.makedirs(DIRECTORIO_LOGS, exist_ok=True)
        with open(os.path.join(DIRECTORIO_LOGS, "accesos.log"), "a") as f:
            f.write(linea + "\n")
    except OSError as e:
        print(f"No se pudo escribir el log en {DIRECTORIO_LOGS}: {e}", file=sys.stderr, flush=True)


class Manejador(BaseHTTPRequestHandler):

    def responder(self, codigo, texto):
        cuerpo = texto.encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/salud":
            try:
                bd.ping()
                self.responder(200, "OK\n")
            except redis.RedisError as e:
                self.responder(503, f"Redis no disponible: {e}\n")
            return

        if url.path == "/consumir":
            mb = int(parse_qs(url.query).get("mb", ["50"])[0])
            memoria_reservada.append(bytearray(mb * 1024 * 1024))
            total = sum(len(b) for b in memoria_reservada) // (1024 * 1024)
            self.responder(200, f"Reservados {mb} MB (total {total} MB)\n")
            return

        if url.path != "/":
            self.responder(404, "No encontrado\n")
            return

        try:
            visitas = bd.incr("visitas")
        except redis.RedisError as e:
            visitas = f"(error: {e})"
        registrar(f"{datetime.now().isoformat()} {self.client_address[0]} {socket.gethostname()}")

        self.responder(200, f"""{MENSAJE}
Visitas            : {visitas}
Hostname           : {socket.gethostname()}
PID                : {os.getpid()}
Usuario (uid:gid)  : {os.getuid()}:{os.getgid()}
Kernel             : {os.uname().release}
memory.max         : {leer('/sys/fs/cgroup/memory.max')}
cpu.max            : {leer('/sys/fs/cgroup/cpu.max')}
pids.max           : {leer('/sys/fs/cgroup/pids.max')}
Capabilities (Eff) : {capabilities()}
Raíz solo lectura  : {raiz_solo_lectura()}
Logs               : {DIRECTORIO_LOGS}/accesos.log
""")

    def log_message(self, formato, *args):
        # salida estándar -> docker logs
        print(f"{self.client_address[0]} {formato % args}", flush=True)


def detener(signum, _frame):
    print(f"Señal {signal.Signals(signum).name} recibida, cerrando...", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    # Como PID 1 en un contenedor, el kernel no aplica la acción por defecto de SIGTERM:
    # si no hay manejador, docker stop espera 10 s y termina con SIGKILL.
    signal.signal(signal.SIGTERM, detener)
    print(f"contador-so escuchando en el puerto {PUERTO} (PID {os.getpid()})", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PUERTO), Manejador).serve_forever()
