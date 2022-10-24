import os

files = []
files_path = "./files/raw/"

for file in os.listdir("./files/raw/"):
    if file.endswith(".csv"):
        files.append(os.path.join("./files/raw/", file))

stringito = "hola"
if stringito.endswith("a"):
    print("o")
else:
    print("u")

