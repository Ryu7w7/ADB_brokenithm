import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

# Directorios donde se encuentran adb.exe y brokenithm_server.exe
adb_directory = os.path.join(os.path.dirname(__file__), 'adb')
server_directory = os.path.join(os.path.dirname(__file__), 'server')

# Variables globales para los textos en diferentes idiomas
texts = {
    "es": {
        "title": "Administrador ADB brokenithm",
        "detect_device": "Detectar dispositivo",
        "start_server": "Iniciar Brokenithm Server",
        "exit": "Salir",
        "status_waiting": "Esperando a que se conecte un dispositivo",
        "device_detected": "Dispositivo detectado. Ejecutando redireccionamiento...",
        "no_device": "Ningún dispositivo detectado. Intentando de nuevo",
        "redirect_complete": "Redirección completada. Ya puede iniciar el servidor.",
        "redirect_error": "Error al redirigir puertos:",
        "start_server_error": "Error al iniciar el servidor:",
        "server_not_found": "Error: brokenithm_server.exe no encontrado.",
        "server_started": "Servidor Brokenithm iniciado en una nueva consola.",
        "exit_confirm": "¿Estás seguro de que quieres salir?",
        "error": "Error al ejecutar adb:",
        "instruction": "* Para conectarse al servidor brokenithm utiliza la siguiente dirección: 127.0.0.1:8081 *"
    },
    "en": {
        "title": "ADB Manager brokenithm",
        "detect_device": "Detect Device",
        "start_server": "Start Brokenithm Server",
        "exit": "Exit",
        "status_waiting": "Waiting for a device to connect",
        "device_detected": "Device detected. Redirecting ports...",
        "no_device": "No device detected. Trying again",
        "redirect_complete": "Redirect complete. You can now start the server.",
        "redirect_error": "Error redirecting ports:",
        "start_server_error": "Error starting server:",
        "server_not_found": "Error: brokenithm_server.exe not found.",
        "server_started": "Brokenithm server started in a new console.",
        "exit_confirm": "Are you sure you want to exit?",
        "error": "Error running adb:",
        "instruction": "* To connect to the Brokenithm server, use the following address: 127.0.0.1:8081 *"
    }
}

# Variable para el idioma actual
current_language = "es"

def set_language(language):
    global current_language
    current_language = language
    root.title(texts[language]["title"])
    button.config(text=texts[language]["detect_device"])
    server_button.config(text=texts[language]["start_server"])
    exit_button.config(text=texts[language]["exit"])
    status_label.config(text=texts[language]["status_waiting"] + '...')
    instruction_label.config(text=texts[language]["instruction"])

def detect_device():
    """Detect devices using adb."""
    try:
        if not os.path.exists(adb_directory):
            raise FileNotFoundError(f"El directorio {adb_directory} no existe.")
        os.chdir(adb_directory)
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        devices = [line for line in result.stdout.splitlines() if '\tdevice' in line]

        if devices:
            update_status(texts[current_language]["device_detected"], "green")
            root.after(1000, redirect_ports)
        else:
            animate_dots()
    except Exception as e:
        update_status(f"{texts[current_language]['error']} {e}", "red")

def redirect_ports():
    """Redirect ports using adb."""
    try:
        result = subprocess.run(['adb', 'reverse', 'tcp:8081', 'tcp:8080'], capture_output=True, text=True)
        if result.returncode == 0:
            update_status(texts[current_language]["redirect_complete"], "green")
        else:
            update_status(f"{texts[current_language]['redirect_error']} {result.stderr}", "red")
    except Exception as e:
        update_status(f"{texts[current_language]['redirect_error']} {e}", "red")

def start_server():
    """Start the Brokenithm server in a new console window."""
    try:
        if not os.path.exists(server_directory):
            raise FileNotFoundError(f"El directorio {server_directory} no existe.")
        original_directory = os.getcwd()  # Guardar el directorio actual
        os.chdir(server_directory)
        if os.path.exists('brokenithm_server.exe'):
            subprocess.Popen(
                ['brokenithm_server.exe', '-T', '-p', '8080'],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            update_status(texts[current_language]["server_started"], "green")
        else:
            update_status(texts[current_language]["server_not_found"], "red")
        os.chdir(original_directory)  # Volver al directorio original
    except Exception as e:
        update_status(f"{texts[current_language]['start_server_error']} {e}", "red")

def update_status(message, color):
    """Update the status label."""
    status_label.config(text=message, fg=color)

def exit_application():
    """Close the application."""
    if messagebox.askokcancel(texts[current_language]["exit"], texts[current_language]["exit_confirm"]):
        root.destroy()

def animate_dots(count=0):
    """Animate the 'Trying again...' message with moving dots."""
    dots = '.' * (count % 4)
    message = f"{texts[current_language]['no_device']}{dots}"
    status_label.config(text=message, fg="red")
    if count < 9:  # 9 iteraciones para un total de 4.5 segundos (9 * 500ms)
        root.after(500, lambda: animate_dots(count + 1))
    else:
        detect_device()

# Crear la ventana principal
root = tk.Tk()

# Configurar el icono de la ventana
try:
    if hasattr(sys, '_MEIPASS'):
        icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
    else:
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
    root.iconbitmap(icon_path)
except tk.TclError:
    print("No se encontró el icono, continuando sin él.")

root.title(texts[current_language]["title"])
root.geometry("600x300")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Crear el marco principal
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(expand=True, fill="both", padx=20, pady=10)

# Crear los botones para cambiar el idioma
lang_frame = tk.Frame(frame, bg="#f0f0f0")
lang_frame.pack(pady=5)

btn_es = tk.Button(lang_frame, text="Español", command=lambda: set_language("es"), font=("Arial", 10), bg="#808080", fg="white")
btn_es.pack(side="left", padx=5)

btn_en = tk.Button(lang_frame, text="English", command=lambda: set_language("en"), font=("Arial", 10), bg="#808080", fg="white")
btn_en.pack(side="left", padx=5)

# Crear el botón para detectar dispositivos
button = tk.Button(frame, text=texts[current_language]["detect_device"], command=detect_device, font=("Arial", 12), bg="#4CAF50", fg="white")
button.pack(pady=5)

# Crear el botón para iniciar el servidor
server_button = tk.Button(frame, text=texts[current_language]["start_server"], command=start_server, font=("Arial", 12), bg="#2196F3", fg="white")
server_button.pack(pady=5)

# Crear la etiqueta para mostrar el estado
status_label = tk.Label(frame, text=texts[current_language]["status_waiting"] + '...', font=("Arial", 10), bg="#f0f0f0", fg="blue")
status_label.pack(pady=10)

# Crear la etiqueta para mostrar las instrucciones
instruction_label = tk.Label(frame, text=texts[current_language]["instruction"], font=("Arial", 10), bg="#f0f0f0", fg="black")
instruction_label.pack(pady=10)

# Crear el botón para salir de la aplicación
exit_button = tk.Button(frame, text=texts[current_language]["exit"], command=exit_application, font=("Arial", 12), bg="#f44336", fg="white")
exit_button.pack(pady=10)

# Añadir etiqueta en la esquina inferior izquierda
creator_label = tk.Label(root, text="Creado por Ryu7w7", font=("Arial", 8), bg="#f0f0f0", fg="black")
creator_label.place(relx=0.01, rely=0.95, anchor='sw')

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
