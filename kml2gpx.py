#!/usr/bin/env python

import sys  #need for argv values
import os.path  #need to work with files
import time   #need to work with time
import random #make time at least a little random

print("     Created by Stephen Semmelroth")

#check for correct number of inputs
if len(sys.argv) is 0:
    print("")
    print("Usage kml2pgx.py X.kml Y.gpx")
if len(sys.argv) is 1:
    print("What file are you analyzing?")
    print("")
    print("Usage kml2pgx.py X.kml Y.gpx")
    print("")
    sys.exit()
if len(sys.argv) is 2:
    print("What is your output file called?")
    sys.exit()
if len(sys.argv) > 3:
    print("Too many variables!")

#test input file for LineString (denotes path object) and count
instances=0
try:
    with open(sys.argv[1]) as preprocess:
        for num, line in enumerate(preprocess, 1):
            if "<LineString>" in line:
                instances = instances + 1
                if instances == 1:
                    #coordinates are three lines after LineString designator
                    coordLine = num + 3
            if instances == 1:
                if num == coordLine:
                    #pull out coordinates
                    coordinates = line

#if the file does not exist, it will throw an error
except:
    print("Could not open the file: " + sys.argv[1])
    sys.exit()

#validate input file has one path object
if instances == 0:
    print("No paths found in KML")
    sys.exit()
if instances > 1:
    print("Whoops, too many paths in the KML. Try exporting one path at a time")
    sys.exit()

#validate not overwriting another file with output
if os.path.isfile(sys.argv[2]):
    print("     Output file already exists. Try a new one")
    sys.exit()

#start doing the actual work
print("Great news, there's a path element. Commencing dissection.")

#clean up coordinates data
coordinates = coordinates.lstrip('\t')
coordinates = coordinates.split(',0 ')
del coordinates[-1]
#print(coordinates)
#coordinates array still needs to be split into tuples
#also, KML tuples are backwards from GPX tuples

#create shell of gpx -------------------
#   make the output file
output= open(sys.argv[2],"w+")

#   populate the output file with header data
output.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n")
output.write("<!-- Created with kml2gpx.py by Stephen Semmelroth -->\r\n")
output.write("<!-- Elevation, time, speed, and sat data are all dummy data -->\r\n")
output.write("<gpx version=\"1.1\" creator=\"Stephen Semmelroth\" xmlns=\"http://www.topografix.com/GPX/1/1\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd\">\r\n")
output.write("\r\n")
output.write("<trk>\r\n")
output.write(" <name>"+sys.argv[2]+"</name>\r\n")
output.write(" <trkseg>\r\n")

#build time object to add dummy time
from datetime import datetime
today = datetime.today()
from datetime import timedelta
#iterate each waypoint in path by one second
second = timedelta(seconds=1)
#start path at plus or minus six years from today
randday = timedelta(days=random.randint(-2190,2190))
today = today + randday


#    iterate through coordinate array and write each line
for element in coordinates:
    output.write('  <trkpt lat="')
    output.write(element.split(',')[1])
    output.write('" lon="')
    output.write(element.split(',')[0])
    output.write('"><ele>22.222</ele><time>')
    output.write(today.replace(microsecond=0).isoformat())
    output.write('Z</time><speed>0.000</speed><sat>14</sat></trkpt>\r\n')
    today = today + second

#    write closeout data
output.write(" </trkseg>\r\n")
output.write("</trk>\r\n")
output.write("\r\n")
output.write("</gpx>\r\n")

print("")
print("Well, the conversion didn't fault out! Go take a look at " + sys.argv[2] + " to see if it worked. you may need to rename it with the gpx extension")
print("")