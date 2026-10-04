#ReGex
import re

txt = "The rain in Spain"
x= re.search("^The.*Spain$", txt)

if x:
    print("Yes!")
else:
    print("No match")

#set of charachters
import re

txt = "The rain Spain"

x= re.findall("[a-m]", txt)
print(x)

#special sequence
import re

txt="That will be 60 dollars"
x=re.findall("\d", txt)
print(x)

#any
import re

txt="hello planet"

x=re.findall("he..o", txt)
print(x)

#starts with
import re

txt="hello planet"

x = re.findall("^hello", txt)
if x:
    print("Yes")
else:
    print("No match")

#ends with

import re
txt="hello planet"
x=re.findall("planet$", txt)
if x:
    print("Yes")
else:
    print("No")

#occurences zero or more
import re
txt="hello planet"
x=re.findall("he.*o", txt)
print(x)

#occurences one or more
import re
txt="hello planet"
x=re.findall("he.+o", txt)
print(x)

#zero or one
import re
txt="hello planet"
x=re.findall("he.?o", txt)
print(x)

#exactly 
import re
txt="hello planet"
x=re.findall("he.{2}o", txt)
print(x)

#either or
import re
txt="The rain in Spain falls mainly in the plain!"

x=re.findall("falls|stays", txt)

print(x)

if x:
    print("yes")
else:
    print("no match")

#flags
import re
txt="Aland"
print(re.findall("\w", txt, re.ASCII))
print(re.findall("\w", txt))
print(re.findall("\w", txt, re.A))

#2
import re
txt="The rain Spain"
print(re.findall("spain", txt, re.DEBUG))

#3
import re
txt="""Hi
my 
name
is
Sally"""
print(re.findall("me.is", txt, re.DOTALL))
print(re.findall("me.is", txt))
print(re.findall("me.is", txt, re.S))

#4
import re
txt="The rain in Spain"
print(re.findall("spain", txt, re.IGNORECASE))
print(re.findall("spain", txt, re.I))

#5
import re
txt="""There
aint much
rain in
Spain"""
print(re.findall("^ain", txt, re.MULTILINE))

#6
import re

txt = "Åland"

print(re.findall("\w", txt, re.UNICODE))
print(re.findall("\w", txt, re.U))

#7
import re

text = "The rain in Spain falls mainly on the plain"

pattern = """
[A-Za-z]* 
ain+      
[a-z]*    
"""

print(re.findall(pattern, text, re.VERBOSE))
print(re.findall(pattern, text))
print(re.findall(pattern, text, re.X))




#special equence
import re
txt= "The rain in Spain"
x=re.findall("\AThe", txt)
print(x)

if x:
    print("Yes")
else:
    print("NO")

#2
import re

txt = "The rain in Spain"

x = re.findall(r"\bain", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#3
import re

txt = "The rain in Spain"

x = re.findall(r"ain\b", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#4
import re

txt = "The rain in Spain"
x = re.findall(r"\Bain", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")


#5
import re

txt = "The rain in Spain"

x = re.findall(r"ain\B", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#6
import re

txt = "The rain in Spain"

x = re.findall("\d", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#7
import re

txt = "The rain in Spain"
x = re.findall("\D", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#8
import re

txt = "The rain in Spain"

x = re.findall("\s", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")


#9
import re

txt = "The rain in Spain"

x = re.findall("\S", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#10
import re

txt = "The rain in Spain"

x = re.findall("\w", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#11
import re

txt = "The rain in Spain"
x = re.findall("\W", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#12
import re

txt = "The rain in Spain"


x = re.findall("Spain\Z", txt)

print(x)

if x:
  print("Yes, there is a match!")
else:
  print("No match")

#sets
import re

txt = "The rain in Spain"
x = re.findall("[arn]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#2
import re

txt = "The rain in Spain"
x = re.findall("[a-n]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#3
import re

txt = "The rain in Spain"

x = re.findall("[^arn]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#4
import re

txt = "The rain in Spain"

x = re.findall("[0123]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#5
import re

txt = "8 times before 11:45 AM"

x = re.findall("[0-9]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#6
import re

txt = "8 times before 11:45 AM"
x = re.findall("[0-5][0-9]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#7
import re

txt = "8 times before 11:45 AM"

x = re.findall("[a-zA-Z]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#8
import re

txt = "8 times before 11:45 AM"
x = re.findall("[+]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")



#findall function
import re
txt="The rain in Spain"
x=re.findall("ai", txt)
print(x)

#no match
import re
txt="The rain in Spain"
x=re.findall("portugal", txt)
print(x)

#the search
import re
txt="The rain in Spain"
x=re.search("\s", txt)
print("The first white space char is located in position:", x.start())

#no match
import re

txt = "The rain in Spain"
x = re.search("Portugal", txt)
print(x)

#the split()
import re

txt = "The rain in Spain"
x = re.split("\s", txt)
print(x)


#maxslit
import re

txt = "The rain in Spain"
x = re.split("\s", txt, 1)
print(x)

#sub()
import re

txt = "The rain in Spain"
x = re.sub("\s", "9", txt)
print(x)

#count
import re

txt = "The rain in Spain"
x = re.sub("\s", "9", txt, 2)
print(x)

#match object
import re

txt = "The rain in Spain"
x = re.search("ai", txt)
print(x) 

#position
import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.span())

#string
import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.string)

#string match
import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.group())








