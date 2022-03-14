import knapsackProblem

def showOptions():
  print("""
  1 - Adicionar item na mochila
  2 - Definir ou modificar a capacidade da mochila
  3 - Mostrar itens presentes na mochila
  4 - Mostrar a capacidade atual da mochila
  5 - Carregar arquivo de itens
  6 - Executar Knapack Problem usando força bruta
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

def printItems(items: list[knapsackProblem.Item], filtered: bool = False):
  if filtered:
    for i in range(len(items)):
      if items[i].chosen:
        print(f"""Item {i + 1}: 
  Nome: {items[i].name}
  Valor: {items[i].value}
  Peso: {items[i].weight}
        """)
  else:
    for i in range(len(items)):
      print(f"""Item {i + 1}: 
  Nome: {items[i].name}
  Valor: {items[i].value}
  Peso: {items[i].weight}
        """)

def check(bag: knapsackProblem.Bag) -> bool:
  if bag.capacity == 0:
    print("Defina a capacidade da mochila antes de executar!")
    return False
  if len(bag.items) == 0:
    print("Mochila vazia, adicione alguns itens.")
    return False

  return True

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
      print("As linhas do arquivo devem serguir o seguinte formato: Nome do item - peso valor\n")
      fileName = str(input("Digite o nome do arquivo: "))
      fileItems = readFile(fileName)
      bag.items = fileItems
      print("Itens adicionados do arquivo. Para verificar, mostre os itens usando a opcao 3")
    elif option == 6:
      if not check(bag): continue 
      items = bag.getItems()
      resetChoice(items)
      choice, totalValue, totalWeight = knapsackProblem.brutalForce(items, bag)
      processingReturnedData(choice, items)
      print(f"O algoritmo foi executado. Valor da mochila: {totalValue}. Peso utilizado: {totalWeight}\n")
      print("Itens escolhidos:")
      printItems(items, True)

  print("End of program")

app()