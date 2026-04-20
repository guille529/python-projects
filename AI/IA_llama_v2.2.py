import tkinter as tk
from tkinter import scrolledtext
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import ollama
import threading
import subprocess
import os
import re
import queue
import json
import webbrowser
import tempfile 

# --- CONFIGURACIÓN DE RUTAS Y MODELOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VOICE_MODEL = os.path.join(BASE_DIR, "es_ES-sharvard-medium.onnx")
VOSK_MODEL_PATH = os.path.join(BASE_DIR, "vosk-model-es-0.42") 
MODEL_NAME = 'llama3'
SAMPLE_RATE = 16000 

# --- VARIABLES DE CONTROL GLOBAL ---
chat_history = []
audio_queue = queue.Queue()
esta_hablando = False
detener_audio = False
ejecutando = True # Bandera para detener los hilos limpiamente

# --- INICIALIZACIÓN DE VOSK ---
if not os.path.exists(VOSK_MODEL_PATH):
    print(f"ERROR: No se encuentra el modelo en: {VOSK_MODEL_PATH}")
    exit(1)

vosk_model = Model(VOSK_MODEL_PATH)
keywords = '["steam", "discord", "firefox", "nobara", "llama", "terminal", "abrir", "cerrar", "[unk]"]'
rec = KaldiRecognizer(vosk_model, SAMPLE_RATE, keywords)

# --- MOTOR DE SALIDA DE AUDIO ---
def audio_worker():
    global esta_hablando, detener_audio
    while ejecutando:
        try:
            text = audio_queue.get(timeout=1) # Timeout para que el hilo pueda morir
        except queue.Empty:
            continue

        if text is None: break

        if os.path.exists(VOICE_MODEL) and not detener_audio:
            esta_hablando = True
            try:
                text_clean = text.replace("*", "").replace("\n", " ").replace("_", " ").strip()
                if text_clean:
                    with tempfile.NamedTemporaryFile(suffix=".raw", delete=True) as temp_audio:
                        comando_piper = f'echo "{text_clean}" | piper --model "{VOICE_MODEL}" --output_raw > {temp_audio.name}'
                        subprocess.run(comando_piper, shell=True, stderr=subprocess.DEVNULL)
                        if not detener_audio and ejecutando:
                            subprocess.run(['aplay', '-r', '22050', '-f', 'S16_LE', '-t', 'raw', temp_audio.name], stderr=subprocess.DEVNULL)
            except Exception as e:
                update_interface(f"Error Audio: {e}", "sys")
            finally:
                esta_hablando = False
                if ejecutando:
                    root.after(300, lambda: set_status("ESCUCHANDO...", "#2ecc71"))
        audio_queue.task_done()

threading.Thread(target=audio_worker, daemon=True).start()

