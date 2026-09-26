#iter
mytuple = ("apple", "banana","cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))

#string iter
mystr="banana"
myiit = iter(mystr)

print(next(myiit))
print(next(myiit))
print(next(myiit))
print(next(myiit))
print(next(myiit))
print(next(myiit))

#looping
mytuple = ("apple", "banana", "cherry")

for x in mytuple:
    print(x)

myystr = "banana"

for x in myystr:
    print(x)

#create an iterator
class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        x=self.a
        self.a +=1
        return x

myclass = MyNumbers()
myiterr = iter(myclass)

print (next(myiterr))
print (next(myiterr))
print (next(myiterr))
print (next(myiterr))
print (next(myiterr))

#stopiteration
class MyNumbers:
    def __iter__(self):
        self.a=1
        return self
    def __next__(self):
        if self.a<=20:
            x=self.a
            self.a +=1
            return x
        else:
            raise StopIteration

myClass = MyNumbers()
MyIter = iter(myclass)

for x in MyIter:
    print(x)


#yield
def fun(max):
    cnt=1
    while cnt<=max:
        yield cnt
        cnt +=1

ctr = fun(5)
for n in ctr:
    print (n)

#return
def fun():
    return 1+2+3

res = fun()
print(res)

#generator

sq = (x*x for x in range (1,6))
for i in sq:
    print(i)



