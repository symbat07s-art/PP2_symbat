import os
import shutil

if os.path.exists("sample.txt"):
    shutil.copy("sample.txt", "copy.txt")
    shutil.copy("sample.txt", "backup.txt")
    print("Files copied")

if os.path.isfile("copy.txt") and os.access("copy.txt", os.W_OK):
    os.remove("copy.txt")
    print("File deleted")

else:
    print("File does not exist or cannot be written to")