# --- LÓGICA DE SISTEMA Y LLAMA ---
def ejecutar_acciones(texto_ia):
    if "BUSCAR:" in texto_ia:
        query = re.search(r'BUSCAR:\s*(.*)', texto_ia)
        if query: webbrowser.open(f"https://www.google.com/search?q={query.group(1).strip()}")

    if "EJECUTAR:" in texto_ia:
        prog = re.search(r'EJECUTAR:\s*([a-zA-Z0-9_-]+)', texto_ia)
        if prog: subprocess.Popen([prog.group(1)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if "CERRAR:" in texto_ia:
        prog = re.search(r'CERRAR:\s*([a-zA-Z0-9_-]+)', texto_ia)
        if prog: subprocess.run(["pkill", "-f", prog.group(1)])

def procesar_comando(texto_usuario):
    global chat_history, detener_audio
    detener_audio = False
    update_interface(f"Tú: {texto_usuario}", "user")
    set_status("LLAMA PENSANDO...", "#9b59b6")

    try:
        system_prompt = ("""Eres un asistente virtual inteligente, amigable y eficiente para Guillermo.
Tu objetivo es ayudar con sus programas, resolver dudas y mantener una conversación natural y agradable.

COMPORTAMIENTO GENERAL
Responde de forma clara, útil y directa.
Mantén un tono cercano, natural y ligeramente informal.
Sé conciso, pero sin sonar seco o robótico.
Si el usuario solo quiere charlar, responde de forma conversacional.

REGLAS IMPORTANTES DE COMANDOS
Incluye el comando en una línea separada.
Acompaña SIEMPRE el comando con una frase natural antes o después.
No uses comandos si el usuario no lo pide claramente.
Si no estás seguro del programa, pide aclaración en lugar de adivinar.

ESTILO DE RESPUESTA
Evita respuestas muy cortas o frías.
No uses lenguaje demasiado formal.
Puedes hacer pequeñas preguntas para continuar la conversación si tiene sentido.                        
                         
COMANDOS DEL SISTEMA

Usa comandos SOLO cuando el usuario lo pida de forma clara.

Ejecutar programas
Para abrir un programa:
EJECUTAR: nombre_del_binario
Cerrar programas
Para cerrar un programa:
CERRAR: nombre_del_binario
Gestión de archivos
Para leer un archivo:
LEER: ruta_del_archivo
Para crear un archivo:
CREAR: ruta_del_archivo
Para eliminar un archivo:
BORRAR: ruta_del_archivo
REGLAS IMPORTANTES DE SEGURIDAD
Usa comandos SOLO si el usuario lo pide explícitamente.
Para acciones sensibles (como BORRAR), pide confirmación antes de ejecutar.
Si la ruta o el archivo no está claro, pide más información.
Nunca asumas rutas o nombres de archivos.
Acompaña SIEMPRE el comando con una frase natural.
                         
TAREAS GRANDES O COMPLEJAS
Cuando el usuario pida algo grande, complejo o detallado, no te limites: ofrece una respuesta completa y útil.
Divide la respuesta en pasos claros o secciones si es necesario.
Prioriza la claridad sobre la longitud innecesaria.
Si la tarea es muy extensa, puedes:
Dar una solución completa y sugerir continuar en más pasos.
O preguntar si el usuario quiere que profundices en alguna parte.
BALANCE DE RESPUESTA
Para tareas simples → respuestas cortas y directas.
Para tareas complejas → respuestas más desarrolladas y bien organizadas.
Evita respuestas excesivamente largas sin estructura.        """)

        messages = [{'role': 'system', 'content': system_prompt}] + chat_history[-6:] + [{'role': 'user', 'content': texto_usuario}]
        response = ollama.chat(model=MODEL_NAME, messages=messages)
        ai_res = response['message']['content']

        ejecutar_acciones(ai_res)
        update_interface(f"Llama: {ai_res}", "ai")
        
        chat_history.append({'role': 'user', 'content': texto_usuario})
        chat_history.append({'role': 'assistant', 'content': ai_res})

        voice_text = re.sub(r'[A-Z_]{5,}:.*', '', ai_res, flags=re.DOTALL).strip()
        if voice_text and not detener_audio and ejecutando:
            audio_queue.put(voice_text)

    except Exception as e:
        if ejecutando: update_interface(f"ERROR: {str(e)}", "sys")

# --- INTERFAZ GRÁFICA ---
root = tk.Tk()
root.title("Llama OS - Terminal v2.6")
root.geometry("600x750")
root.configure(bg="#1a1a2e")

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#16213e", fg="#ffffff", font=("Arial", 11), state=tk.DISABLED)
chat_display.tag_config("user_text", foreground="#00d2ff", font=("Arial", 11, "bold"))
chat_display.tag_config("ai_text", foreground="#ffffff")
chat_display.tag_config("sys_text", foreground="#95a5a6", font=("Arial", 9, "italic"))
chat_display.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

status_label = tk.Label(root, text="INICIANDO...", bg="#1a1a2e", fg="white", font=("Arial", 10, "bold"))
status_label.pack()

user_entry = tk.Entry(root, bg="#16213e", fg="white", font=("Arial", 11), insertbackground="white")
user_entry.pack(fill=tk.X, padx=20, pady=5, ipady=8)

def enviar_manual(event=None):
    texto = user_entry.get().strip()
    if texto:
        user_entry.delete(0, tk.END)
        threading.Thread(target=procesar_comando, args=(texto,), daemon=True).start()

user_entry.bind("<Return>", enviar_manual)

def silenciar():
    global detener_audio
    detener_audio = True
    subprocess.run(["pkill", "-f", "aplay"])

tk.Button(root, text="SILENCIAR / SALTAR", command=silenciar, bg="#e74c3c", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

def update_interface(msg, sender):
    if ejecutando: root.after(0, lambda: _update(msg, sender))

def _update(msg, sender):
    chat_display.config(state=tk.NORMAL)
    tag = "user_text" if sender == "user" else "ai_text" if sender == "ai" else "sys_text"
    chat_display.insert(tk.END, msg + "\n\n", tag)
    chat_display.see(tk.END)
    chat_display.config(state=tk.DISABLED)

def set_status(t, c):
    if ejecutando: root.after(0, lambda: status_label.config(text=t, fg=c))

# --- BUCLE DE ESCUCHA (CORREGIDO) ---
def listen_loop():
    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1) as stream:
            while ejecutando:
                data, _ = stream.read(4000)
                if not esta_hablando and ejecutando:
                    if rec.AcceptWaveform(bytes(data)):
                        res = json.loads(rec.Result())
                        text = res.get("text", "").strip()
                        if text and ejecutando:
                            threading.Thread(target=procesar_comando, args=(text,), daemon=True).start()
                    else:
                        partial_res = json.loads(rec.PartialResult())
                        partial_text = partial_res.get("partial", "")
                        if partial_text and ejecutando:
                            set_status(f"Escuchando: {partial_text}...", "#3498db")
                else:
                    if ejecutando: stream.read(4000)
    except Exception:
        pass

# --- CIERRE LIMPIO ---
def on_closing():
    global ejecutando
    ejecutando = False # Detiene todos los bucles
    root.destroy()
    os._exit(0) # Fuerza la salida de todos los hilos secundarios inmediatamente

root.protocol("WM_DELETE_WINDOW", on_closing)
threading.Thread(target=listen_loop, daemon=True).start()
root.mainloop()