# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%
# reset ide
%reset -f

#%%

from datetime import datetime

import urllib
from skyfield import api as sf
datadir = '/home/g/python/python-skyfield/'
loader = sf.Loader(datadir, expire=False)

import simplekml
kml = simplekml.Kml()


lats = []
lngs = []
elevation = []

satellites = loader.tle('http://celestrak.com/NORAD/elements/stations.txt')
satellite = satellites['ISS (ZARYA)']

now = datetime.utcnow()
ts = loader.timescale()


for i in range(now.hour, now.hour+24):
    t = ts.utc(now.year, now.month, now.day, i, range(0, 59), 0)
    
    geocentric = satellite.at(t)
    subpoint = geocentric.subpoint()
    
    lats.extend(subpoint.latitude.degrees)
    lngs.extend(subpoint.longitude.degrees)
    elevation.extend(subpoint.elevation.m)

lin = kml.newlinestring(name="ISS", description = "ISS - ZARYA",
                        coords=list(zip(lngs, lats, elevation)))

kml.save("/home/g/python/python-skyfield/export/space-station.kml")


#%%

from skyfield.api import load

planets = load('de421.bsp')
earth, mars = planets['earth'], planets['mars']

ts = load.timescale()
t = ts.now()
position = earth.at(t).observe(mars)
ra, dec, distance = position.radec()

print(ra)
print(dec)
print(distance)

#%%

'''
Skyfield can compute geocentric coordinates, as shown in the example above, 
or topocentric coordinates specific to your location on the Earth’s surface:
'''

from skyfield.api import Topos

auckland = earth + Topos('54.4596 S', '48.0096 E')
astrometric = auckland.at(t).observe(mars)
alt, az, d = astrometric.apparent().altaz()

print(alt)
print(az)




#%%
# reset ide
%reset -f

#%%
# get sattellite details

import urllib
from skyfield import api as sf
datadir = '/home/g/python/python-skyfield/'
loader = sf.Loader(datadir, expire=False)
# Satellite TLEs.
celestrak = 'http://celestrak.com/NORAD/elements/'
geosats = loader.tle(celestrak+'geo.txt')
gpssats = loader.tle(celestrak+'supplemental/gps.txt')
sciencesats = loader.tle(celestrak+'science.txt')
stationsats = loader.tle(celestrak+'stations.txt')
tdrss = loader.tle(celestrak+'tdrss.txt')
visualsats = loader.tle(celestrak+'visual.txt')
# Make catalogs indexable by either name or catalog number.
# Also create sats, a merge of the individual ones.
satcats = [geosats, gpssats, sciencesats, stationsats, tdrss, visualsats]
sats = {}
for cat in satcats:
    names = [key for key in cat.keys()]
    for name in names:
        sat = cat[name]
        satnum = sat.model.satnum
        cat[satnum]  = sat
        sats[satnum] = sat
        sats[name]   = sat
def getsat(satid):
    """
    Return a skyfield EarthSatellite.
    
    <satid> is case independent if it is a satellite name (str).
    
    Retrieve directly from CelesTrak by catalog number if not in local database.
    """
    if isinstance(satid, str):
        satid = satid.upper()
    if satid in sats.keys():
        return sats[satid]
    if not isinstance(satid, int):
        msg = 'satid must be an integer for satellites not in the local set'
        raise Exception(msg)
    base = 'http://celestrak.com/cgi-bin/TLE.pl?CATNR='
    url = base + str(satid)
    with urllib.request.urlopen(url) as fd:
        lines = fd.readlines()
    for k, line in enumerate(lines):
        if 'PRE' in line.decode():
            name = lines[k+1].decode().strip()
            if name == 'No TLE found':
                msg = '%i is not in the CelesTrak database!' % satid
                raise Exception(msg)
            tle1 = lines[k+2].decode().strip()
            tle2 = lines[k+3].decode().strip()
            break
    sat = sf.EarthSatellite(tle1, tle2, name)
    return sat
#%%
# provide location stats
    
sat = getsat('ISS (ZARYA)')
print(sat)

