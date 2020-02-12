# Implement a class to hold room information. This should have name and
# description attributes.
class Room:
  def __init__(self, name, description, key, items = []):
    self.key = key
    self.name = name
    self.description = description
    self.items = items