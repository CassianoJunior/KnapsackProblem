import timeit
class Item:
  def __init__(self, name, weight, value) -> None:
      self.name = name
      self.weight = weight
      self.value = value
      self.chosen = False

class Bag:
  def __init__(self, capacity) -> None:
    self.capacity = capacity
    self.items = []
  
  def putItem(self, item: Item) -> bool:
    self.items.append(item)
    return True
  
  def getItems(self) -> list[Item]:
    return self.items

def brutalForce(items: list[Item], bag: Bag) -> tuple[list[int], int, int, float]:
  data = []
  def execute(items: list[Item], bag: Bag, data):
    A = [0]*len(items)
    bestChoice = [0]*len(items)
    bestValue = 0
    bestWeight = 0
    for i in range(0, 2**(len(items))):
      tempWeight = 0
      tempValue = 0
      j = len(items) - 1
      while (A[j] != 0) and (j > 0):
        A[j] = 0
        j = j-1
      A[j] = 1
      for k in range(0, len(items)):
        if A[k] == 1:
          tempWeight += items[k].weight
          tempValue += items[k].value
      if (tempValue > bestValue) and (tempWeight <= bag.capacity):
        bestValue = tempValue
        bestWeight = tempWeight
        bestChoice = A[:]
            
    data.append(bestChoice)
    data.append(bestValue)
    data.append(bestWeight)
    
  runtime = timeit.timeit(lambda: execute(items, bag, data), number=1)
  return data[1], data[2], data[0], runtime

brutalForce([Item("A", 1, 1), Item("B", 2, 2), Item("C", 3, 3), Item("D", 4, 4), Item("E", 5, 5)], Bag(10))

def knapsackProblemGreedy(items: list[Item], bag: Bag, index: int = 0) -> int:
  if len(items) == index or bag.capacity <= 0:
    return 0
  
  if items[index].weight <= bag.capacity :
    valueIfPut = knapsackProblemGreedy(items, Bag(bag.capacity - items[index].weight), index+1) + items[index].value
    valueIfNotPut = knapsackProblemGreedy(items, bag, index+1)
    return max(valueIfPut, valueIfNotPut)
  else:
    valueIfNotPut = knapsackProblemGreedy(items, bag, index+1)
    return valueIfNotPut

def __generateMatriz(sizeItems: int, sizeCapacity: int) -> list[list[int]]:
  matriz = []
  for i in range(sizeItems+1):
    linha = []
    for j in range(sizeCapacity+1):
      if i == 0 or j == 0:
        linha.append(0)
      else:
        linha.append(-1)
    matriz.append(linha)
  
  return matriz

def __knapsackProblemRecursive(quantity: int, values: list[int], weights: list[int], bagCapacity: int, matriz: list[list[int]]) -> int:
  if matriz[quantity][bagCapacity] == -1:
    if weights[quantity-1] > bagCapacity:
      matriz[quantity][bagCapacity] = __knapsackProblemRecursive(quantity-1, values, weights, bagCapacity, matriz)
    else:
      useItem = values[quantity-1] + __knapsackProblemRecursive(quantity-1, values, weights, bagCapacity - weights[quantity-1], matriz)
      notUseItem = __knapsackProblemRecursive(quantity-1, values, weights, bagCapacity, matriz)
      matriz[quantity][bagCapacity] = max(useItem, notUseItem)

  return matriz[quantity][bagCapacity]

def dynamicProgramming(items: list[Item], bag: Bag) -> tuple[int, int, list[int], float]:
  matriz = __generateMatriz(len(items), bag.capacity)
  values = []
  weights = []

  for item in items:
    values.append(item.value)
    weights.append(item.weight)
  
  value = __knapsackProblemRecursive(len(items), values, weights, bag.capacity, matriz)
  runtime = timeit.timeit(lambda: __knapsackProblemRecursive(len(items), values, weights, bag.capacity, matriz), number=1)

  choise = [0 for i in range(len(items))]

  capacity = bag.capacity
  totalValue = value

  for i in range(len(items), 0, -1):
    if totalValue <= 0:
      break
    if totalValue == matriz[i - 1][capacity]:
      continue
    else:
      choise[i - 1] = 1     
      totalValue -= values[i - 1]
      capacity -= weights[i - 1]
  
  weight = 0
  for i in range(len(items)):
    if choise[i] == 1:
      weight += items[i].weight

  return value, weight, choise, runtime