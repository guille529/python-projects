import random

print("I am thinking of a 3-digit number.")
print("Try to guess what it is.\n")
print("Here are some clues:")
print("When I say:")
print("pico:   One digit is correct but in the wrong position.")
print("Fermi:  One digit is correct and in the right position.")
print("Bagels: No digit is correct.\n")

secret_number = str(random.randint(100, 999))

Attempts = 1

while Attempts <= 10:
    print(f"\nGuess #{Attempts}")
    guess = input("> ")

    if len(guess) != 3 or not guess.isdigit():
        print("Please enter a valid 3-digit number.")
        continue

    if guess == secret_number:
        print("You did it, congratulations! ")
        break

    Clues = []

    for i in range(3):
        if guess[i] == secret_number[i]:
            Clues.append("Fermi")
        elif guess[i] in secret_number:
            Clues.append("Pico")

    if len(Clues) == 0:
        print("Bagels")
    else:
        print(" ".join(Clues))

    Attempts += 1

if Attempts > 10:
    print(f"\nThe attempts are over. The number was: {secret_number}")