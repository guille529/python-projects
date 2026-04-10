abecedario_dict = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 
    'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 
    'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 
    'Z': 25
}

num_to_letter = {v: k for k, v in abecedario_dict.items()}

def encrypt(message, key):
    result = ""
    message = message.upper() 
    for letter in message:
        if letter in abecedario_dict:
            current_position = abecedario_dict[letter]
            new_position = (current_position + key) % 26
            result += num_to_letter[new_position]
        else:
            result += letter
    return result

def decrypt(message, key):
    result = ""
    message = message.upper() 
    for letter in message:
        if letter in abecedario_dict:
            current_position = abecedario_dict[letter]
            new_position = (current_position - key) % 26
            result += num_to_letter[new_position]
        else:
            result += letter
    return result

print('Caesar Cipher')
print('The Caesar cipher encrypts letters by shifting them over by a')
print('key number.\n')

while True:
    print('Do you want to (e)ncrypt or (d)ecrypt?')
    choice = input("> ").lower()

    if choice in ['e', 'd']:
        action = 'encrypt' if choice == 'e' else 'decrypt'
        print(f"Enter the message to {action}:")
        user_message = input("> ")
        
        print("Enter the key number (1 - 100):")
        try:
            user_key = int(input("> "))
            
            if choice == 'e':
                print("\nEncrypted Message:")
                print(encrypt(user_message, user_key))
            else:
                print("\nDecrypted Message:")
                print(decrypt(user_message, user_key))
            break
            
        except ValueError:
            print("\nError: The key must be a number.\n")
            continue
    else:
        print("\nPlease only respond with 'e' or 'd'.\n")