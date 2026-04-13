import pyttsx3 as voz
import speech_recognition as sr
import webbrowser
from datetime import datetime
from googlesearch import search
import requests
from bs4 import BeautifulSoup

engine = voz.init()
engine.setProperty('rate', 155)

def say(text):
    print(f"Asistente: {text}")
    engine.say(text)
    engine.runAndWait()

def limpiar_comando(comando):
    relleno = ["por favor", "puedes", "podrías", "necesito", "oye", "quiero", "busca en google", "busca"]
    for palabra in relleno:
        comando = comando.replace(palabra, "")
    return comando.strip()

def buscar_en_web(consulta):
    say(f"Buscando {consulta} en la web...")
    try:
        # Obtenemos el primer resultado de Google
        for j in search(consulta, tld="com", lang='es', num=1, stop=1, pause=2):
            url = j
            
        # Extraemos un resumen rápido de la página
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Buscamos el primer párrafo significativo
        parrafos = soup.find_all('p')
        for p in parrafos:
            if len(p.text) > 50:
                resumen = p.text[:200] + "..."
                return resumen
        return "Encontré un enlace interesante, pero no pude leer un resumen."
    except:
        return "Lo siento, no pude realizar la búsqueda en este momento."

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
    'github': 'https://www.github.com'
}

INTENTOS = {
    'abrir': ['abrir', 'ponme', 'lanza', 've a', 'muéstrame', 'abre'],
    'hora': ['hora', 'qué hora es', 'momento', 'tiempo'],
    'saludo': ['hola', 'buenos días', 'qué tal', 'cómo estás'],
    'salir': ['adiós', 'terminar', 'salir', 'cierra', 'hasta luego', 'duerme'],
    'buscar': ['busca', 'quién es', 'qué es', 'averigua', 'investiga']
}

say("Hola Guillermo. Sistema de búsqueda activado.")

while True:
    comando_crudo = escuchar()
    if not comando_crudo: continue
        
    print(f"Tú: {comando_crudo}")
    
    # Lógica de búsqueda específica
    if any(p in comando_crudo for p in INTENTOS['buscar']):
        consulta = limpiar_comando(comando_crudo)
        respuesta = buscar_en_web(consulta)
        say(respuesta)
        continue

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
            say("¿Qué sitio quieres abrir?")

    elif any(p in comando for p in INTENTOS['hora']):
        ahora = datetime.now().strftime('%I:%M %p')
        say(f"Son las {ahora}")

    elif any(p in comando for p in INTENTOS['saludo']):
        say("Hola. ¿Qué quieres investigar hoy?")

    elif any(p in comando for p in INTENTOS['salir']):
        say("Cerrando. ¡Hasta pronto!")
        break

    else:
        # Si no encaja en nada, lo busca en la web automáticamente
        respuesta = buscar_en_web(comando_crudo)
        say(f"No estoy seguro de ese comando, pero encontré esto: {respuesta}")