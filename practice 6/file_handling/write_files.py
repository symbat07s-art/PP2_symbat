with open("sample.txt") as f:
    f.write("Hello Python!\n")
    f.write("This is sample data\n")

with open("sample.txt", "a") as f:
    f.write("This is a new line\n")

with open("sample.txt", "r") as f:
    print(f.read())

