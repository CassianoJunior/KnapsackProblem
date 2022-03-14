from array import array


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
    if self.searchItem(item):
      return False

    self.items.append(item)
    return True

  def searchItem(self, item: Item) -> bool:
    for i in self.items:
      if i.weight == item.weight and i.value == item.value:
        return True

    return False
  
  def getItems(self) -> list[Item]:
    return self.items


# items = []
# item1 = Item("Nome 1", 2, 5)
# item2 = Item("Nome 1", 4, 2)
# item3 = Item("Nome 1", 2, 10)
# item4 = Item("Nome 1", 10, 20)
# item5 = Item("Nome 1", 4, 1)

# items.append(item1)
# items.append(item2)
# items.append(item3)
# items.append(item4)
# items.append(item5)

# bag = Bag(12)

def brutalForce(items: list[Item], bag: Bag) -> tuple[list[int], int, int]:
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
            
  return bestChoice, bestValue, bestWeight

# def knapsackProblem(items, bag, index = 0):
#   if len(items) == index or bag.capacity <= 0:
#     return 0
  
#   if items[index].weight <= bag.capacity :
#     valueIfPut = knapsackProblem(items, Bag(bag.capacity - items[index].weight), index+1) + items[index].value
#     valueIfNotPut = knapsackProblem(items, bag, index+1)
#     return max(valueIfPut, valueIfNotPut)
#   else:
#     valueIfNotPut = knapsackProblem(items, bag, index+1)
#     return valueIfNotPut