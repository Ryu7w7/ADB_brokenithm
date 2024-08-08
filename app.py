import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys

adb_directory = os.path.join(os.path.dirname(__file__), 'adb')
server_directory = os.path.join(os.path.dirname(__file__), 'server')
icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')

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
        "instruction": "* Para conectarse al servidor brokenithm utiliza la siguiente dirección: 127.0.0.1:8081 con protocolo TCP *",
        "about": "Acerca de",
        "created_by": "Creado por Ryu7w7 v0.2"
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
        "instruction": "* To connect to the Brokenithm server, use the following address: 127.0.0.1:8081 with TCP protocol *",
        "about": "About",
        "created_by": "Created by Ryu7w7 v0.2"
    },
    "ja": {
        "title": "ADBマネージャーbrokenithm",
        "detect_device": "デバイスを検出",
        "start_server": "Brokenithmサーバーを起動",
        "exit": "終了",
        "status_waiting": "デバイスの接続を待っています",
        "device_detected": "デバイスが検出されました。ポートをリダイレクトしています...",
        "no_device": "デバイスが検出されません。再試行します",
        "redirect_complete": "リダイレクト完了。サーバーを起動できます。",
        "redirect_error": "ポートのリダイレクトエラー:",
        "start_server_error": "サーバーの起動エラー:",
        "server_not_found": "エラー: brokenithm_server.exeが見つかりません。",
        "server_started": "Brokenithmサーバーが新しいコンソールで起動しました。",
        "exit_confirm": "本当に終了しますか？",
        "error": "adbの実行エラー:",
        "instruction": "* Brokenithmサーバーに接続するには、TCPプロトコルで次のアドレスを使用してください：127.0.0.1:8081 *",
        "about": "約",
        "created_by": "Ryu7w7によって作成されました v0.2"
    },
    "zh": {
        "title": "ADB管理器brokenithm",
        "detect_device": "检测设备",
        "start_server": "启动Brokenithm服务器",
        "exit": "退出",
        "status_waiting": "等待设备连接",
        "device_detected": "设备已检测到。正在重定向端口...",
        "no_device": "未检测到设备。重试中",
        "redirect_complete": "重定向完成。现在可以启动服务器。",
        "redirect_error": "端口重定向错误：",
        "start_server_error": "启动服务器错误：",
        "server_not_found": "错误：未找到brokenithm_server.exe。",
        "server_started": "Brokenithm服务器已在新控制台中启动。",
        "exit_confirm": "您确定要退出吗？",
        "error": "执行adb时出错：",
        "instruction": "* 要连接到Brokenithm服务器，请使用以下地址：127.0.0.1:8081，使用TCP协议 *",
        "about": "关于",
        "created_by": "由Ryu7w7创建 v0.2"
    },
    "ko": {
        "title": "ADB 관리자 brokenithm",
        "detect_device": "장치 감지",
        "start_server": "Brokenithm 서버 시작",
        "exit": "종료",
        "status_waiting": "장치 연결 대기 중",
        "device_detected": "장치가 감지되었습니다. 포트를 리디렉션하는 중...",
        "no_device": "장치가 감지되지 않았습니다. 다시 시도 중",
        "redirect_complete": "리디렉션 완료. 이제 서버를 시작할 수 있습니다.",
        "redirect_error": "포트 리디렉션 오류:",
        "start_server_error": "서버 시작 오류:",
        "server_not_found": "오류: brokenithm_server.exe를 찾을 수 없습니다.",
        "server_started": "Brokenithm 서버가 새 콘솔에서 시작되었습니다.",
        "exit_confirm": "정말로 종료하시겠습니까?",
        "error": "adb 실행 오류:",
        "instruction": "* Brokenithm 서버에 연결하려면 다음 주소를 사용하십시오: 127.0.0.1:8081, TCP 프로토콜 사용 *",
        "about": "정보",
        "created_by": "Ryu7w7에 의해 생성됨 v0.2"
    }
}

current_language = "es"

def set_language(language):
    global current_language
    current_language = language
    root.title(f"{texts[language]['title']} - {texts[language]['created_by']}")
    button.config(text=texts[language]["detect_device"])
    server_button.config(text=texts[language]["start_server"])
    exit_button.config(text=texts[language]["exit"])
    status_label.config(text=texts[language]["status_waiting"] + '...')
    instruction_label.config(text=texts[language]["instruction"])
    about_menu.entryconfig(0, label=texts[language]["about"])
    update_language_buttons()
    lang_tabs.tab(0, text=texts[language]["title"])
    lang_tabs.tab(1, text="Language" if language == "en" else "Idioma")

