# orbital_track_shapefile_creator
Simple script for generating satellite day track shapefile

Inputs are:
year, month, day, step in minutes between track points, two TLE lines, output file path

example for cmd:

python orbital_track_shapefile_creator.py -y 2014 -m 6 -d 21 -s 5 -u "1 25994U 99068A   14172.15370853
  .00000261  00000-0  68078-4 0  9990"  -l "2 25994 098.2112 246.8346 0001762 090.7383 269.4028 14.57122372771643"
  -o "E:\track1.shp"

example for python usage:

import orbital_track_shapefile_creator

orbital_track_shapefile_creator.create_orbital_track_shapefile_for_day (2014,6,21,5,'1 25994U 99068A   14172.15370853  .00000261 00000-0  68078-4 0  9990',   '2 25994 098.2112 246.8346 0001762 090.7383 269.4028    14.57122372771643','E:\\track.shp')

using pyorbital lib by:
Esben S. Nielsen <esn@dmi.dk>; Adam Dybbroe <adam.dybbroe@smhi.se>; Martin Raspaud <martin.raspaud@smhi.se>

using shapefile lib by:
jlawhead@geospatialpython.com

====

by Eduard Kazakov <silenteddie@gmail.com>, 2016
