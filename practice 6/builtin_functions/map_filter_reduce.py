from functools import reduce

numbers = [1, 2, 3, 4, 5]

squares = list(map(lambda x: x * x, numbers))
print(squares)

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)

total = reduce(lambda x, y: x + y, numbers)
print(total)

value = "25"
print(type(value))
number = int(value)
print(number)
print(type(number))