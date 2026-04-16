import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import ollama
import threading
import subprocess
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VOICE_MODEL = os.path.join(BASE_DIR, "es_ES-sharvard-medium.onnx")
MODEL_NAME = 'llama3'

SYSTEM_PROMPT = """Eres un asistente virtual inteligente y amable para Nobara Linux. 
Tu objetivo es ayudar al usuario con sus programas y charlar de forma natural.

REGLAS DE COMANDOS:
- Si el usuario quiere abrir algo: incluye 'EJECUTAR: nombre_del_binario'.
- Si quiere cerrar algo: incluye 'CERRAR: nombre_del_binario'.
- SIEMPRE acompaña el comando con una frase amable y natural.

REGLAS DE CHARLA:
- Responde con calidez y personalidad. No seas cortante.
- Mantén las respuestas fluidas."""

chat_history = []

def speak(text):
    if text:
        update_interface(f"Llama: {text}\n", "ai")
        clean_voice_text = re.sub(r'(EJECUTAR:|CERRAR:)\s*\S+', '', text).strip()
        
        if os.path.exists(VOICE_MODEL) and clean_voice_text:
            frases = re.split(r'[.!?¡¿,]+', clean_voice_text)
            for frase in frases:
                frase = frase.strip()
                if len(frase) > 1:
                    command = f"echo '{frase}' | piper --model '{VOICE_MODEL}' --output_raw | aplay -r 22050 -f S16_LE -t raw 2>/dev/null"
                    subprocess.run(command, shell=True)

def listen_and_process():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False 
    recognizer.energy_threshold = 350 
    recognizer.pause_threshold = 1.2

    with sr.Microphone() as source:
        set_status("CALIBRANDO...", "#3498db")
        recognizer.adjust_for_ambient_noise(source, duration=1.0) 
        set_status("TE ESCUCHO...", "#e74c3c")
        
        try:
            audio_data = recognizer.listen(source, timeout=None, phrase_time_limit=10)
            set_status("ENTENDIENDO...", "#f1c40f")
            
            user_text = recognizer.recognize_google(audio_data, language='es-MX').lower()
            update_interface(f"Usuario: {user_text}\n", "user")
            
            if any(word in user_text for word in ["apágate", "salir", "adiós"]):
                speak("¡Entendido! Me apago ahora. ¡Ten un gran día!")
                main_window.after(1500, main_window.quit)
                return

            messages = [{'role': 'system', 'content': SYSTEM_PROMPT}] + chat_history[-6:]
            response = ollama.chat(
                model=MODEL_NAME, 
                messages=messages + [{'role': 'user', 'content': user_text}],
                options={'temperature': 0.7}
            )
            ai_response = response['message']['content'].strip()

            lines = ai_response.split('\n')
            found_action = False
            for line in lines:
                if "EJECUTAR:" in line:
                    match = re.search(r'EJECUTAR:\s*(\S+)', line)
                    if match:
                        prog = match.group(1).replace('.', '')
                        subprocess.Popen([prog], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        found_action = True
                elif "CERRAR:" in line:
                    match = re.search(r'CERRAR:\s*(\S+)', line)
                    if match:
                        prog = match.group(1).lower()
                        subprocess.run(["pkill", "-f", prog])
                        found_action = True

            chat_history.append({'role': 'user', 'content': user_text})
            chat_history.append({'role': 'assistant', 'content': ai_response})
            
            if found_action:
                if len(chat_history) > 4: chat_history.pop(0)
            
            speak(ai_response)
            
        except Exception:
            pass
        
        set_status("ESPERANDO...", "#2ecc71")
        main_window.after(300, start_voice_thread)

def start_voice_thread():
    threading.Thread(target=listen_and_process, daemon=True).start()

def update_interface(message, sender):
    chat_display.config(state=tk.NORMAL)
    tag = "user_text" if sender == "user" else "ai_text" if sender == "ai" else "sys_text"
    chat_display.insert(tk.END, message, tag)
    chat_display.see(tk.END)
    chat_display.config(state=tk.DISABLED)

def set_status(text, color):
    status_label.config(text=text, fg=color)

main_window = tk.Tk()
main_window.title("Llama 3 OS Assistant")
main_window.geometry("600x550")
main_window.configure(bg="#1a1a2e")

chat_display = scrolledtext.ScrolledText(
    main_window, wrap=tk.WORD, bg="#16213e", fg="#ffffff", 
    font=("Segoe UI", 11), state=tk.DISABLED, padx=10, pady=10
)
chat_display.tag_config("user_text", foreground="#00d2ff")
chat_display.tag_config("ai_text", foreground="#ffffff")
chat_display.tag_config("sys_text", foreground="#555555", font=("Segoe UI", 9, "italic"))
chat_display.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

status_label = tk.Label(
    main_window, text="INICIALIZANDO...", 
    bg="#1a1a2e", fg="#2ecc71", font=("Arial", 12, "bold")
)
status_label.pack(pady=10)

main_window.after(1000, start_voice_thread)
main_window.mainloop()