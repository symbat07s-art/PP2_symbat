#grams to ounces 
def grams_to_ounces(grams):
    return 28.3495231 * grams


grams = float(input())
print(grams_to_ounces(grams))

#fahrenheit to celsius 
def fahrenheit_to_celsius(F):
    return (5 / 9) * (F - 32)


F = float(input())
print(fahrenheit_to_celsius(F))

#chickens and rabbits
def solve(numheads, numlegs):
    rabbits = (numlegs - 2 * numheads) // 2
    chickens = numheads - rabbits

    print("Rabbits:", rabbits)
    print("Chickens:", chickens)


solve(35, 94)

#filter prime
def filter_prime(numbers):
    result = []
    for num in numbers:
        if num > 1:
            prime = True

            for i in range(2, num):
                if num % i == 0:
                    prime = False
                    break

            if prime:
                result.append(num)

    return result
numbers = list(map(int, input().split()))
print(filter_prime(numbers))

#permutations of a string
from itertools import permutations

def all_permutations(text):
    result = permutations(text)

    for p in result:
        print("".join(p))


text = input()
all_permutations(text)

#reverse the words

def reverse_words(text):
    words = text.split()
    words.reverse()
    return " ".join(words)


text = input()
print(reverse_words(text))

# has 33

def has_33(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 3 and nums[i + 1] == 3:
            return True

    return False


print(has_33([1, 3, 3]))
print(has_33([1, 3, 1, 3]))
print(has_33([3, 1, 3]))


#spy_game
def spy_game(nums):
    code = [0, 0, 7]
    index = 0

    for num in nums:
        if num == code[index]:
            index += 1

            if index == 3:
                return True

    return False


print(spy_game([1, 2, 4, 0, 0, 7, 5]))
print(spy_game([1, 0, 2, 4, 0, 5, 7]))
print(spy_game([1, 7, 2, 0, 4, 5, 0]))

#volume of a sphere

import math

def sphere_volume(radius):
    return (4 / 3) * math.pi * radius ** 3


radius = float(input())
print(sphere_volume(radius))

#unique elements

def unique_elements(numbers):
    result = []

    for num in numbers:
        if num not in result:
            result.append(num)

    return result


print(unique_elements([1, 2, 2, 3, 4, 4, 5]))


#palindrome

def is_palindrome(text):
    text = text.replace(" ", "").lower()

    if text == text[::-1]:
        return True
    else:
        return False


text = input()
print(is_palindrome(text))


#histogram 
def histogram(numbers):
    for num in numbers:
        print("*" * num)


histogram([4, 9, 7])

#guess the num

import random

name = input("Hello! What is your name?\n")

number = random.randint(1, 20)
guesses = 0

print("Well,", name + ", I am thinking of a number between 1 and 20.")

while True:
    guess = int(input("Take a guess.\n"))
    guesses += 1

    if guess < number:
        print("Your guess is too low.")
    elif guess > number:
        print("Your guess is too high.")
    else:
        print("Good job,", name + "! You guessed my number in", guesses, "guesses!")
        break

#import functions 

def sphere_volume(radius):
    import math
    return (4 / 3) * math.pi * radius ** 3


def is_palindrome(text):
    text = text.replace(" ", "").lower()
    return text == text[::-1]


