'''
'''
import numpy as np
import astropy.units as u
from astropy.time import Time, TimeDelta
from astropy.coordinates import EarthLocation, AltAz
from astropy.coordinates import SkyCoord
from astropy.coordinates import get_sun
from astropy.coordinates import get_body
from astropy.coordinates import solar_system_ephemeris

from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_astronomy.catalogue_sources import catalogue_sources
from package_astronomy.find_max_altitude import find_max_altitude


################################################################################

def culmination_time_utc(source_name, date, print_or_not):
    '''
    '''

    # Coordinates of UTR-2 radio telescope
    longitude = '36d56m27.560s'
    latitude = '+49d38m10.310s'
    elevation = 156 * u.m
    observatory = 'UTR-2, Ukraine'
    utr2_location = EarthLocation.from_geodetic(longitude, latitude, elevation)

    start_time = Time(date + ' 00:00:00')
    end_time = Time(date + ' 23:59:59')
    time_line = time_window = start_time + (end_time - start_time) * np.linspace(0, 1, 86400)
    frame = AltAz(obstime = time_window, location = utr2_location)

    if print_or_not == 1: print('\n  Observatory:', observatory, '\n')
    if print_or_not == 1: print('  Coordinates: \n  * Longitude: ', str(utr2_location.lon).replace("d", "\u00b0 " ).replace("m", "\' " ).replace("s", "\'\' " ),' \n  * Latitude:   '+ str(utr2_location.lat).replace("d", "\u00b0 " ).replace("m", "\' " ).replace("s", "\'\' " ) + '\n')
    if print_or_not == 1: print('  Source:', source_name, '\n')


    if source_name.lower() == 'sun':
        source_alt_az = get_sun(time_window).transform_to(frame)
    elif source_name.lower() == 'jupiter':
        with solar_system_ephemeris.set('builtin'):
            source_alt_az = get_body('jupiter', time_window, utr2_location).transform_to(frame)
    elif source_name.startswith('B') or source_name.startswith('J'):
        alt, az, DM = catalogue_pulsar(source_name)
        coordinates = SkyCoord(alt, az, frame='icrs')
        source_alt_az = coordinates.transform_to(frame)
    elif source_name.startswith('3C') or source_name.startswith('4C'):
        alt, az = catalogue_sources(source_name)
        coordinates = SkyCoord(alt, az, frame='icrs')
        source_alt_az = coordinates.transform_to(frame)
    else:
        print ('Source not found!')

    xmax, ymax = find_max_altitude(source_alt_az)

    culm_time = str(time_line[int(xmax)])[0:19]

    if print_or_not == 1: print('  Culmination time:', culm_time, ' UTC \n')

    return culm_time

################################################################################
################################################################################

if __name__ == '__main__':

    date = '2019-10-05'
    source_name = '3C461'

    culm_time = culmination_time_utc(source_name, date, 1)
