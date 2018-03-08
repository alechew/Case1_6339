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
with open('cities_china.csv') as File:
    reader = csv.reader(File)
    for row in reader:
        cityDictionary[str(row[0])] = {'name': row[0], 'location': ''}
        listOfCities.append(row[0])

# Prepare the request details for the assembly into a request URL
payload = {
    'origins': shenzhenLocation,
    'destinations': '|'.join(listOfCities),
    'api_key': 'AIzaSyB8RHdgEToHGLyQUA71DRyXGQqfoVJgSHs'
}


# Assemble the URL and query the web service
# r = requests.get(base_url, params=payload)

coordiantes = gmaps.geocode('shanghai+shenzhen')

string = "hello"


# read csv file of cities in china
