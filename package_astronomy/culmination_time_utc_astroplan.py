
from astroplan import Observer, FixedTarget
import astropy.units as u
from astropy.time import Time, TimeDelta
from astropy.coordinates import EarthLocation, AltAz
from astropy.coordinates import SkyCoord

from package_astronomy.catalogue_sources import catalogue_sources


################################################################################

def culmination_time_utc_astroplan(source_name, date, print_or_not, culm_type='next'):
    """
    Calculates culmination time in UTC with astroplan library
    """
    # Coordinates of UTR-2 radio telescope
    longitude = '36d56m27.560s'
    latitude = '+49d38m10.310s'
    elevation = 156 * u.m
    observatory = 'UTR-2, Ukraine'
    utr2_location = EarthLocation.from_geodetic(longitude, latitude, elevation)

    if print_or_not == 1:
        print('\n  Observatory:', observatory, '\n')
        print('  Coordinates: \n  * Longitude: ',
              str(utr2_location.lon).replace("d", "\u00b0 ").replace("m", "\' ").replace("s", "\'\' "),
              ' \n  * Latitude:   ' + str(utr2_location.lat).replace("d", "\u00b0 ").replace("m", "\' ").replace("s", "\'\' ") + '\n')
        print('  Source:', source_name, '\n')

    observer = Observer(location=utr2_location, name='Volokhiv Yar', timezone='UTC')

    alt, az = catalogue_sources(source_name)
    coordinates = SkyCoord(alt, az, frame='icrs')

    target = FixedTarget(coord=coordinates, name="target")
    date_of_obs = Time(date, scale='utc')
    culmination = observer.target_meridian_transit_time(date_of_obs, target, which=culm_type)  # next, 'previous'
    culm_time = culmination.to_datetime().time()

    culm_time = date[0:10] + ' ' + str(culm_time)[0:8]

    if print_or_not == 1:
        print('  Culmination time:', culm_time, ' UTC \n')

    return culm_time


################################################################################


if __name__ == '__main__':

    date = '2019-10-05'
    source = '3C461'
    culmination_time_utc_astroplan(source, date, 1)
