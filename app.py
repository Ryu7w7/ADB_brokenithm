from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import locale

NO_WINDOW = subprocess.CREATE_NO_WINDOW
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADB_DIR = os.path.join(BASE_DIR, "adb")
ADB_EXE = os.path.join(ADB_DIR, "adb.exe")
SERVER_DIR = os.path.join(BASE_DIR, "server")
ICON_PATH = os.path.join(BASE_DIR, "icon.ico")
BG_IMAGE_PATH = os.path.join(BASE_DIR, "bg.png")

def detect_system_language():
    try:
        lang = locale.getdefaultlocale()[0]
        if lang and lang.lower().startswith("es"):
            return "es"
        return "en"
    except Exception:
        return "en"

current_language = detect_system_language()

texts = {
    "es": {
        "title": "ADB_Brokenithm",
        "detect_device": "Detectar dispositivo",
        "start_server": "Iniciar Brokenithm Server",
        "exit": "Salir",
        "status_waiting": "Esperando dispositivo",
        "device_detected": "Dispositivo detectado. Redirigiendo puertos...",
        "no_device": "Ningún dispositivo detectado",
        "redirect_complete": "Redirección completada. Ya puede iniciar el servidor.",
        "redirect_error": "Error al redirigir puertos:",
        "start_server_error": "Error al iniciar el servidor:",
        "server_not_found": "brokenithm_server.exe no encontrado.",
        "server_started": "Servidor Brokenithm iniciado.",
        "exit_confirm": "¿Estás seguro de que quieres salir?",
        "error": "Error ejecutando adb:",
        "instruction": "* Conecta con 127.0.0.1:8081 usando TCP *",
        "about": "Acerca de",
        "created_by": "Ver. v0.3"
    },
    "en": {
        "title": "ADB_Brokenithm",
        "detect_device": "Detect Device",
        "start_server": "Start Brokenithm Server",
        "exit": "Exit",
        "status_waiting": "Waiting for device",
        "device_detected": "Device detected. Redirecting ports...",
        "no_device": "No device detected",
        "redirect_complete": "Redirect complete. You can start the server.",
        "redirect_error": "Port redirect error:",
        "start_server_error": "Server start error:",
        "server_not_found": "brokenithm_server.exe not found.",
        "server_started": "Brokenithm server started.",
        "exit_confirm": "Are you sure you want to exit?",
        "error": "ADB execution error:",
        "instruction": "* Connect with 127.0.0.1:8081 using TCP *",
        "about": "About",
        "created_by": "Ver. v0.3"
    }
}

def t(key):
    return texts[current_language][key]

dot_count = 0

def update_status(msg, color="black"):
    status_var.set(msg)
    status_label.config(fg=color)

def adb_exists():
    return os.path.exists(ADB_EXE)

def detect_device():
    global dot_count

    if not adb_exists():
        update_status("adb.exe not found", "red")
        return

    try:
        result = subprocess.run(
            [ADB_EXE, "devices"],
            cwd=ADB_DIR,
            capture_output=True,
            text=True,
            creationflags=NO_WINDOW
        )

        devices = [l for l in result.stdout.splitlines() if "\tdevice" in l]

        if devices:
            update_status(t("device_detected"), "green")
            root.after(1000, redirect_ports)
        else:
            dot_count = (dot_count + 1) % 4
            update_status(t("no_device") + "." * dot_count)
            root.after(1000, detect_device)

    except Exception as e:
        update_status(f"{t('error')} {e}", "red")

def redirect_ports():
    try:
        result = subprocess.run(
            [ADB_EXE, "reverse", "tcp:8081", "tcp:8080"],
            cwd=ADB_DIR,
            capture_output=True,
            text=True,
            creationflags=NO_WINDOW
        )

        if result.returncode == 0:
            update_status(t("redirect_complete"), "green")
        else:
            update_status(f"{t('redirect_error')} {result.stderr}", "red")

    except Exception as e:
        update_status(f"{t('redirect_error')} {e}", "red")

def start_server():
    try:
        exe = os.path.join(SERVER_DIR, "brokenithm_server.exe")

        if not os.path.exists(exe):
            update_status(t("server_not_found"), "red")
            return

        subprocess.Popen(
            [exe, "-T", "-p", "8080"],
            cwd=SERVER_DIR,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        update_status(t("server_started"), "green")

    except Exception as e:
        update_status(f"{t('start_server_error')} {e}", "red")

def exit_app():
    if messagebox.askyesno(t("title"), t("exit_confirm")):
        root.destroy()

def show_about():
    messagebox.showinfo(t("about"), t("created_by"))

root = tk.Tk()
root.title(f"{t('title')} - {t('created_by')}")
root.geometry("400x400")
root.resizable(False, False)
ICON_PATH = os.path.join(BASE_DIR, "icon.png")

try:
    icon_img = tk.PhotoImage(file=ICON_PATH)
    root.iconphoto(True, icon_img)
except Exception:
    pass

bg_image = Image.open(BG_IMAGE_PATH)
bg_image = bg_image.resize((400, 400))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_photo

status_var = tk.StringVar(value=t("status_waiting") + "...")

ttk.Button(root, text=t("detect_device"), command=detect_device).pack(pady=10)
ttk.Button(root, text=t("start_server"), command=start_server).pack(pady=10)
ttk.Button(root, text=t("exit"), command=exit_app).pack(pady=10)

status_label = tk.Label(root, textvariable=status_var)
status_label.pack(pady=10)

tk.Label(root, text=t("instruction"), wraplength=380).pack(pady=10)

menu = tk.Menu(root)
root.config(menu=menu)
about_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label=t("about"), menu=about_menu)
about_menu.add_command(label=t("about"), command=show_about)

root.protocol("WM_DELETE_WINDOW", exit_app)
root.mainloop()
