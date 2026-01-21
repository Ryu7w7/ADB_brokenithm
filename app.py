from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import locale
import threading
from tkinter.scrolledtext import ScrolledText
import sys

NO_WINDOW = subprocess.CREATE_NO_WINDOW

def resource_path(relative):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADB_DIR = resource_path("adb")
ADB_EXE = os.path.join(ADB_DIR, "adb.exe")
SERVER_DIR = resource_path("server")
ICON_PATH = resource_path("icon.ico")

brokenithm_process = None

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
        "detect_device": "Detectar dispositivo (USB)",
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
        "instruction": "USB: 127.0.0.1:52468 TCP | LAN: 192.168.X.X:52468 TCP",
        "about": "Acerca de",
        "created_by": "RyuVer. v0.4"
    },
    "en": {
        "title": "ADB_Brokenithm",
        "detect_device": "Detect Device (USB)",
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
        "instruction": "USB: 127.0.0.1:52468 | LAN: 192.168.X.X:52468",
        "about": "About",
        "created_by": "RyuVer. v0.4"
    }
}

def t(key):
    return texts[current_language][key]

dot_count = 0

def update_status(msg, color="#cccccc"):
    status_var.set(msg)
    status_label.config(fg=color)

def adb_exists():
    return os.path.exists(ADB_EXE)

def detect_device():
    global dot_count
    if not adb_exists():
        update_status("adb.exe not found", "#ff5555")
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
            update_status(t("device_detected"), "#55ff99")
            root.after(1000, redirect_ports)
        else:
            dot_count = (dot_count + 1) % 4
            update_status(t("no_device") + "." * dot_count)
            root.after(1000, detect_device)
    except Exception as e:
        update_status(f"{t('error')} {e}", "#ff5555")

def redirect_ports():
    try:
        result = subprocess.run(
            [ADB_EXE, "reverse", "tcp:52468", "tcp:52468"],
            cwd=ADB_DIR,
            capture_output=True,
            text=True,
            creationflags=NO_WINDOW
        )
        if result.returncode == 0:
            update_status(t("redirect_complete"), "#55ff99")
        else:
            update_status(f"{t('redirect_error')} {result.stderr}", "#ff5555")
    except Exception as e:
        update_status(f"{t('redirect_error')} {e}", "#ff5555")

def write_log(text):
    log_box.configure(state="normal")
    low = text.lower()
    if "error" in low:
        tag = "error"
    elif "warn" in low:
        tag = "warn"
    elif "connect" in low or "listen" in low:
        tag = "ok"
    else:
        tag = "normal"
    log_box.insert("end", text, tag)
    log_box.see("end")
    log_box.configure(state="disabled")

def read_server_output(proc):
    for line in proc.stdout:
        root.after(0, write_log, line)

def start_server():
    global brokenithm_process
    exe = os.path.join(SERVER_DIR, "brokenithm_server.exe")
    if not os.path.exists(exe):
        update_status(t("server_not_found"), "#ff5555")
        return
    if brokenithm_process and brokenithm_process.poll() is None:
        update_status("Server already running.", "#ffaa00")
        return
    brokenithm_process = subprocess.Popen(
        [exe, "-T"],
        cwd=SERVER_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    threading.Thread(target=read_server_output, args=(brokenithm_process,), daemon=True).start()
    update_status(t("server_started"), "#55ff99")

def exit_app():
    global brokenithm_process
    if messagebox.askyesno(t("title"), t("exit_confirm")):
        try:
            if brokenithm_process and brokenithm_process.poll() is None:
                brokenithm_process.kill()
        except Exception:
            pass
        root.destroy()

def show_about():
    messagebox.showinfo(t("about"), t("created_by"))

root = tk.Tk()
root.title(f"{t('title')} - {t('created_by')}")
root.geometry("420x560")
root.resizable(False, False)
root.configure(bg="#1b1b1b")

try:
    root.iconbitmap(ICON_PATH)
except Exception as e:
    print(f"Error cargando icono: {e}")

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
style.configure("TLabel", background="#1b1b1b", foreground="#dddddd")

header = tk.Label(root, text="ADB_BROKENITHM", font=("Segoe UI", 15, "bold"),
                  bg="#1b1b1b", fg="#55ffd5")
header.pack(pady=10)

btn_frame = tk.Frame(root, bg="#1b1b1b")
btn_frame.pack(pady=6)
ttk.Button(btn_frame, text=t("detect_device"), width=32, command=detect_device).pack(pady=4)
ttk.Button(btn_frame, text=t("start_server"), width=32, command=start_server).pack(pady=4)
ttk.Button(btn_frame, text=t("exit"), width=32, command=exit_app).pack(pady=4)

status_var = tk.StringVar(value=t("status_waiting") + "...")
status_label = tk.Label(root, textvariable=status_var, bg="#1b1b1b",
                        fg="#cccccc", font=("Segoe UI", 9))
status_label.pack(pady=6)

tk.Label(root, text=t("instruction"), wraplength=390,
         bg="#1b1b1b", fg="#888888", font=("Segoe UI", 9)).pack(pady=4)

log_frame = tk.Frame(root, bg="#1b1b1b")
log_frame.pack(fill="both", expand=True, padx=10, pady=8)
log_box = ScrolledText(log_frame, height=10, state="disabled",
                       font=("Consolas", 10),
                       background="#111111", foreground="#dddddd",
                       insertbackground="white")
log_box.pack(fill="both", expand=True)
log_box.tag_config("error", foreground="#ff5555")
log_box.tag_config("warn", foreground="#ffaa00")
log_box.tag_config("ok", foreground="#55ff99")
log_box.tag_config("normal", foreground="#dddddd")

footer = tk.Label(root, text="ADB_Brokenithm by Ryu7w7",
                  bg="#111111", fg="#666666", font=("Segoe UI", 8))
footer.pack(fill="x", side="bottom")

root.protocol("WM_DELETE_WINDOW", exit_app)
root.mainloop()
