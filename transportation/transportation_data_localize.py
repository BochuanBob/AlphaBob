'''
transportation_data_localize.py
  Function: Save data of transportation terminals into 
            local database

  Author: Xiao Xin
  Date: Feb. 4, 2017
'''

import json
import sys
from pymongo import MongoClient
from math import *

# Define static variable
SOCKET = MongoClient('localhost', 27017)                          # Connection to local database server
TRAVEL = SOCKET['transportation']                                 # Database to use
TERMINAL = TRAVEL['terminal']                                     # Collection to save terminal data
DISTANCE = TRAVEL['distance']                                     # Collection to save inter-terminal distance
VALID_TOURIST_TERMINAL_OPTIONS = ['Airport', 'Railway Station',   # Valid types of terminals for tourists
                                  'Heliport', 'Bus Station',
                                  'Harbour']
EARTH_SCALE = 100                                                 # Unit scale used to computer geo-distance

'''
rectify_terminal_type:
  Convert the type of the terminal into a readble word
  
  parameter: data - dictionary containing the data of 
                    a terminal
  return: string - the more reable version of the 
                   terminal type
'''
def rectify_terminal_type(data):
  terminal_type = data['type']
  if terminal_type[-1] == 's' or terminal_type[-1] == '2':
    return terminal_type[:-1]
  return terminal_type

'''
is_valid_tourist_terminal:
  Check whether a terminal is for tourist to use.
  (In order to be a for-tourist terminal, the terminal
   has to be a type defined in VALID_TOURIST_TERMINAL_OPTIONS)

  parameter: data - dictionary containing the data of
                    a terminal
  return: boolean - whether a terminal is ok for tourists to use
'''
def is_valid_tourist_terminal(data):
  return data['type'] in VALID_TOURIST_TERMINAL_OPTIONS

'''
process_terminal_data:
  Remove redundant field in the original data pack for
  terminals, and parse some numerical value into correct
  data type.

  parameter: data - dictionary containing the data of 
                    a terminal
  return: dictionary - a valid, and simplified, object
                       with the data of a terminal
          None - the terminal cannot be used for tourism
'''
def process_terminal_data(data):
  data['type'] = rectify_terminal_type(data)
  if not is_valid_tourist_terminal(data):
    return None
  data['lat'] = float(data['lat'])
  data['lon'] = float(data['lon'])
  data['carriers'] = int(data['carriers'])
  data['direct_flights'] = int(data['direct_flights'])
  del data['woeid']
  del data['phone']
  del data['email']
  del data['url']
  del data['elev']
  del data['runway_length']
  return data

'''
process_terminal:
  Process the data of all terminals from a file and
  save the processed data into local database.

  parameter: source - the source read from the local file
'''
def process_terminal(source):
  source = json.loads(source)
  total = len(source)
  counter = 0
  for data in source:
    terminal = process_terminal_data(data)
    # Only save valid data into database
    if terminal != None:
      TERMINAL.insert_one(terminal)
    counter += 1 
    # Print progress
    sys.stdout.write("\r  Source compilation progress: {}/{}".format(counter, total))
    sys.stdout.flush()
  print

'''
geo_distance:
  Compute the relative distance between two points on 
  earth based on their latitudes and longitudes

  parameter: start, end - terminal objects
  return: float - relative distance between the 2
'''
def geo_distance(start, end):
  start_lat = radians(start['lat'])
  end_lat = radians(end['lat'])
  lon_diff = abs(radians(start['lon'] - end['lon']))
  central_angle_cos = sin(start_lat) * sin(end_lat) + cos(start_lat) * cos(end_lat) * cos(lon_diff)
  # Control the cosine value to be in correct range
  if central_angle_cos >= 1:
    central_angle_cos = 1
  elif central_angle_cos <= -1:
    central_angle_cos = -1
  central_angle = acos(central_angle_cos)
  return EARTH_SCALE * central_angle

'''
terminal_distance:
  Compute inter-terminal distances among all terminals,
  and store the distance relation into local database
'''
def terminal_distance():
  # Retract terminal data from local database
  terminals = TERMINAL.find()
  size = terminals.count()
  total = size * (size - 1) / 2
  counter = 0
  for i in range(size):
    end = terminals[i]
    end['distance'] = []
    for j in range(i):
      start = terminals[j]
      distance = geo_distance(start, end)
      record = {
                 'start': start['code'],
                 'end': end['code'],
                 'distance': distance
               }
      DISTANCE.insert_one(record)
      counter += 1
      # Print progress
      sys.stdout.write("\r  Inter-terminal distance calculation progress: {}/{}".format(counter, total))
      sys.stdout.flush()
  print

def main():
  print 'Initiate transportation terminal data localization ...'

  print '1.Initiate source file loading ...'
  f = open('./transportation_terminals.json')
  source = f.read()
  f.close()
  print '  Source file loading complete'

  print '2.Initiate local database cleanup ...'
  TERMINAL.drop()
  DISTANCE.drop()
  print '  Local database cleanup complete'

  print '3.Initiate source file compilation ...'
  terminals = process_terminal(source)
  print '  Source file compilation complete'

  print '4.Initiate inter-terminal distance calculation ...'
  terminal_distance()
  print '  Inter-terminal distance calculation complete'

  SOCKET.close()
  print 'All tasks has complete, please open mongo shell to check the results'

if __name__ == '__main__':
  main()
