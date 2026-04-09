import random
import tkinter as tk
from tkinter import ttk

secret_number = str(random.randint(100, 999))
attempts = 1
max_attempts = 10

def show_game():
    frame_rules.pack_forget()
    frame_game.pack(fill="both", expand=True)

def show_rules():
    frame_game.pack_forget()
    frame_rules.pack(fill="both", expand=True)

def reset_game():
    global secret_number, attempts
    secret_number = str(random.randint(100, 999))
    attempts = 1
    label_history.config(text="")
    label_message.config(text="Guess the number!")
    button_guess.config(state="normal")
    user_entry.delete(0, tk.END)

def evaluate_guess():
    global attempts
    
    guess = user_entry.get()

    if len(guess) != 3 or not guess.isdigit():
        label_message.config(text="Please enter a valid 3-digit number.")
        return

    if guess == secret_number:
        label_message.config(text=f"Congratulations! It was {secret_number}.")
        button_guess.config(state="disabled")
        return

    clues = []
    for i in range(3):
        if guess[i] == secret_number[i]:
            clues.append("Fermi")
        elif guess[i] in secret_number:
            clues.append("Pico")

    if len(clues) == 0:
        result = "Bagels"
    else:
        clues.sort()
        result = " ".join(clues)

    current_history = label_history.cget("text")
    new_text = f"{current_history}\nGuess #{attempts}: {guess} -> {result}"
    label_history.config(text=new_text)

    attempts += 1
    user_entry.delete(0, tk.END)

    if attempts > max_attempts:
        label_message.config(text=f"Game Over. The number was: {secret_number}")
        button_guess.config(state="disabled")

window = tk.Tk()
window.title("Bagels Game")
window.geometry("500x500")

frame_rules = ttk.Frame(window)
frame_rules.pack(fill="both", expand=True)

rules_text = """
Welcome to the Bagels Game!

I am thinking of a secret 3-digit number. 
Your goal is to guess it in 10 attempts.

Clues:
- Pico: One digit is correct but in the wrong position.
- Fermi: One digit is correct and in the right position.
- Bagels: No digits are correct.

Press "Next" to start the game.
"""

label_title = ttk.Label(frame_rules, text="GAME RULES", font=("Arial", 20, "bold"))
label_title.pack(pady=10)

label_info = ttk.Label(frame_rules, text=rules_text, justify="left", font=("Arial", 11))
label_info.pack(pady=20)

button_next = ttk.Button(frame_rules, text="Next", command=show_game)
button_next.pack(pady=10)

frame_game = ttk.Frame(window)

label_game_title = ttk.Label(frame_game, text="Game Started!", font=("Arial", 16, "bold"))
label_game_title.pack(pady=10)

label_message = ttk.Label(frame_game, text="Guess the number!", font=("Arial", 16, "bold"))
label_message.pack(pady=5)

user_entry = ttk.Entry(frame_game, font=("Arial", 14), width=10, justify="center")
user_entry.pack(pady=5)

window.bind('<Return>', lambda event: evaluate_guess() if frame_game.winfo_ismapped() else None)

button_guess = ttk.Button(frame_game, text="Guess", command=evaluate_guess)
button_guess.pack(pady=5)

label_history = ttk.Label(frame_game, text="", font=("Courier", 10), justify="center")
label_history.pack(pady=10)

frame_bottom_buttons = ttk.Frame(frame_game)
frame_bottom_buttons.pack(side="bottom", pady=20)

button_reset = ttk.Button(frame_bottom_buttons, text="New Game", command=reset_game)
button_reset.pack(side="left", padx=5)

button_back = ttk.Button(frame_bottom_buttons, text="Show Rules", command=show_rules)
button_back.pack(side="left", padx=5)

window.mainloop()