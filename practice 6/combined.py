#1
import os

path = "."

print("All:", os.listdir(path))

for name in os.listdir(path):
    if os.path.isdir(os.path.join(path, name)):
        print("Directory:", name)

for name in os.listdir(path):
    if os.path.isfile(os.path.join(path, name)):
        print("File:", name)

#2
import os

path = "sample.txt"

print("Exists:", os.path.exists(path))
print("Readable:", os.access(path, os.R_OK))
print("Writable:", os.access(path, os.W_OK))
print("Executable:", os.access(path, os.X_OK))

#3
import os

path = "sample.txt"

if os.path.exists(path):
    print("Filename:", os.path.basename(path))
    print("Directory:", os.path.dirname(os.path.abspath(path)))
else:
    print("Path does not exist")


#4
with open("sample.txt", "r") as file:
    lines = file.readlines()
    print("Number of lines:", len(lines))

#5
items = ["Apple", "Banana", "Orange"]

with open("fruits.txt", "w") as file:
    for item in items:
        file.write(item + "\n")

#6
for letter in range(ord("A"), ord("Z") + 1):
    filename = chr(letter) + ".txt"

    with open(filename, "w") as file:
        file.write("This is " + filename)

#7
with open("sample.txt", "r") as source:
    content = source.read()

with open("copy.txt", "w") as destination:
    destination.write(content)

#8
import os

path = "sample.txt"

if os.path.isfile(path):
    if os.access(path, os.W_OK):
        os.remove(path)
        print("File deleted")
    else:
        print("No write permission")
else:
    print("File does not exist")