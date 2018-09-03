# kml2gpx

Had some issues converting KML to GPX so I wrote a tool to do it for me. It does some basic error checking. Some GPX import tools require time stamps and Path objects in KML obviously don't timestamp. It's written in Python so don't forget to chmod before running. Yes, it could be done in bash with awk or sed but I haven't programmed in Python for a while so thought it would be fun. Syntax: ./kml2gpx.py inputfile outputfile.gpx.
