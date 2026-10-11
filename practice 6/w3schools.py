#file handl9ing
f=open("w3schools.txt")
f==open("w3schools.txt", "rt")

#file reading
f = open("w3schools.txt")
print(f.read())

f = open("D:\\myfiles\w3schools.txt")
print(f.read())

with open("demofile.txt") as f:
    print(f.read)

f = open("demofile.txt")
print(f.readline())
f.close()

with open("demofile.txt") as f:
    print(f.read(5))

with open("demofile.txt") as f:
    print(f.readline())

with open("demofile.txt") as f:
    for x in f:
        print(x)

#write create
with open("demofile.txt") as f:
    f.write("now the file has more contenrt")
with open("demofile.txt") as f:
    print(f.read())

with open("demofile.txt", "w") as f:
    f.write("Woops, i have deleted the content")
with open("demofile.txt") as f:
    print(f.read())

f = open("myfile.txt", "x")

#delete files
import os
os.remove("demofile.txt")

import os
if os.path.exists("demofile.txt"):
    os.remove("demofile.txt")
else:
    print("the file does not exists")

import os
os.rmdir("myfolder")

