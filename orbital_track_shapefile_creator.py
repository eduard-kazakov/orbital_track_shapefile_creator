'''
Simple script for generating satellite day track shapefile
Inputs are:
year, month, day, step in minutes between track points, two TLE lines, output file path

example for cmd:

python orbital_track_shapefile_creator.py -y 2014 -m 6 -d 21 -s 5 -u "1 25994U 99068A   14172.15370853
  .00000261  00000-0  68078-4 0  9990"  -l "2 25994 098.2112 246.8346 0001762 090.7383 269.4028 14.57122372771643"
  -o "E:\track1.shp"

example for python usage:

import orbital_track_shapefile_creator
orbital_track_shapefile_creator.create_orbital_track_shapefile_for_day (2014,6,21,5,'1 25994U 99068A
   14172.15370853  .00000261  00000-0  68078-4 0  9990',
   '2 25994 098.2112 246.8346 0001762 090.7383 269.4028
    14.57122372771643','E:\\track.shp')

using pyorbital lib by:
Esben S. Nielsen <esn@dmi.dk>; Adam Dybbroe <adam.dybbroe@smhi.se>; Martin Raspaud <martin.raspaud@smhi.se>

using shapefile lib by:
jlawhead<at>geospatialpython.com

====

by Eduard Kazakov <silenteddie@gmail.com>, 2016
'''

from optparse import OptionParser
import shapefile
from pyorbital.orbital import Orbital
from pyorbital.tlefile import ChecksumError
import datetime

def create_orbital_track_shapefile_for_day (year, month, day, step_minutes, tle_line1, tle_line2, output_shapefile):
    try:
        orb = Orbital("N",tle_file=None,line1=tle_line1, line2=tle_line2)
    except (ChecksumError):
        print 'Invalid TLE'
        return 2

    try:
        year = int(year)
        month = int(month)
        day = int(day)
        step_minutes = float(step_minutes)
    except:
        print 'Invalid date'
        return 3

    w = shapefile.Writer(shapefile.POINT)
    w.field('ID','C',40)
    w.field('TIME','C',40)
    w.field('LAT','C',40)
    w.field('LON','C',40)

    i = 0
    minutes = 0
    while minutes < 1440:
        utc_hour = int(minutes // 60)
        utc_minutes = int((minutes - (utc_hour*60)) // 1)
        utc_seconds = int(round((minutes - (utc_hour*60) - utc_minutes)*60))

        utc_string = str(utc_hour) + '-' + str(utc_minutes) + '-' + str(utc_seconds)

        utc_time = datetime.datetime(year,month,day,utc_hour,utc_minutes,utc_seconds)

        lon, lat, alt = orb.get_lonlatalt(utc_time)

        w.point(lon,lat)

        w.record(str(i),utc_string,str(lat),str(lon))

        i += 1
        minutes += step_minutes

    try:
        prj = open("%s.prj" % output_shapefile.replace('.shp',''), "w")
        epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
        prj.write(epsg)
        prj.close()
        w.save(output_shapefile)
    except:
        print 'Unable to save shapefile'
        return 4

if __name__ == "__main__":
    usage = "usage: %prog [options] arg"
    parser = OptionParser()
    parser.add_option("-y", "--year", dest="year", help="year")
    parser.add_option("-m", "--month", dest="month", help="month")
    parser.add_option("-d", "--day", dest="day", help="day")
    parser.add_option("-s", "--step", dest="step", help="Step in minutes")
    parser.add_option("-u", "--tle_l1", dest="tle_l1", help="TLE line 1")
    parser.add_option("-l", "--tle_l2", dest="tle_l2", help="TLE line 2")
    parser.add_option("-o", "--output", dest="output", help="Output shapefile")

    options, args = parser.parse_args()
    
    if not options.year or not options.month or not options.day or not options.step or not options.tle_l1 or not options.tle_l2 or not options.output:
        parser.error('Not enough parameters!')

    create_orbital_track_shapefile_for_day (options.year,options.month,options.day,options.step,
                                            options.tle_l1,options.tle_l2,options.output)