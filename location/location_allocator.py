'''
location_allocator.py
  Function: This is an algorithm to divide the given places
            to several areas according to their geolocation.

  Author: Bochuan Lu
  Date: Feb. 5, 2017
'''

# Import the Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

PLACE_TYPES=['amusement_park','park','museum','zoo','aquarium']

'''
allocation_location_visualizer:
  visualize the output clusters.
  parameter: coordinates, a matrix with latitude and longtitude
             y_hc, an array to indicate cluster id to the corresponding location 
'''    
def allocation_location_visualizer(coordinates,y_hc):
    # Visualising the clusters
    color = ['red', 'blue', 'green', 'cyan', 'magenta']
    for i in range(0,5):
        plt.scatter(coordinates[y_hc == i, 0],
                    coordinates[y_hc == i, 1],
                    c = color[i], s = 100, label = "Area: " + str(i))
    plt.title('Location Allocation')
    plt.xlabel('Latitude')
    plt.ylabel('Longtitude')
    plt.legend()
    plt.show()

'''
allocate_location
  Take in an json file with the information of places
  and allocate those places to different areas according to the locations.
  parameter: clusters_num, how many areas you want to divide into
             filename: the name of JSON file
             lowest_rate: the lowest rating of those places to get into our data set to make calculation.
  Outputs:   A object with the prediction function which can determine the area with given latitude and longtitude.
'''  
def allocate_location(clusters_num,filename,lowest_rate):
    # Import the location dataset
    data_str=open(filename).read()
    json_data=json.loads(data_str)
    places=[]
    
    # Get the places information and store them into an array.
    # Each place contains name, latitude, longtitude 
    # and rating.(If rating information is lost, it is -1)
    for place_type in PLACE_TYPES:
        for place in json_data[place_type]['results']:
            if not 'rating' in place:
                place['rating']=-1
            info = [place['name'],place['geometry']['location']['lat'],place['geometry']['location']['lng'],place['rating']]
            places.append(info)
    
    # Convert places to matrix for our calculations.
    places=np.matrix(places)
    rating=np.array(places[:,3]).astype(float).ravel()
    
    # filter_places are places with rating higher than given value.
    filter_places=places[rating>=lowest_rate,:]
    coordinates=filter_places[:,1:3].astype(float)
    
    # Fitting hierarchical clustering to the coordinates.
    from sklearn.cluster import AgglomerativeClustering
    hc = AgglomerativeClustering(n_clusters = clusters_num, affinity ='euclidean',
                                 linkage = 'ward')
    y_hc = hc.fit_predict(coordinates)
    allocation_location_visualizer(coordinates,y_hc)
    return hc


def main():    
    allocate_location(5,'attraction.json',4.5)    
#%reset -f
        

