# Write a class to hold player information, e.g. what room they are in
# currently.
from item import Item
class Player:
  def __init__(self, room, inventory = []):
    self.room = room
    self.inventory = inventory

  def goToRoom(self, room):
    self.room = room

  def getItem(self, loot, qty = 1):
    # remove item from room
    availableQty = self.room.dropItem(loot, qty)
    # add item to player inventory
    if availableQty > 0:
      if loot.name not in [item.name for item in self.inventory]:
        newItem = Item(loot.name, loot.description, availableQty)
        self.inventory.append(newItem)
        newItem.on_take(availableQty)
      else:
        for item in self.inventory:
          if item.name == loot.name:
            item.qty += availableQty
            item.on_take(availableQty)
    else:
      print('No such item available in this room!')

  def dropItem(self, loot, qty = 1):
    # remove item from player inventory
    availableQty = 0
    for i, item in enumerate(self.inventory):
      if item.name == loot.name:
        if item.qty >= qty:
          availableQty = qty
        else:
          availableQty = qty + (item.qty - qty)
        item.qty -= availableQty
        item.on_drop(availableQty)
        if item.qty <= 0:
          self.inventory.pop(i)
    # add item to player room
    if availableQty > 0:
      self.room.getItem(loot, availableQty)
    else:
      print('Can\'t drop an item that\'s not in your possession!')