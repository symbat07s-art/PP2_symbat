import os 
import shutil
os.makedirs("source", exist_ok=True)
os.makedirs("destination", exist_ok=True)

with open("source/example.txt", "w") as file:
    file.write("Example file")

shutil.copy("source/example.txt", "destination")
