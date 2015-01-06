import random
import argparse

class Alien:
  def __init__(self, id, currently_at):
    self.id = id
    self.currently_at = currently_at
  
  def moveRandomly(self):
    can_move_to_set = self.currently_at.neighbours.values()
    if len(can_move_to_set) == 0:
      return
    can_move_to = list(can_move_to_set)
    self.setTown(random.choice(can_move_to))

  def setTown(self, town):
    if self.currently_at is not None:
      try:
        self.currently_at.aliens_in_town.remove(self)
      except ValueError:
        pass
    if town is not None:
      self.currently_at = town
      self.currently_at.aliens_in_town.append(self)

class Town:
  def __init__(self, name):
    self.name = name
    self.aliens_in_town = []
    self.neighbours = {}
    # self.north = None
    # self.east = None
    # self.south = None
    # self.west = None

  # def neighboursAsList(self):
  #   neighbours = []
  #   if self.north is not None:
  #     neighbours.append(self.north)
  #   if self.east is not None:
  #     neighbours.append(self.east)
  #   if self.south is not None:
  #     neighbours.append(self.south)
  #   if self.west is not None:
  #     neighbours.append(self.west)
  #   return neighbours

  def __str__(self):
    string = self.name
    for key, value in self.neighbours.items():
      string += " {}={}".format(key, value.name)
    # if self.north is not None:
    #   string = string + " north=" + self.north.name
    # if self.east is not None:
    #   string = string + " east=" + self.east.name
    # if self.south is not None:
    #   string = string + " south=" + self.south.name
    # if self.west is not None:
    #   string = string + " west=" + self.west.name
    return string + "\n"

  def destroy(self):
    string = self.name + " has been destroyed by aliens "
    for key, value in self.neighbours.items():
      string += " {}=".format(key, value)
      if key is 'north':
        del value.neighbours['south']
      elif key is 'east':
        del value.neighbours['west']
      elif key is 'south':
        del value.neighbours['north']
      elif key is 'west':
        del value.neighbours['east']
    # if neighbours['north'] is not None:
    #   neighbours['north'].south = None
    # if neighbours['east'] is not None:
    #   neighbours['east'].west = None
    # if neighbours['south'] is not None:
    #   neighbours['south'].north = None
    # if neighbours['west'] is not None:
    #   neighbours['west.east = None
    string = self.name + " has been destroyed by aliens "
    for alien in self.aliens_in_town:
      string += str(alien.id) + ", "
    string = string[:-2] + "!"
    print(string)

def iterateInvasion():
  moveAliensRandomly()
  destroyTowns()

def moveAliensRandomly():
  for alien in aliens:
    alien.moveRandomly()

def destroyTowns():
  destroyed_town_names = []
  for town in towns.values():
    if len(town.aliens_in_town) > 1:
      destroyed_town_names.append(town.name)
      for alien_in_town in town.aliens_in_town:
        aliens.remove(alien_in_town)
      town.destroy()
  for name in destroyed_town_names:
    del towns[name]

def generateTowns():
  file = open(pathname, 'r')
  for line in file:
    createTownAndAddToMap(line)
  file.close()

def generateAliens():
  number_of_aliens = int(input('Please enter the size of the invading alien force: '))
  towns_list = list(towns.values())
  for i in range(number_of_aliens):
    alien = Alien(i, random.choice(towns_list))
    alien.setTown(alien.currently_at)
    aliens.append(alien)

def outputTowns(filename):
  file = open(filename, 'w')
  for town in towns.values():
    file.write(str(town))
  file.close()

def createTownAndAddToMap(input):
  components = input.strip(' \t\n\r').split(" ")
  new_town = getOrCreateTown(components[0].strip(' \t\n\r'))

  for dir in ['north', 'south', 'east', 'west']:
    dir_town = getOrCreateTown(extractTownName(components, dir))
    if dir_town is not None:
      new_town.neighbours[dir] = dir_town

  # new_town.north = getOrCreateTown(extractTownName(components, "north"))
  # new_town.east = getOrCreateTown(extractTownName(components, "east"))
  # new_town.south = getOrCreateTown(extractTownName(components, "south"))
  # new_town.west = getOrCreateTown(extractTownName(components, "west"))

def extractTownName(input, direction):
  for s in input:
    if s.startswith(direction):
      return s[len(direction) + 1:]
  return None

def getOrCreateTown(town_name):
  if town_name is None:
    return None
  if town_name in towns:
    return towns[town_name]
  new_town = Town(town_name)
  towns[town_name] = new_town
  return new_town

parser = argparse.ArgumentParser()
parser.add_argument("inputfile")
args = parser.parse_args()
pathname = args.inputfile

aliens = []
towns = {}

generateTowns()
generateAliens()
for i in range(10000):
  if len(aliens) <= 0:
    break
  iterateInvasion()

outputTowns("output.txt")