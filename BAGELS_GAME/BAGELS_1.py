import random

print("I am thinking of a 3-digit number.")
print("Try to guess what it is.\n")
print("Here are some clues:")
print("When I say:")
print("pico:   One digit is correct but in the wrong position.")
print("Fermi:  One digit is correct and in the right position.")
print("Bagels: No digit is correct.\n")

secret_number = str(random.randint(100, 999))

intentos = 1

while intentos <= 10:
    print(f"\nGuess #{intentos}")
    guess = input("> ")

    if len(guess) != 3 or not guess.isdigit():
        print("Please enter a valid 3-digit number.")
        continue

    if guess == secret_number:
        print("¡Lo lograste, felicidades! 🎉")
        break

    pistas = []

    for i in range(3):
        if guess[i] == secret_number[i]:
            pistas.append("Fermi")
        elif guess[i] in secret_number:
            pistas.append("Pico")

    if len(pistas) == 0:
        print("Bagels")
    else:
        print(" ".join(pistas))

    intentos += 1

if intentos > 10:
    print(f"\nSe acabaron los intentos. El número era: {secret_number}")