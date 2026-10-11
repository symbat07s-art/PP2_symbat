import os
print(os.listdir("."))

for name in os.listdir("."):
    if os.path.isdir(name):
        print("Directory:", name)

for name in os.listdir("."):
    if os.path.isfile(name):
        print("File:", name)

for name in os.listdir("."):
    if name.endswith(".py"):
        print(name)
        