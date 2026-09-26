#1
def square(N):
    for i in range(N+1):
        yield i*i

N=int(input())
for x in square(N):
    print(x)

#2
def even_numbers(n):
    for i in range(n+1):
        if i%2==0:
            yield i
n=int(input())

print(",".join(str(x) for x in even_numbers(n)))

#3
def numbers(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


n = int(input())

for x in numbers(n):
    print(x)

#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


a = int(input())
b = int(input())

for x in squares(a, b):
    print(x)


#5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1


n = int(input())

for x in countdown(n):
    print(x)