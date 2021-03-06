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
gmaps = googlemaps.Client(key='AIzaSyDcbgI_lC47VTtIh0tTpAzaOit-7mzmMLc')
# Google Distance Matrix base URL to which all other parameters are attached
base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=9.00711 7.2634&destinations='
end_base_url = "&key=AIzaSyDcbgI_lC47VTtIh0tTpAzaOit-7mzmMLc"
cityDictionary = {

}


listOfCities = []
# code to open the excel spreadsheet
counter = 0
with open('kanostostates.csv') as File:
    reader = csv.reader(File)
    for row in reader:
        cityDictionary[counter] = {'name': row[0], 'location': '', 'distance': 0}
        listOfCities.append(row[0])
        counter = counter + 1

for key in range(len(listOfCities)):
    # Assemble the URL and query the web service
    distancesRequest = requests.get(base_url + listOfCities[key] + end_base_url)
    jsonDistances = json.loads(distancesRequest.text)
    distances = jsonDistances['rows']
    distanceElements = []
    # print str(key) + "  " + listOfCities[key]
    for x in range(len(distances)):
        distanceElements = distances[x].get('elements')


    cityDictionary[key]['distance'] = (distanceElements[0].get('distance').get('value'))



for z in range(len(listOfCities)):
    print str(z) + "  " + listOfCities[z]
    response = gmaps.geocode(listOfCities[z])
    coordinates = response[0].get('geometry').get('location')
    theCoordinates = str(float("{0:.5f}".format(coordinates.get('lat')))) + "," + str(float("{0:.5f}".format(coordinates.get('lng'))))
    cityDictionary[z]['location'] = theCoordinates

# opening csv file to output
filename = ""
ofile = open(filename + "distancefromkanotostates.csv", "wb")

columns = "City, Latitude, Longitud, Distance\n"
ofile.write(columns)
for cities in range(len(cityDictionary)):
    cityRow = str(cityDictionary[cities].get('distance') / 1000) + "\n"
    ofile.write(cityRow)


string = "hello"


# read csv file of cities in china
