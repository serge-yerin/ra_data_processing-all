import numpy as np
from astropy.time import Time
from PyAstronomy import pyasl
from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_common_modules.text_manipulations import find_between


def right_ascension_to_deg(pulsar_ra):
    hour = int(pulsar_ra[0:2])
    mins = int(pulsar_ra[3:5])
    secs = float(find_between(pulsar_ra, 'm', 's'))
    ra_deg = (hour + mins / 60. + secs / 3600.) * 15
    return ra_deg


def declination_to_deg(pulsar_dec):
    degs = int(pulsar_dec[0:3])
    mins = int(pulsar_dec[4:6])
    secs = float(find_between(pulsar_dec, 'm', 's'))
    dec_deg = (degs + mins / 60. + secs / 3600.)
    return dec_deg


def pulsar_visible_period(pulsar_name, obs_time, print_or_not=False):
    """
    Calculates pulsar visible period from baricentric period and observation epoch (date and time)
    Inputs:
        pulsar_name - (string) pulsar name to check in pulsar catalogue from this repo
        obs_time - (string) observation time UTC to convert to Julian days (ex. '2020-01-01 00:00:00.000000')
        print_or_not - (bool optional) to print the initial data and results to console or not
    Outputs:
        p_visible - (np.float64) visible pulsar period
        jd - (np.float64) Julian day calculated from the observations day and time
    """

    # Take pulsar coordinates and baricentric period from catalogue
    pulsar_ra, pulsar_dec, pulsar_dm, p_bar = catalogue_pulsar(pulsar_name, epoch_obs='2020-01-01 00:00:00.000000')

    # Convert from hh:mm:ss or deg:min:sec catalogue values to degrees
    ra_deg = right_ascension_to_deg(pulsar_ra)
    dec_deg = declination_to_deg(pulsar_dec)

    # convert degrees to radians to calculate sin and cos correctly
    ra_rad = ra_deg * np.pi / 180
    dec_rad = dec_deg * np.pi / 180

    t = Time([obs_time], scale='utc')
    jd = np.float64(t.jd)

    vh, vb = pyasl.baryvel(jd, 2000)
    '''
    # https://pyastronomy.readthedocs.io/en/latest/pyaslDoc/aslDoc/baryvel.html
    Parameters:
        djefloat - Julian ephemeris date
        deqfloat - Epoch of mean equinox of helio- and barycentric velocity output. 
                    If deq is zero, deq is assumed to be equal to dje.
    Returns:
        dvelharray - Heliocentric velocity vector [km/s].
        dvelbarray - Barycentric velocity vector [km/s].
    '''

    c = np.float64(299792.458)  # Speed of light

    # Project velocity toward star:
    v = np.float64(vb[0] * np.cos(dec_rad) * np.cos(ra_rad) +
                   vb[1] * np.cos(dec_rad) * np.sin(ra_rad) +
                   vb[2] * np.sin(dec_rad))

    # Visible pulsar period:
    p_visible = np.float64(p_bar * ((1 - v / c) / (1 + v / c)) ** 0.5)

    if print_or_not:
        print(' Calculating visible period of pulsar... \n')
        print(' Pulsar name:                        ', pulsar_name)
        print(' Dispersion measure:                 ', pulsar_dm, ' pc * cm^-3 ')
        print(' Catalogue coordinates:              ', pulsar_ra, '  ', pulsar_dec)
        print(' Right ascension:                    ', ra_deg, ' deg or', ra_rad, ' rad')
        print(' Declination:                        ', dec_deg, ' deg or', dec_rad, ' rad')
        print(' Observation time:                   ', obs_time)
        print(' Observation time (Jul):             ', Time([obs_time], scale='utc')[0].jd)
        print(' Heliocentric velocity vector [km/s]:', vh)
        print(' Barycentric velocity vector [km/s]: ', vb)
        print(' Barycentric period:                 ', p_bar, 's.')
        print(' Visible period:                     ', p_visible, 's. \n')

    return p_visible, jd


if __name__ == '__main__':

    pulsar_name = 'B0809+74'
    obs_time = '2022-04-13 12:16:07.915231'

    p_vis, jul_day = pulsar_visible_period(pulsar_name, obs_time, print_or_not=True)
    print('\n\n Result period and epoch in jd:', p_vis, jul_day)