def update_language_buttons():
    lang_texts = {
        "es": "Español",
        "en": "English",
        "ja": "日本語",
        "zh": "中文",
        "ko": "한국어"
    }
    for idx, (btn, lang) in enumerate(lang_buttons):
        btn.config(text=lang_texts[lang])

def detect_device():
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
    try:
        result = subprocess.run(['adb', 'reverse', 'tcp:8081', 'tcp:8080'], capture_output=True, text=True)
        if result.returncode == 0:
            update_status(texts[current_language]["redirect_complete"], "green")
        else:
            update_status(f"{texts[current_language]['redirect_error']} {result.stderr}", "red")
    except Exception as e:
        update_status(f"{texts[current_language]['redirect_error']} {e}", "red")

def start_server():
    try:
        if not os.path.exists(server_directory):
            raise FileNotFoundError(f"El directorio {server_directory} no existe.")
        original_directory = os.getcwd()
        os.chdir(server_directory)
        if os.path.exists('brokenithm_server.exe'):
            subprocess.Popen(['brokenithm_server.exe', '-T', '-p', '8080'], creationflags=subprocess.CREATE_NEW_CONSOLE)
            update_status(texts[current_language]["server_started"], "green")
        else:
            update_status(texts[current_language]["server_not_found"], "red")
        os.chdir(original_directory)
    except Exception as e:
        update_status(f"{texts[current_language]['start_server_error']} {e}", "red")

def update_status(message, color):
    status_label.config(text=message, fg=color)

def exit_app():
    if messagebox.askyesno(texts[current_language]["title"], texts[current_language]["exit_confirm"]):
        root.destroy()

def show_about():
    messagebox.showinfo(texts[current_language]["about"], texts[current_language]["created_by"])

root = tk.Tk()
root.title(f"{texts[current_language]['title']} - {texts[current_language]['created_by']}")
root.geometry("400x400")
root.resizable(False, False)
root.iconbitmap(icon_path)

style = ttk.Style()
style.configure('TButton', padding=6, relief="flat", background="#ccc")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

about_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label=texts[current_language]["about"], menu=about_menu)
about_menu.add_command(label=texts[current_language]["about"], command=show_about)

lang_tabs = ttk.Notebook(root)
main_tab = ttk.Frame(lang_tabs)
lang_tab = ttk.Frame(lang_tabs)
lang_tabs.add(main_tab, text=texts[current_language]["title"])
lang_tabs.add(lang_tab, text="Idioma" if current_language == "es" else "Language")
lang_tabs.pack(expand=1, fill="both")

lang_buttons = []

lang_frame = tk.Frame(lang_tab)
lang_frame.pack(expand=1)

for idx, (lang, text) in enumerate([("es", "Español"), ("en", "English"), ("ja", "日本語"), ("zh", "中文"), ("ko", "한국어")]):
    btn = ttk.Button(lang_frame, text=text, command=lambda l=lang: set_language(l), style='TButton')
    btn.grid(row=idx, column=0, padx=5, pady=5, sticky="ew")
    lang_buttons.append((btn, lang))

button = ttk.Button(main_tab, text=texts[current_language]["detect_device"], command=detect_device, style='TButton')
button.pack(pady=10)

server_button = ttk.Button(main_tab, text=texts[current_language]["start_server"], command=start_server, style='TButton')
server_button.pack(pady=10)

exit_button = ttk.Button(main_tab, text=texts[current_language]["exit"], command=exit_app, style='TButton')
exit_button.pack(pady=10)

status_label = tk.Label(main_tab, text=texts[current_language]["status_waiting"] + '...')
status_label.pack(pady=10)

instruction_label = tk.Label(main_tab, text=texts[current_language]["instruction"], wraplength=380)
instruction_label.pack(pady=10)

def animate_dots():
    if '...' not in status_label.cget("text"):
        status_label.config(text=status_label.cget("text") + '.')
    else:
        status_label.config(text=texts[current_language]["no_device"])
    root.after(1000, detect_device)

set_language(current_language)

root.protocol("WM_DELETE_WINDOW", exit_app)
root.mainloop()
