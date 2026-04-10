import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- CIPHER LOGIC ---

alphabet_dict = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 
    'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 
    'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 
    'Z': 25
}

num_to_letter = {v: k for k, v in alphabet_dict.items()}

def encrypt(message, key):
    """Shifts letters forward in the alphabet."""
    result = ""
    message = message.upper() 
    for letter in message:
        if letter in alphabet_dict:
            current_position = alphabet_dict[letter]
            new_position = (current_position + key) % 26
            result += num_to_letter[new_position]
        else:
            result += letter
    return result

def decrypt(message, key):
    """Shifts letters backward in the alphabet."""
    result = ""
    message = message.upper() 
    for letter in message:
        if letter in alphabet_dict:
            current_position = alphabet_dict[letter]
            new_position = (current_position - key) % 26
            result += num_to_letter[new_position]
        else:
            result += letter
    return result

# --- NAVIGATION AND ACTION FUNCTIONS ---

def show_encryption():
    choice_frame.pack_forget()
    encrypt_frame.pack(fill="both", expand=True)

def show_decryption():
    choice_frame.pack_forget()
    decrypt_frame.pack(fill="both", expand=True)

def show_choice():
    encrypt_frame.pack_forget()
    decrypt_frame.pack_forget()
    welcome_frame.pack_forget()
    choice_frame.pack(fill="both", expand=True)
    
    # Clear inputs and results
    encrypt_msg_entry.delete(0, tk.END)
    encrypt_key_entry.delete(0, tk.END)
    res_encrypt.config(state='normal')
    res_encrypt.delete(0, tk.END)
    res_encrypt.config(state='readonly')
    
    decrypt_msg_entry.delete(0, tk.END)
    decrypt_key_entry.delete(0, tk.END)
    res_decrypt.config(state='normal')
    res_decrypt.delete(0, tk.END)
    res_decrypt.config(state='readonly')

def show_welcome():
    choice_frame.pack_forget()
    welcome_frame.pack(fill="both", expand=True)

def run_encryption():
    msg = encrypt_msg_entry.get()
    try:
        key = int(encrypt_key_entry.get())
        output = encrypt(msg, key)
        res_encrypt.config(state='normal')
        res_encrypt.delete(0, tk.END)
        res_encrypt.insert(0, output)
        res_encrypt.config(state='readonly')
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric key.")

def run_decryption():
    msg = decrypt_msg_entry.get()
    try:
        key = int(decrypt_key_entry.get())
        output = decrypt(msg, key)
        res_decrypt.config(state='normal')
        res_decrypt.delete(0, tk.END)
        res_decrypt.insert(0, output)
        res_decrypt.config(state='readonly')
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric key.")

# --- MAIN INTERFACE ---

root = tk.Tk()
root.title("Caesar Cipher Tool")
root.geometry("500x500")

# PAGE 1: WELCOME
welcome_frame = tk.Frame(root)
welcome_frame.pack(fill="both", expand=True)

ttk.Label(welcome_frame, text="Caesar Cipher", font=("Arial", 16, "bold")).pack(pady=20)
ttk.Label(welcome_frame, text="Welcome to the encryption tool.\nPress the button below to start.", justify="center").pack(pady=20)
ttk.Button(welcome_frame, text="Start", command=show_choice).pack(pady=10)

# PAGE 2: CHOICE
choice_frame = ttk.Frame(root)
ttk.Label(choice_frame, text="Selection Menu", font=("Arial", 14, "bold")).pack(pady=20)
ttk.Button(choice_frame, text="Encrypt a Message", command=show_encryption).pack(pady=10)
ttk.Button(choice_frame, text="Decrypt a Message", command=show_decryption).pack(pady=10)
ttk.Button(choice_frame, text="Go Back", command=show_welcome).pack(pady=10)

# PAGE 3: ENCRYPT
encrypt_frame = tk.Frame(root)
ttk.Label(encrypt_frame, text="ENCRYPTION MODE", font=("Arial", 12, "bold")).pack(pady=10)
ttk.Label(encrypt_frame, text="Enter message:").pack()
encrypt_msg_entry = ttk.Entry(encrypt_frame, width=40)
encrypt_msg_entry.pack(pady=5)
ttk.Label(encrypt_frame, text="Enter key:").pack()
encrypt_key_entry = ttk.Entry(encrypt_frame, width=10)
encrypt_key_entry.pack(pady=5)
ttk.Button(encrypt_frame, text="Run Encryption", command=run_encryption).pack(pady=10)

ttk.Label(encrypt_frame, text="Result:").pack(pady=5)
res_encrypt = ttk.Entry(encrypt_frame, font=("Arial", 11), justify="center", state="readonly")
res_encrypt.pack(pady=5, fill="x", padx=50)
ttk.Button(encrypt_frame, text="Back to Menu", command=show_choice).pack(pady=20)

# PAGE 4: DECRYPT
decrypt_frame = tk.Frame(root)
ttk.Label(decrypt_frame, text="DECRYPTION MODE", font=("Arial", 12, "bold")).pack(pady=10)
ttk.Label(decrypt_frame, text="Enter message:").pack()
decrypt_msg_entry = ttk.Entry(decrypt_frame, width=40)
decrypt_msg_entry.pack(pady=5)
ttk.Label(decrypt_frame, text="Enter key:").pack()
decrypt_key_entry = ttk.Entry(decrypt_frame, width=10)
decrypt_key_entry.pack(pady=5)
ttk.Button(decrypt_frame, text="Run Decryption", command=run_decryption).pack(pady=10)

ttk.Label(decrypt_frame, text="Result:").pack(pady=5)
res_decrypt = ttk.Entry(decrypt_frame, font=("Arial", 11), justify="center", state="readonly")
res_decrypt.pack(pady=5, fill="x", padx=50)
ttk.Button(decrypt_frame, text="Back to Menu", command=show_choice).pack(pady=20)

root.mainloop()