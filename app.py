import matplotlib.pyplot as plt
import numpy as np

import knapsackProblem
import generateItemFile

def showOptions():
  print("""
  1 - Adicionar item na mochila
  2 - Definir ou modificar a capacidade da mochila
  3 - Mostrar itens presentes na mochila
  4 - Mostrar a capacidade atual da mochila
  5 - Carregar arquivo de itens
  6 - Gerar arquivo de itens aleatórios
  7 - Executar Knapsack Problem usando força bruta
  8 - Executar Knapsack Problem usando programação dinâmica
  9 - Gerar resultados para comparação
  0 - Encerrar o programa
  """)

def readFile(fileName: str) -> list[knapsackProblem.Item]:
  with open(fileName, "r") as file:
    data = file.readlines()

  itemsInFile = []

  for line in data:
    aux = line.split('-')
    itemName = aux[0].strip()
    itemData = aux[1].split()
    itemWeight = int(itemData[0])
    itemValue = int(itemData[1])
    itemToAdd = knapsackProblem.Item(itemName, itemWeight, itemValue)
    itemsInFile.append(itemToAdd)

  return itemsInFile

def processingReturnedData(choice: list[int], items: list[knapsackProblem.Item]) -> None:
  for i in range(len(choice)):
    if choice[i] == 1:
      items[i].chosen = True

def addItem(bag: knapsackProblem.Bag, item: knapsackProblem.Item) -> bool:
  return bag.putItem(item)

def resetChoice(items: list[knapsackProblem.Item]) -> None:
  for i in items:
    i.chosen = False

def printItems(items: list[knapsackProblem.Item]):
  for i in range(len(items)):
    if items[i].chosen:
      print(f"""Item {i + 1}: 
  Nome: {items[i].name}
  Valor: {items[i].value}
  Peso: {items[i].weight}
        """)
  resetChoice(items)

def writeOnFile(items: list[knapsackProblem.Item], value: int, weight: int, time: float, fileName: str) -> None:
  with open(fileName, "w") as file:
    file.write(f"Valor da mochila: {value}. Peso utilizado: {weight}.\n")
    file.write("Itens escolhidos:\n")
    for item in items:
      if item.chosen:
        file.write(f"{item.name} - valor: {item.value}, peso: {item.weight}\n")

    file.write(f"Tempo de execução: {time} segundos.\n")
  resetChoice(items)

def check(bag: knapsackProblem.Bag) -> bool:
  if bag.capacity == 0:
    print("Defina a capacidade da mochila antes de executar!")
    return False
  if len(bag.items) == 0:
    print("Mochila vazia, adicione alguns itens.")
    return False

  return True


def generateResults(quantity: int, capacity: int, bag: knapsackProblem.Bag) -> dict:
  results = {}
  generateItemFile.generateFile(quantity)
  fileItems = readFile("itemFile.txt")
  bag.items = fileItems
  bag.capacity = capacity
  results["baseline"] = knapsackProblem.brutalForce(fileItems, bag)
  results["dynamicProgramming"] = knapsackProblem.dynamicProgramming(fileItems, bag)

  return results

def makeGraph(sizes: list[int], times: list[float], fileName: str) -> None:
  name = "Algorithm Baseline" if fileName == "graphBaseline" else "Algorithm Dynamic Programming"
  plt.figure(figsize=(10, 5))

  plt.xticks(sizes)

  plt.bar(sizes, times, color="red")

  plt.xlabel("Tamanho do arquivo de itens")
  plt.ylabel("Tempo de execução (segundos)")
  plt.title(f"Tempo de execução para cada tamanho de arquivo de itens\n{name}")

  plt.savefig(f"{fileName}.png")
  plt.close()


