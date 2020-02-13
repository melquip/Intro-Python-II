# Implement a class to hold room information. This should have name and
# description attributes.
class Item:
  def __init__(self, name, description, qty = 1):
    self.name = name
    self.description = description
    self.qty = qty

  def on_take(self, qty = 1):
    print(f'You have picked up {qty}x [{self.name}]!')
    return self
    
  def on_drop(self, qty = 1):
    print(f'You have dropped {qty}x [{self.name}]!')
    return self