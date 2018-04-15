# google maps api key    AIzaSyBtMWxx528evP5IGAkUNg10CjdpCB7Gha8
# https://developers.google.com/maps/documentation/directions/intro
# http://py-googlemaps.sourceforge.net/
# Author. Alejandro Chew
import googlemaps
import json
import requests
import sys
import csv

shenzhenLocation = '22.542883,114.062996'

maps = googlemaps.Client(key='AIzaSyBcj_HbD89hlzNCs120yX_PBRmJ3Eejc88')
# Google Distance Matrix base URL to which all other parameters are attached
base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
before_end = '&location='
end_base_url = "&radius=3500&keyword="
end_end = "&key=AIzaSyBcj_HbD89hlzNCs120yX_PBRmJ3Eejc88"
cityDictionary = {

}

cityNames = []
listOfCities = []
# code to open the excel spreadsheet
counter = 0
with open('cities_only_lat_long.csv') as File:
    reader = csv.reader(File)
    for row in reader:
        cityDictionary[counter] = {'name': row[0], 'location': '', 'distance': 0}
        listOfCities.append(row[0].replace(" ", ","))
        counter = counter + 1

with open('cityname_only.csv') as File2:
    reader = csv.reader(File2)
    for row in reader:
        cityNames.append(row[0])


for key in range(len(listOfCities)):
    # Assemble the URL and query the web service
    theUrl = base_url + listOfCities[key] + end_base_url + cityNames[key] + end_end
    distancesRequest = requests.get(theUrl)
    jsonDistances = json.loads(distancesRequest.text)
    # jsonDistances.

    string = "hello"
    # distances = jsonDistances['rows']
    # distanceElements = []
    # # print str(key) + "  " + listOfCities[key]
    # for x in range(len(distances)):
    #     distanceElements = distances[x].get('elements')


    # cityDictionary[key]['distance'] = (distanceElements[0].get('distance').get('value'))



for z in range(len(listOfCities)):
    print str(z) + "  " + listOfCities[z]
    response = gmaps.geocode(listOfCities[z])
    coordinates = response[0].get('geometry').get('location')
    theCoordinates = str(float("{0:.5f}".format(coordinates.get('lat')))) + "," + str(float("{0:.5f}".format(coordinates.get('lng'))))
    cityDictionary[z]['location'] = theCoordinates

# opening csv file to output
filename = ""
ofile = open(filename + "stateOfCities.csv", "wb")

columns = "City, Latitude, Longitud, Distance\n"
ofile.write(columns)
for cities in range(len(cityDictionary)):
    cityRow = str(cityDictionary[cities].get('distance') / 1000) + "\n"
    ofile.write(cityRow)


string = "hello"


# read csv file of cities in china
