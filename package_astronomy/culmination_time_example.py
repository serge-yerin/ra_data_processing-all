'''
'''
import sys
import pytz
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date,timezone
from astroplan import Observer, FixedTarget
import astropy.units as u
from astropy.time import Time, TimeDelta
from astropy.coordinates import EarthLocation, AltAz
from astropy.visualization import astropy_mpl_style
from geopy.geocoders import Nominatim

################################################################################

def culmination_time():
    '''
    '''
    loc_name = "Volokhiv Yar"
    loc_tzname = 'Europe/Kiev'
    loc_tz = pytz.timezone(loc_tzname)
    star_name = "Polaris"
    first_year = 2010
    day_of_year = "08-07"
    num_years = 20

    geolocator = Nominatim(user_agent='SunPosition Python Script V00.00')
    loc = geolocator.geocode(loc_name)
    print('\n Loc = ', loc, '\n')
    coords = EarthLocation.from_geodetic(lat=loc.latitude*u.deg, lon=loc.longitude*u.deg)
    print(' Coords = ', coords)

    observer = Observer(location = coords, name='Volokhiv Yar', timezone=loc_tzname)

    target = FixedTarget.from_name(star_name)

    years = range(first_year, first_year + num_years)
    string_dates = [ f'{y}-{day_of_year} 00:00:00.000' for y in years]
    dates = [ Time(d,scale='utc') for d in string_dates ]

    culminations = [ observer.target_meridian_transit_time(t,target,which='next') for t in dates ]
    times = [ t.to_datetime(timezone=loc_tz).time() for t in culminations ]
    data = pd.DataFrame(data={'year':years,'time':times})

    print(data)
    plt.plot(data.year,data.time)
    plt.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
    #plt.set_xlim([2010, 2020])
    plt.show()

    return

################################################################################
################################################################################

if __name__ == '__main__':


    culmination_time()
