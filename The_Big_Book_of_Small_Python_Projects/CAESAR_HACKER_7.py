abecedario_dict = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 
    'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 
    'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 
    'Z': 25
}

num_to_letter = {v: k for k, v in abecedario_dict.items()}

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

print('Caesar Cipher Hacker')
print('The Caesar cipher encrypts letters by shifting them over by a key number.\n')

while True:
    print('Do you want to use brute (f)orce, or try a (k)ey?')
    choice = input("> ").lower()

    if choice in ['f', 'k']:
        action = 'decrypt with a key' if choice == 'k' else 'decrypt using brute force'
        print(f"Enter the message to {action}:")
        user_message = input("> ")
        
        if choice == 'k':
            try:
                print("Enter the key number (1 - 100):") 
                user_key = int(input("> "))
                print(f"\nDecrypted message: {decrypt(user_message, user_key)}")
                break
            except ValueError:
                print("\nError: The key must be a number.\n")
                continue
        else:
            
            start_key = 1
            max_limit = 100
            
            while start_key <= max_limit:
                
                end_key = min(start_key + 9, max_limit)
                
                print(f"\n--- Testing keys {start_key} to {end_key} ---")
                for key in range(start_key, end_key + 1):
                    print(f"Key {key:03d}: {decrypt(user_message, key)}")
                
                print('\nHas the message been decrypted? (y/n)')
                answer = input('> ').lower()
                
                if answer == 'y':
                    print("\nSuccess! System closed.")
                    break
                else:
                    start_key += 10
            else:
                print("\nReached the limit of 100 keys.")
            break
    else:
        print("\nPlease only respond with 'f' or 'k'.\n")