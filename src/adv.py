from item import Item
from room import Room
from player import Player

# Declare all the rooms
items = [
  Item('Napkin', 'A damaged piece of cloth napkin.', 1),
  Item('Sword', 'A good-looking weapon.', 1),
  Item('Rock', 'Rubble from ancient structures.', 3),
  Item('Coin', 'A golden coin from an ancient civilization.', 2),
]

def createItem(i):
  item = items[i]
  return Item(item.name, item.description, item.qty)

rooms = {
  'outside': Room(
    "Outside Cave Entrance", 
    "North of you, the cave mount beckons", 
    'outside',
    [createItem(2)]
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
  [createItem(2)]
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
player1 = Player(rooms[initialRoom], [])

quitGame = False

def goDirection(direction):
  global player1, allDirections, quitGame
  if direction == 'N' and direction in availableDirections:
    player1.goToRoom(player1.room.n_to)
  elif direction == 'E' and direction in availableDirections:
    player1.goToRoom(player1.room.e_to)
  elif direction == 'S' and direction in availableDirections:
    player1.goToRoom(player1.room.s_to)
  elif direction == 'W' and direction in availableDirections:
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
    ['GET', 'PICK', 'PICKUP', 'LOOT', 'G', 'P', 'L'],
    '<qty> <item-name>, to pick up / loot <qty>x of <item-name> into your inventory',
    '\nExamples: get 1 rock, pick 1 rock, pickup 1 rock, loot 1 rock, g 1 rock, p 1 rock, l 1 rock'
  )
  print(
    ['DROP', 'REM', 'REMOVE', 'DESTROY', 'D', 'R'],
    '<qty> <item-name>, to drop / remove <qty> of <item-name> from your inventory and put back in room',
    '\nExamples: drop 1 rock, rem 1 rock, remove 1 rock, destroy 1 rock, d 1 rock, r 1 rock'
  )
  print('\n')

tutorial()
while not quitGame:
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

  # player inventory 
  print('\nHere\'s what you have:')
  for item in player1.inventory:
    print(f'{item.qty}x [{item.name}] - {item.description}')

  # player move
  print('\n')
  allInput = input("What do you do?\n")
  userInput = allInput.split(' ')[1:]
  userCommand = allInput.split(' ')[:1][0].upper()
  print('\n')

  # execute correct player command
  if userCommand in ['GO', 'GOTO', 'ROOM', 'TRAVEL', 'T']:
    goDirection(userInput[0].upper())
  elif userCommand in ['GET', 'PICK', 'PICKUP', 'LOOT', 'G', 'P', 'L']:
    inputItem = ''.join(userInput[1:]).lower().capitalize()
    inputItem = [item for item in items if item.name == inputItem]
    inputQty = int(userInput[:1][0])
    if len(inputItem) > 0:
      player1.getItem(inputItem[0], inputQty)
    else:
      print('That item does not exist!')
  elif userCommand in ['DROP', 'REM', 'REMOVE', 'DESTROY', 'D', 'R']:
    inputItem = ''.join(userInput[1:]).lower().capitalize()
    inputItem = [item for item in items if item.name == inputItem]
    inputQty = int(userInput[:1][0])
    if len(inputItem) > 0:
      player1.dropItem(inputItem[0], inputQty)
    else:
      print('That item does not exist!')
  elif userCommand in ['Q', 'QUIT', 'EXIT', 'STOP']:
    print("Giving up already? Weak adventurers shouldn't even have started!")
    quitGame = True
  else:
    print('That command is invalid.')
    tutorial()

  print('\n')