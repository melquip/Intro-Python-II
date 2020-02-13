from item import Item
class LightSource(Item):
  def __init__(self, name, description):
    super().__init__(name, description, 1)
    self.is_light = True
    
  def on_drop(self, qty = 1):
    print(f'It\'s not wise to drop your source of light!')
    return self