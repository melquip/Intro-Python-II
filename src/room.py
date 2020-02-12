# Implement a class to hold room information. This should have name and
# description attributes.
from item import Item
class Room:
  def __init__(self, name, description, key, items = []):
    self.key = key
    self.name = name
    self.description = description
    self.items = items

  def getItem(self, loot, qty = 1):
    if loot.name not in [item.name for item in self.items]:
      self.items.append(Item(loot.name, loot.description, qty))
    else:
      for item in self.items:
        if item.name == loot.name:
          item.qty += qty

  def dropItem(self, loot, qty = 1):
    availableQty = 0
    for i, item in enumerate(self.items):
      if item.name == loot.name:
        if item.qty >= qty:
          availableQty = qty
        else:
          availableQty = qty + (item.qty - qty)
        item.qty -= availableQty
        if item.qty <= 0:
          self.items.pop(i)
    return availableQty