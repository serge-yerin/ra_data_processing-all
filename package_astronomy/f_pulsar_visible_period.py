import numpy as np
from astropy.time import Time
from PyAstronomy import pyasl
from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_common_modules.text_manipulations import find_between


def preparations():
    # earth_radius = 6371.0
    # lon_utr2 = 2.46273  # 36.941  # 36 56 27.56 E
    # lat_utr2 = 49.6362  # / !RADEG    # 49 38 10.31 N

    epoch_obs = 2000

    pulsar_name = 'B0809+74'

    pulsar_ra, pulsar_dec, pulsar_DM, p_bar = catalogue_pulsar(pulsar_name)

    print(pulsar_ra, pulsar_dec, pulsar_DM, p_bar)

    def right_ascension_to_deg(pulsar_ra):
        hour = int(pulsar_ra[0:2])
        mins = int(pulsar_ra[3:5])
        secs = float(find_between(pulsar_ra, 'm', 's'))
        ra_deg = (hour + mins/60. + secs/3600.) * 15
        return ra_deg

    def declination_to_deg(pulsar_dec):
        degs = int(pulsar_dec[0:3])
        mins = int(pulsar_dec[4:6])
        secs = float(find_between(pulsar_dec, 'm', 's'))
        dec_deg = (degs + mins/60. + secs/3600.)
        return dec_deg

    ra_deg = right_ascension_to_deg(pulsar_ra)
    dec_deg = declination_to_deg(pulsar_dec)

    obs_time = '2022-04-13 12:16:07.915231'

    p_visible = pulsar_visible_period(obs_time, ra_deg, dec_deg, p_bar)

    print(' Right ascension:        ', ra_deg)
    print(' Declination:            ', dec_deg)
    print(' Observation time:       ', obs_time)
    print(' Observation time (Jul): ', Time([obs_time], scale='utc')[0].mjd)
    print(' Barycentric period:     ', p_bar)
    print(' Visible period:         ', p_visible)
    return


def pulsar_visible_period(obs_time, ra, dec_deg, p_bar):

    t = Time([obs_time], scale='utc')
    jd = np.float64(t.mjd)

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

    c = np.float64(299792.458)

    # Project velocity toward star:
    v = np.float64(vb[0] * np.cos(dec_deg) * np.cos(ra) + vb[1] * np.cos(dec_deg) * np.sin(ra) + vb[2] * np.sin(dec_deg))
    p_visible = np.float64(p_bar * ((1 - v/c) / (1 + v/c)) ** 0.5)  # Visible period
    return p_visible


preparations()
