from item import Item
from lightsource import LightSource
from room import Room
from player import Player

# Declare all the rooms
items = [
  Item('Napkin', 'A damaged piece of cloth napkin.', 1),
  Item('Sword', 'A good-looking weapon.', 1),
  Item('Rock', 'Rubble from ancient structures.', 3),
  Item('Coin', 'A golden coin from an ancient civilization.', 2),
  LightSource('Lamp', 'An old but still functioning oil lamp.'),
]

def createItem(i):
  item = items[i]
  if isinstance(item, LightSource):
    return LightSource(item.name, item.description)
  elif isinstance(item, Item):
    return Item(item.name, item.description, item.qty)
  

rooms = {
  'outside': Room(
    "Outside Cave Entrance", 
    "North of you, the cave mount beckons", 
    'outside',
    [createItem(2), createItem(4)]
  ),
  'foyer': Room(
    "Foyer",
    """Dim light filters in from the south. Dusty
passages run north and east.""",
    'foyer',
    [createItem(0), createItem(2)]
  ),
  'overlook': Room(
    "Grand Overlook",
    """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""",
  'overlook',
  [createItem(2)],
  False
  ),
  'narrow': Room(
    "Narrow Passage",
    """The narrow passage bends here from west
to north. The smell of gold permeates the air.""",
    'narrow',
    [createItem(1), createItem(2)]
  ),
  'treasure': Room(
    "Treasure Chamber",
    """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""",
    'treasure',
    [createItem(3)]
  ),
}

print([type(item) for item in rooms['outside'].items])
# Link rooms together

rooms['outside'].n_to = rooms['foyer']
rooms['foyer'].s_to = rooms['outside']
rooms['foyer'].n_to = rooms['overlook']
rooms['foyer'].e_to = rooms['narrow']
rooms['overlook'].s_to = rooms['foyer']
rooms['narrow'].w_to = rooms['foyer']
rooms['narrow'].n_to = rooms['treasure']
rooms['treasure'].s_to = rooms['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
allDirections = ['N', 'E', 'S', 'W']
availableDirections = []
initialRoom = 'outside'
lastLitRoom = rooms[initialRoom]
player1 = Player(rooms[initialRoom], [])

quitGame = False

def main():
  global player1, allDirections, availableDirections, quitGame
  tutorial()
  while not quitGame:
    if player1.isRoomLit():
      # player current location
      print(f"You walked into the Room {player1.room.name}")
      print(f"{player1.room.description}\n")

      # directions you can travel
      availableDirections = [key.split("_")[0].upper() for key, val in vars(player1.room).items() if key not in ['name', 'description', 'key']]
      for direction in allDirections:
        if direction in availableDirections:
          print(f'[{direction}] Looks like a promising path...')
        else:
          print(f'[{direction}] Doesn\'t inpire confidence...')
      
      # room items
      print('\nHere\'s what you can see:')
      for item in player1.room.items:
        print(f'{item.qty}x [{item.name}] - {item.description}')
    else:
      print('It\'s pitch black!')
    # player move
    executeUserInput()

def executeUserInput():
  global player1, allDirections, availableDirections, lastLitRoom, quitGame
  print('')
  allInput = input("What do you do?\n")
  print('\n')
  userInput = allInput.split(' ')[1:]
  userCommand = allInput.split(' ')[:1][0].upper()

  # travel rooms
  if userCommand in ['GO', 'GOTO', 'ROOM', 'TRAVEL', 'T'] and player1.isRoomLit():
    goDirection(userInput[0].upper())
  # pick up items to player inventory
  elif userCommand in ['GET', 'TAKE', 'PICK', 'PICKUP', 'G', 'T', 'P']:
    inputItem = ''.join(userInput[1:]).lower().capitalize()
    inputItem = [item for item in items if item.name == inputItem]
    inputQty = int(userInput[:1][0])
    if len(inputItem) > 0:
      player1.getItem(inputItem[0], inputQty)
    else:
      print('That item does not exist!')
  # drop items back into room
  elif userCommand in ['DROP', 'REM', 'REMOVE', 'DESTROY', 'D', 'R']:
    inputItem = ''.join(userInput[1:]).lower().capitalize()
    inputItem = [item for item in items if item.name == inputItem]
    inputQty = int(userInput[:1][0])
    if len(inputItem) > 0:
      player1.dropItem(inputItem[0], inputQty)
    else:
      print('That item does not exist!')
  # see player inventory
  elif userCommand in ['I', 'INV', 'INVENTORY', 'ITEMS']:
    if player1.isRoomLit():
      if len(player1.inventory) > 0:
        print('\nHere\'s what you have:')
        for item in player1.inventory:
          print(f'{item.qty}x [{item.name}] - {item.description}')
      else:
        print('\nThere is nothing in your inventory!')
    else:
      print('You can\'t find anything in the darkness!')
  # quit the game
  elif userCommand in ['Q', 'QUIT', 'EXIT', 'STOP']:
    print("Giving up already? Weak adventurers shouldn't even have started!")
    quitGame = True
  # room is not lit, new commands available
  elif not player1.isRoomLit():
    if userCommand in ['L', 'LEAVE', 'B', 'BACK']:
      player1.goToRoom(lastLitRoom)
    elif userCommand in ['H', 'HOLD']:
      if player1.holdLightSource():
        print(f"You\'re holding a [{player1.holding.name}]\nand can see much better now!")
      else:
        print("Oh no! You don\'t have any light source available!")
    else:
      print('That command is invalid.')
      tutorial()
  else:
    print('That command is invalid.')
    tutorial()

  print('\n')
    
def goDirection(direction):
  global player1, allDirections, availableDirections, lastLitRoom, quitGame
  if direction == 'N' and direction in availableDirections:
    lastLitRoom = player1.room
    player1.goToRoom(player1.room.n_to)
  elif direction == 'E' and direction in availableDirections:
    lastLitRoom = player1.room
    player1.goToRoom(player1.room.e_to)
  elif direction == 'S' and direction in availableDirections:
    lastLitRoom = player1.room
    player1.goToRoom(player1.room.s_to)
  elif direction == 'W' and direction in availableDirections:
    lastLitRoom = player1.room
    player1.goToRoom(player1.room.w_to)
  elif direction in allDirections and direction not in availableDirections:
    print("Congrats! You just smashed your face on the wall!")
  elif direction not in allDirections:
    print("You seem confused. Try N, E, S or W!")

def tutorial():
  print('Available commands:')
  print(
    ['GO', 'GOTO', 'ROOM', 'TRAVEL', 'T'],
    '<dir>, where <dir> is N, E, S, W, to change rooms',
    '\nExamples: go n, goto e, room s, travel w, t n'
  )
  print(
    ['GET', 'TAKE', 'PICK', 'PICKUP', 'G', 'T', 'P'],
    '<qty> <item-name>, to pick up / loot <qty>x of <item-name> into your inventory',
    '\nExamples: get 1 rock, pick 1 rock, pickup 1 rock, take 1 rock, g 1 rock, p 1 rock, t 1 rock'
  )
  print(
    ['DROP', 'REM', 'REMOVE', 'DESTROY', 'D', 'R'],
    '<qty> <item-name>, to drop / remove <qty> of <item-name> from your inventory and put back in room',
    '\nExamples: drop 1 rock, rem 1 rock, remove 1 rock, destroy 1 rock, d 1 rock, r 1 rock'
  )
  print('\n')

main()
