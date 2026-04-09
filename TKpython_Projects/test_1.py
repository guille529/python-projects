import tkinter as tk
from tkinter import ttk

# --- FUNCIONES DE TRANSICIÓN ---
def mostrar_juego():
    # Ocultamos el frame de reglas y mostramos el del juego
    frame_reglas.pack_forget()
    frame_juego.pack(fill="both", expand=True)

def mostrar_reglas():
    # Por si quieres regresar: ocultamos juego y mostramos reglas
    frame_juego.pack_forget()
    frame_reglas.pack(fill="both", expand=True)

# --- CONFIGURACIÓN DE LA VENTANA ---
ventana = tk.Tk()
ventana.title("Bagels Game")
ventana.geometry("400x300")

# --- PÁGINA 1: REGLAS ---
frame_reglas = tk.Frame(ventana)
frame_reglas.pack(fill="both", expand=True) # Se muestra al inicio

label_titulo = ttk.Label(frame_reglas, text="REGLAS DEL JUEGO", font=("Arial", 14, "bold"))
label_titulo.pack(pady=10)

texto_reglas = "1. Pico: Posición incorrecta.\n2. Fermi: Posición correcta.\n3. Bagels: Nada correcto."
label_info = ttk.Label(frame_reglas, text=texto_reglas, justify="left")
label_info.pack(pady=20)

boton_siguiente = ttk.Button(frame_reglas, text="Siguiente", command=mostrar_juego)
boton_siguiente.pack(pady=10)


# --- PÁGINA 2: EL JUEGO (OCULTA AL PRINCIPIO) ---
frame_juego = tk.Frame(ventana)

label_juego = ttk.Label(frame_juego, text="¡El juego ha comenzado!", font=("Arial", 12))
label_juego.pack(pady=20)

# Input para que el usuario escriba su número
entrada_usuario = ttk.Entry(frame_juego)
entrada_usuario.pack(pady=5)

boton_adivinar = ttk.Button(frame_juego, text="Adivinar")
boton_adivinar.pack(pady=10)

boton_volver = ttk.Button(frame_juego, text="Volver a reglas", command=mostrar_reglas)
boton_volver.pack(pady=20)

# --- ARRANCAR ---
ventana.mainloop()