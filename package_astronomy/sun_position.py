'''
'''
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from datetime import date
import astropy.units as u
from astroplan import Observer
from astropy.time import Time, TimeDelta
from astropy.coordinates import get_sun, EarthLocation, AltAz
from astropy.visualization import astropy_mpl_style
from geopy.geocoders import Nominatim
from plotnine import *
################################################################################



#matplotlib inline
plt.style.use(astropy_mpl_style)
np.set_printoptions(threshold=np.inf)
#loc_names = [ 'Equator', 'North Pole', 'South Pole']
#loc_coord = [
    #EarthLocation.from_geodetic(lon=0,lat=0),
    #EarthLocation.from_geodetic(lon=0,lat=89.9),
    #EarthLocation.from_geodetic(lon=0,lat=-89.9)
#]

loc_names = ['Cape Town','Isle of Wight','Quito','Oslo','Singapore','Punta Arenas','Barcelona','Dunedin']

#capeTownCoord = EarthLocation(lat=-33.918861*u.deg, lon=18.423300*u.deg)
#isleOfWightCoord = EarthLocation(lat=50.6927176*u.deg, lon=-1.3167103*u.deg)

def get_places(loclist):
    """
    Get a dataframe with the names and locations from a list
    of place names.
    Parameters:
        - loclist: list of strings containing locations to be searched on OpenMaps
    Returns:
        pandas.DataFrame with the name of the locations and the position as an
        astropy.EarthLocation
    """
    geolocator = Nominatim(user_agent='SunPosition Python Script V00.00')
    locs = [ geolocator.geocode(loc) for loc in loc_names ]
    cities = [l.address.split(',')[0] for l in locs]
    coords = [ EarthLocation.from_geodetic(lat=l.latitude*u.deg, lon=l.longitude*u.deg) for l in locs ]
    places = pd.DataFrame({'locations': cities,
                           'coordinates': coords})
    return places

def get_places_fromlist(names,coordinates):
    """
    Get a dataframe build from a list of names and a list of EarthLocation objects
    Parameters:
        - names: list of place names
        - coordinates: list of EarthLocation objects
    Returns:
        pandas.DataFrame with the names and locations
    """
    places = pd.DataFrame({'locations': names, 'coordinates': coordinates})
    return places

numDays = 365
oneDay = TimeDelta(1.0,format='jd')
firstDay = Time('2018-01-01 00:00:00',scale='utc')
allDays = [ firstDay + i*oneDay for i in range(numDays) ]

#places = get_places_fromlist(loc_names,loc_coord)
places = get_places(loc_names)

elevations = np.zeros((len(places.locations),len(allDays)))
for ind,(loc,coord) in enumerate(zip(places.locations,places.coordinates)):
    print(f"Computing sun elevations for {loc}")
    observer = Observer(location=coord)
    noons  = [ observer.noon(h,which=u'next') for h in allDays ]
    sunpos = [ observer.sun_altaz(h) for h in noons ]
    elevations[ind,:] = [ az.alt/u.deg for az in sunpos ]


df = pd.DataFrame([d.to_datetime() for d in allDays])
df.columns = [ 'Day' ]
dfelevs = pd.DataFrame(elevations.transpose(),columns=places.locations)
df = df.join(dfelevs).set_index('Day')

dfs = df.stack().reset_index()
dfs.columns = ['day','location','elevation']

p = ggplot(dfs,aes(x='day',y='elevation',color='location')) + geom_line()
p = p + ggtitle('Sun elevations by date and location')
p = p + xlab('Day of year') + ylab('Elevation (degrees)')
p.draw()
