import random

def generateFile(quantity):
  with open("itemFile.txt", "w") as file:
    for i in range(quantity):
      value = random.randint(1, 100)
      weight = random.randint(1, 100)
      file.write(f"Item {i + 1} - {weight} {value}\n")
