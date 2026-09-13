#while
i = 1
while i <= 5:
    print(i)
    i += 1

#whilebreak
i = 1
while i <= 10:
    print(i)
    if i == 5:
        break
    i += 1

#whilecontinue
i = 0
while i < 5:
    i += 1

    if i == 3:
        continue

    print(i)

#forloop
fruits = ["apple", "banana", "orange"]

for fruit in fruits:
    print(fruit)

#forbreak
fruits = ["apple", "banana", "orange"]

for fruit in fruits:
    print(fruit)

    if fruit == "banana":
        break

#forcontinue
fruits = ["apple", "banana", "orange"]

for fruit in fruits:

    if fruit == "banana":
        continue

    print(fruit)