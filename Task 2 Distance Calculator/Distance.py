# google maps api key    AIzaSyBtMWxx528evP5IGAkUNg10CjdpCB7Gha8
# https://developers.google.com/maps/documentation/directions/intro
# http://py-googlemaps.sourceforge.net/

import googlemaps
import json
import requests
import sys
import csv

gmaps = googlemaps.Client(key='AIzaSyB8RHdgEToHGLyQUA71DRyXGQqfoVJgSHs')
# Google Distance Matrix base URL to which all other parameters are attached
base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
shenzhenLocation = '22.542883,114.062996'


cityDictionary = {

}


listOfCities = []
# code to open the excel spreadsheet
counter = 0
with open('cities_china.csv') as File:
    reader = csv.reader(File)
    for row in reader:
        cityDictionary[counter] = {'name': row[0], 'location': '', 'distance': 0}
        listOfCities.append(row[0])
        counter = counter + 1

# Prepare the request details for the assembly into a request URL
payload = {
    'origins': shenzhenLocation,
    'destinations': '|'.join(listOfCities),
    'api_key': 'AIzaSyB8RHdgEToHGLyQUA71DRyXGQqfoVJgSHs'
}

# Assemble the URL and query the web service
distancesRequest = requests.get(base_url, params=payload)

jsonDistances = json.loads(distancesRequest.text)

distances = jsonDistances['rows']
distanceElements = []

for x in range(len(distances)):
    distanceElements = distances[x].get('elements')

for y in range(len(distanceElements)):
    cityDictionary[y]['distance'] = (distanceElements[y].get('distance').get('value'))

for z in range(len(listOfCities)):
    response = gmaps.geocode(listOfCities[z])
    coordinates = response[0].get('geometry').get('location')
    theCoordinates = str(float("{0:.5f}".format(coordinates.get('lat')))) + "," + str(float("{0:.5f}".format(coordinates.get('lng'))))
    cityDictionary[z]['location'] = theCoordinates



string = "hello"


# read csv file of cities in china
