# Write a class to hold player information, e.g. what room they are in
# currently.
from item import Item
from lightsource import LightSource

class Player:
  def __init__(self, room, inventory = [], holding = None):
    self.room = room
    self.inventory = inventory
    self.holding = holding

  def goToRoom(self, room):
    self.room = room
    return self

  def getItem(self, loot, qty = 1):
    if not self.isRoomLit():
      print('Good luck finding that in the dark!')
      return self
    # remove item from room
    availableQty = self.room.dropItem(loot, qty)
    # add item to player inventory
    if availableQty > 0:
      if loot.name not in [item.name for item in self.inventory]:
        newItem = None
        if isinstance(loot, LightSource):
          newItem = LightSource(loot.name, loot.description)
        elif isinstance(loot, Item):
          newItem = Item(loot.name, loot.description, availableQty)
        if newItem != None:
          self.inventory.append(newItem)
          newItem.on_take(availableQty)
      else:
        for item in self.inventory:
          if item.name == loot.name:
            item.qty += availableQty
            item.on_take(availableQty)
    else:
      print('No such item available in this room!')
    return self

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
      if not self.isRoomLit():
        print('You dropped something in the dark!')
    else:
      print('Can\'t drop an item that\'s not in your possession!')
    return self
  
  def holdItem(self, item):
    self.holding = item
    return self

  def stopHold(self):
    self.holding = None
    return self

  def isRoomLit(self):
    return self.room.is_light or (not self.room.is_light and isinstance(self.holding, LightSource))

  def holdLightSource(self):
    for item in self.inventory:
      if isinstance(item, LightSource):
        self.holdItem(item)
        break
    return isinstance(self.holding, LightSource)