def generateGraphs(results: list[dict]) -> None:
  resultsBaseline = []
  resultsDynamicProgramming = []

  for result in results:
    resultsBaseline.append(result["baseline"])
    resultsDynamicProgramming.append(result["dynamicProgramming"])
  
  timesBaseline = []
  timesDynamicProgramming = []

  for result in resultsBaseline:
    timesBaseline.append(result[3])
    
  for result in resultsDynamicProgramming:
    timesDynamicProgramming.append(result[3])
  
  sizes = [10, 20, 30, 40]

  makeGraph(sizes, times=timesBaseline, fileName="graphBaseline")
  makeGraph(sizes, times=timesDynamicProgramming, fileName="graphDynamicProgramming")

def app():
  bag = knapsackProblem.Bag(0)
  while(True):
    showOptions()
    try:
      option = int(input("Selecione uma opção: "))
    except ValueError:
      print("Digite apenas numeros!")
      continue

    if option == 0: break

    if option == 1:
      name = str(input("Qual o nome do item a ser adicionado: "))
      value = int(input(f"Qual o valor de {name}: "))
      weight = int(input(f"Qual o peso de {name}: "))
      newItem = knapsackProblem.Item(name, weight, value)
      if addItem(bag, newItem):
        print("\nItem adicionado\n")
      else:
        print("\nErro ao adicionar o item\n")
    elif option == 2:
      newCapacity = int(input("Qual a nova capacidade da mochila: "))
      bag.capacity = newCapacity
      print(f"Capacidade definida. Nova capacidade = {newCapacity}")
    elif option == 3:
      if len(bag.items) == 0:
        print("Mochila vazia, adicione alguns itens.")
        continue
      print("Itens na mochila:\n")
      printItems(bag.getItems())
    elif option == 4:
      print(f"A capacidade atual da mochila é: {bag.capacity}")
    elif option == 5:
      print("Certifique-se que o arquivo esta na mesma pasta que o programa!")
      print("As linhas do arquivo devem seguir o seguinte formato: Nome do item - peso valor\n")
      fileName = str(input("Digite o nome do arquivo: "))
      fileItems = readFile(fileName)
      bag.items = fileItems
      print("Itens adicionados do arquivo. Para verificar, mostre os itens usando a opcao 3")
    elif option == 6:
      quantity = int(input("Digite a quantidade de itens a serem adicionados: "))
      generateItemFile.generateFile(quantity)
      print("Arquivo gerado com sucesso! Verifique o arquivo itemFile.txt")
    elif option == 7:
      if not check(bag): continue 
      items = bag.getItems()
      choice, totalValue, totalWeight, runtime = knapsackProblem.brutalForce(items, bag)
      processingReturnedData(choice, items)
      print(f"O algoritmo foi executado. Valor da mochila: {totalValue}. Peso utilizado: {totalWeight}\n")
      writeOnFile(items, totalValue, totalWeight, runtime, f"knapsackProblemBaseline-{len(items)}.txt")
      print(f"Arquivo gerado com os itens escolhidos e o valor e peso utilizados. Para verificar, abra o arquivo knapsackProblemBaseline-{len(items)}.txt.")
    elif option == 8:
      if not check(bag): continue
      items = bag.getItems()
      value, weight, choice, runtime = knapsackProblem.dynamicProgramming(items, bag)
      processingReturnedData(choice, items)
      print(f"O algoritmo foi executado. Valor da mochila: {value}. Peso utilizado: {weight}\n")
      writeOnFile(items, value, weight, runtime, f"knapsackProblemDynamicProgramming-{len(items)}.txt")
      print(f"Arquivo gerado com os itens escolhidos e o valor e peso utilizados. Para verificar, abra o arquivo knapsackProblemDynamicProgramming-{len(items)}.txt.")
    elif option == 9:
      results10 = generateResults(10, 400, bag)
      results20 = generateResults(20, 800, bag)
      results30 = generateResults(30, 1200, bag)
      results40 = generateResults(40, 1600, bag)

      results = [results10, results20, results30, results40]

      generateGraphs(results)

  print("End of program")

app()