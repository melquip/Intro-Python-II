# Implement a class to hold room information. This should have name and
# description attributes.
class Item:
  def __init__(self, name, description, qty = 1):
    self.name = name
    self.description = description
    self.qty = qty