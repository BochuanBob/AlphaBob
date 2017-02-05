# AlphaBob - Transportation
This bundle is used for transportation-related issues in AlphaBob. 

## Dependencies
The dependencies used in transportation bundle includes:
- [Python](https://www.python.org/)
- [MongoDB](https://docs.mongodb.com/)
- [PyMongo](https://api.mongodb.com/python/current/)

Please make sure all above has been properly set up and activated. 

## File Description
This section describes the functions of different files in this bundle. 

### transportation_terminals.json
This is the source file of the detailed data of 3885 transportation terminals around the world. No functions is inside the file. Please strictly keep the integrity of this document. No manual modification shall ever be made to this file, or as if any modification were to be manually made, please keep a record and the adjustment immediately afterwards. 

### transportation_data_localize.py
This script is used to save the data in *transportation_terminals.json* into the local MongoDB. All data in this file is stored in 1 database named *transportation* using 2 collections. Those two are:
- *terminal*, which records the general description of the transportation terminals
- *distance*, which records the distance between the terminals in the collection *terminal*

The documents in collection *terminal* is stored in the format:
``` json
  {
    "code" : "IATA code of the transportation terminal", 
    "icao" : "ICAO code of the terminal", 
    "type" : "Type of the terminal", 
    "name" : "Name of the terminal", 
    "country" : "The country where the terminal locates", 
    "state" : "The state where the terminal locates", 
    "city" : "The city where the terminal locates", 
    "lat" : "The latitude of the terminal", 
    "lon" : "The longitude o the terminal", 
    "tz" : "Timezone at the location of the terminal", 
    "carriers" : "Number of carriers operating at the terminal", 
    "direct_flights" : "Number of direct passage into this terminal" 
  }
```

The documents in collection *distance* is stored in the format:
```json
  {
    "start" : "One end in this distance relation",
    "end" : "Another end in this distance relation",
    "distance" : "The distance between the previous 2 terminals"
  }
```
The order of *start* and *end* in this relation does not matter; it was just for the convenience at the time of calculation. 
