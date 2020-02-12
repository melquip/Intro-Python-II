from room import Room
from player import Player

# Declare all the rooms

room = {
  'outside': Room("Outside Cave Entrance", "North of you, the cave mount beckons", 'outside'),
  'foyer': Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", 'foyer'),
  'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""", 'overlook'),
  'narrow': Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", 'narrow'),
  'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""", 'treasure'),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

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

initialRoom = 'outside'
player1 = Player(room[initialRoom])

quitGame = False
while not quitGame:
  print('\n')
  print(f"You walked into the Room {player1.room.name}")
  print(f"{player1.room.description}\n")

  allDirections = ['N', 'E', 'S', 'W']
  availableDirections = [key.split("_")[0].upper() for key, val in vars(player1.room).items() if key not in ['name', 'description', 'key']]
  
  for direction in availableDirections:
    print(f'[{direction}]')

  print('\n')
  decision = input("What do you do?\n").upper()
  print('\n')

  if decision == 'N' and decision in availableDirections:
    player1.goToRoom(player1.room.n_to)
  elif decision == 'E' and decision in availableDirections:
    player1.goToRoom(player1.room.e_to)
  elif decision == 'S' and decision in availableDirections:
    player1.goToRoom(player1.room.s_to)
  elif decision == 'W' and decision in availableDirections:
    player1.goToRoom(player1.room.w_to)
  elif decision == 'Q':
    print("Giving up already? Weak adventurers shouldn't even have started!")
    quitGame = True
  elif decision in allDirections and decision not in availableDirections:
    print("Congrats! You just smashed your face on the wall!")
  elif decision not in allDirections:
    print("You seem confused. Try N, E, S or W!")