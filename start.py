import os
import sys
import time
import socket
import threading
import traceback
import webview

# 🔥 BASE_DIR siempre apunta a _internal dentro del exe
if hasattr(sys, '_MEIPASS'):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔥 Agregar rutas ANTES de cualquier import de Django o apps
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "hospital"))

# Verificar que las apps están en el path
for app in ['usuarios', 'pacientes', 'medicos', 'empleados', 
            'citas', 'dashboard', 'historiaclinica', 'internacion',
            'inventario', 'facturas', 'evolucion']:
    app_path = os.path.join(BASE_DIR, app)
    if os.path.exists(app_path):
        sys.path.insert(0, os.path.dirname(app_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hospital.settings")

LOG_PATH = os.path.join(os.path.dirname(sys.executable), "error_log.txt")

def log(msg):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

log(f"=== Inicio ===")
log(f"BASE_DIR: {BASE_DIR}")
log(f"sys.path: {sys.path[:5]}")

import django
django.setup()

import usuarios.models
from django.core.management import execute_from_command_line

def iniciar_servidor():
    try:
        log("Iniciando servidor Django...")
        execute_from_command_line([
            "manage.py", "runserver", "127.0.0.1:8000", "--noreload"
        ])
    except Exception as e:
        log("ERROR en servidor:")
        log(traceback.format_exc())

def esperar_servidor():
    log("Esperando servidor...")
    for i in range(30):
        try:
            with socket.create_connection(("127.0.0.1", 8000), timeout=1):
                log("Servidor listo.")
                return True
        except:
            time.sleep(1)
    log("ERROR: servidor no respondió en 30 segundos.")
    return False

if __name__ == "__main__" and not os.environ.get("RUN_MAIN"):
    threading.Thread(target=iniciar_servidor, daemon=True).start()
    if esperar_servidor():
        webview.create_window(
            "Hospital System",
            "http://127.0.0.1:8000",
            width=1200,
            height=800
        )
        webview.start()
    else:
        log("No se pudo conectar. Cerrando.")