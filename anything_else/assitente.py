import pyttsx3 as voz
import speech_recognition as sr
import webbrowser
from datetime import datetime

engine = voz.init()
engine.setProperty('rate', 155)

def say(text):
    print(f"Asistente: {text}")
    engine.say(text)
    engine.runAndWait()

def limpiar_comando(comando):
    relleno = ["por favor", "puedes", "podrías", "necesito", "oye", "quiero"]
    for palabra in relleno:
        comando = comando.replace(palabra, "")
    return comando.strip()

def escuchar():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.7)
        print(">>> Te escucho...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
            texto = recognizer.recognize_google(audio, language='es-MX')
            return texto.lower()
        except:
            return ""

SITES = {
    'google': 'https://www.google.com',
    'youtube': 'https://www.youtube.com',
    'instagram': 'https://www.instagram.com',
    'github': 'https://www.github.com',
    'reddit': 'https://www.reddit.com'
}

INTENTOS = {
    'abrir': ['abrir', 'ponme', 'lanza', 've a', 'muéstrame', 'abre'],
    'hora': ['hora', 'qué hora es', 'momento', 'tiempo'],
    'saludo': ['hola', 'buenos días', 'qué tal', 'cómo estás'],
    'salir': ['adiós', 'terminar', 'salir', 'cierra', 'hasta luego', 'duerme']
}

say("Hola Guillermo. Sistema en línea.")

while True:
    comando_crudo = escuchar()
    
    if not comando_crudo:
        continue
        
    print(f"Tú: {comando_crudo}")
    comando = limpiar_comando(comando_crudo)

    if any(p in comando for p in INTENTOS['abrir']):
        encontrado = False
        for sitio in SITES:
            if sitio in comando:
                say(f"Entendido, abriendo {sitio}")
                webbrowser.open(SITES[sitio])
                encontrado = True
                break
        if not encontrado:
            say("Te entendí que quieres abrir algo, pero ¿qué sitio exactamente?")

    elif any(p in comando for p in INTENTOS['hora']):
        ahora = datetime.now().strftime('%I:%M %p')
        say(f"Son las {ahora}")

    elif any(p in comando for p in INTENTOS['saludo']):
        say("Hola. Estoy listo para tus comandos. ¿Qué necesitas?")

    elif any(p in comando for p in INTENTOS['salir']):
        say("Cerrando sesión. ¡Que tengas un excelente día!")
        break

    else:
        say(f"No estoy seguro de cómo ayudarte con eso, pero puedo buscar {comando} en Google si quieres.")