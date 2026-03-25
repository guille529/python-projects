"""
year = int(input("Enter a year: "))

if year <= 1582:
    print("Not within the Gregorian calendar period")
elif year % 4 != 0: 
    print (year , "Common year")
elif year % 100 != 0 :
    print(year , "Leap year")
elif year % 400 != 0 :
    print(year , "Common year")
elif year % 400 == 0 :
    print(year , "Leap year")
"""
"""
secret_number = 777

print(
""
+================================+
| Welcome to my game, muggle!    |
| Enter an integer number        |
| and guess what number I've     |
| picked for you.                |
| So, what is the secret number? |
+================================+
"")
numbre = int(input("Enter an integer number:"))
while numbre != 777:
    print("Ha ha! You're stuck in my loop!")
    numbre = int(input("Enter an integer number:"))
if numbre == secret_number :
    print("Well done, muggle! You are free now.")
"""

import time
tiempo = 0
for tiempo in range(5):
    tiempo = tiempo + 1
    print(tiempo,"Mississippi")
    if tiempo == 5:
        print("Ready or not, here I come!")












