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
base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='
city_Loc = ""
destinationSyntax = "&destinations="
destination_Loc = ""
end_base_url = "&key=AIzaSyDcbgI_lC47VTtIh0tTpAzaOit-7mzmMLc"
cityDictionary = {

}

# opening csv file to output
filename = ""
ofile = open(filename + "distancecitytocapital3.csv", "wb")
columns = "City, Distance\n"
ofile.write(columns)

listOfCities = []
# code to open the excel spreadsheet
counter = 0
with open('DistanceTOEachCityInput.csv') as File:
    reader = csv.reader(File)
    for row in reader:
        cityDictionary[counter] = {'cityName': row[0], 'citylocation': row[1].replace(" ", ","),'capitalName': row[2], 'capitalloc': row[3].replace(" ", ","), 'distance': 0}
        counter = counter + 1

for key in range(len(cityDictionary)):
    # Assemble the URL and query the web service
    city_Loc = cityDictionary.get(key).get('citylocation')
    destination_Loc = cityDictionary.get(key).get('capitalloc')
    distancesRequest = requests.get(base_url + city_Loc + destinationSyntax + destination_Loc + end_base_url)
    jsonDistances = json.loads(distancesRequest.text)
    distances = jsonDistances['rows']
    distanceElements = []
    print str(key) + " " + cityDictionary.get(key).get('cityName')
    # print str(key) + "  " + listOfCities[key]
    for x in range(len(distances)):
        distanceElements = distances[x].get('elements')

    cityDictionary[key]['distance'] = (distanceElements[0].get('distance').get('value'))
    cityRow = cityDictionary.get(key).get('cityName') + "," + str(cityDictionary[key].get('distance') / 1000) + "\n"
    ofile.write(cityRow)

string = "hello"


# read csv file of cities in china
