import random

print("Birthday Paradox")
print("\nHow many birthdays shall I generate?")
people = int(input("> "))

birthdays = []
seen = set()
repetidos = []

MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

days_in_month = (31, 28, 31, 30, 31, 30,
                 31, 31, 30, 31, 30, 31)

for i in range(people):
    month = random.randint(1, 12)
    day = random.randint(1, days_in_month[month - 1])

    birthday = (month, day)
    birthdays.append(birthday)

    if birthday in seen:
        repetidos.append(birthday)
    else:
        seen.add(birthday)

print("\nGenerated birthdays:")
for b in birthdays:
    print(f"{MONTHS[b[0] - 1]} {b[1]}")

if len(repetidos) > 0:
    print("\nThere is at least one matching birthday!")
    print("Repeated birthdays:")
    for b in set(repetidos):
        print(f"{MONTHS[b[0] - 1]} {b[1]}")
else:
    print("\nNo matching birthdays.")