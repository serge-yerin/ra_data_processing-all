'''
'''
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz

################################################################################

def altitude_azimuth_for_sources():
    '''
    '''
    m33 = SkyCoord.from_name('M33')
    bear_mountain = EarthLocation(lat=41.3*u.deg, lon=-74*u.deg, height=390*u.m)
    utcoffset = -4*u.hour  # Eastern Daylight Time
    time = Time('2012-7-12 23:00:00') - utcoffset
    m33altaz = m33.transform_to(AltAz(obstime=time,location=bear_mountain))
    print("M33's Altitude = {0.alt:.2}".format(m33altaz))

    midnight = Time('2012-7-13 00:00:00') - utcoffset
    delta_midnight = np.linspace(-2, 10, 100)*u.hour
    frame_July13night = AltAz(obstime=midnight+delta_midnight, location=bear_mountain)
    m33altazs_July13night = m33.transform_to(frame_July13night)

    m33airmasss_July13night = m33altazs_July13night.secz

    plt.plot(delta_midnight, m33airmasss_July13night)
    plt.xlim(-2, 10)
    plt.ylim(1, 4)
    plt.xlabel('Hours from EDT Midnight')
    plt.ylabel('Airmass [Sec(z)]')
    plt.show()

    from astropy.coordinates import get_sun
    delta_midnight = np.linspace(-12, 12, 1000)*u.hour
    times_July12_to_13 = midnight + delta_midnight
    frame_July12_to_13 = AltAz(obstime=times_July12_to_13, location=bear_mountain)
    sunaltazs_July12_to_13 = get_sun(times_July12_to_13).transform_to(frame_July12_to_13)


    from astropy.coordinates import get_moon
    moon_July12_to_13 = get_moon(times_July12_to_13)
    moonaltazs_July12_to_13 = moon_July12_to_13.transform_to(frame_July12_to_13)

    m33altazs_July12_to_13 = m33.transform_to(frame_July12_to_13)

    plt.plot(delta_midnight, sunaltazs_July12_to_13.alt, color='r', label='Sun')
    plt.plot(delta_midnight, moonaltazs_July12_to_13.alt, color=[0.75]*3, ls='--', label='Moon')
    plt.scatter(delta_midnight, m33altazs_July12_to_13.alt,
            c=m33altazs_July12_to_13.az, label='M33', lw=0, s=8,
            cmap='viridis')
    plt.fill_between(delta_midnight.to('hr').value, 0, 90,
                 sunaltazs_July12_to_13.alt < -0*u.deg, color='0.5', zorder=0)
    plt.fill_between(delta_midnight.to('hr').value, 0, 90,
                 sunaltazs_July12_to_13.alt < -18*u.deg, color='k', zorder=0)
    plt.colorbar().set_label('Azimuth [deg]')
    plt.legend(loc='upper left')
    plt.xlim(-12, 12)
    plt.xticks(np.arange(13)*2 -12)
    plt.ylim(0, 90)
    plt.xlabel('Hours from EDT Midnight')
    plt.ylabel('Altitude [deg]')
    plt.show()

    return

################################################################################
################################################################################

if __name__ == '__main__':


    altitude_azimuth_for_sources()
