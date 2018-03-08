# google maps api key    AIzaSyBtMWxx528evP5IGAkUNg10CjdpCB7Gha8
# https://developers.google.com/maps/documentation/directions/intro
# http://py-googlemaps.sourceforge.net/


import googlemaps

gmaps = googlemaps.Client(key='AIzaSyCsXT2OeX6VLSzitHnpVRcs5cNGA0YlDPg')

#shenzheng latitude
#shengzheng longitude
shenzhengLocation = '22.542883,114.062996'
shanghaiLocation = '24.479834,118.089424'

dirs = gmaps.directions(shenzhengLocation, shanghaiLocation)

string = "hello"


# read csv file of cities in china
