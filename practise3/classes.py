#getsring and printstring
class String:
    def getString(self):
        self.text = input()

    def printString(self):
        print(self.text.upper())


s = String()
s.getString()
s.printString()

#shape and square

class Shape:
    def area(self):
        print(0)


class Square(Shape):
    def __init__(self, length):
        self.length = length

    def area(self):
        print(self.length * self.length)


s = Square(5)
s.area()

#point class

import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(self.x, self.y)

    def move(self, x, y):
        self.x = x
        self.y = y

    def dist(self, point):
        return math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)


p1 = Point(2, 3)
p2 = Point(5, 7)

p1.show()
p1.move(4, 6)
p1.show()

print(p1.dist(p2))


#bank account

class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print("Balance:", self.balance)

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print("Balance:", self.balance)
        else:
            print("Not enough money")


account = Account("KBTU", 1000)

account.deposit(500)
account.deposit(200)
account.withdraw(300)
account.withdraw(2000)

#filter and lambda

numbers = [1, 2,  3, 4, 5, 6, 7, 8, 9, 10]
prime = lambda x: x > 1 and all(x%i !=0 for i in range(2, int(x ** 0.5) + 1))
result = list(filter(prime, numbers))
print(result)