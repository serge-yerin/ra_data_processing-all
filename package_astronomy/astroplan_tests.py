'''
'''
import time
import numpy as np
import astropy.units as u
from astropy.coordinates import EarthLocation
from pytz import timezone
from astroplan import Observer
from astropy.coordinates import SkyCoord
from astroplan import FixedTarget
from astroplan import Observer
from astropy.time import Time
from astroplan.plots import plot_sky
from astroplan.plots import plot_altitude
import matplotlib.pyplot as plt

################################################################################

def astroplan_test():
    '''
    '''

    currentDate = time.strftime("%Y-%m-%d")
    currentTime = time.strftime("%H:%M:%S")
    print ('\n  Today is ', currentDate, ' time is ', currentTime, '\n')

    longitude = '36d56m29.000s'
    latitude = '+49d38m10.000s'
    elevation = 156 * u.m
    location = EarthLocation.from_geodetic(longitude, latitude, elevation)

    observer = Observer(name='UTR-2 radio telescope',
               location=location,
               pressure=0.615 * u.bar,
               relative_humidity=0.11,
               temperature=0 * u.deg_C,
               timezone=timezone('Europe/Kiev'),
               description="UTR-2 radio telescope, Volokhiv Yar village Kharkiv region Ukraine")

    print(' Observer:', observer.name)

    coordinates = SkyCoord('20h41m25.9s', '+45d16m49.3s', frame='icrs')
    deneb = FixedTarget(name = 'Deneb', coord = coordinates)

    obs_time = Time('2019-08-06 23:00:00')

    #utr2 = Observer.at_site(observer)

    #obs_time = Time(currentDate +' '+ currentTime)   # Pay attention, not UTC, local time!

    print(' At', obs_time, ' Night is: ', observer.is_night(obs_time))
    print(' Is Deneb on the sky: ', observer.target_is_up(obs_time, deneb))


    sunset_tonight = observer.sun_set_time(obs_time, which='nearest')
    sunrise_tonight = observer.sun_rise_time(obs_time, which='nearest')

    print(' Sunset:', sunset_tonight.iso, ' Sunrise: ', sunrise_tonight.iso)


    # Plotting
    deneb_rise = observer.target_rise_time(obs_time, deneb) + 5*u.minute
    deneb_set = observer.target_set_time(obs_time, deneb) - 5*u.minute
    print(' Deneb is up from ',deneb_rise,'till',deneb_set)


    deneb_style = {'color': 'r'}

    '''
    start = Time('2019-08-06 12:00:00')
    end = Time('2019-08-07 12:00:00')

    time_window = start + (end - start) * np.linspace(0, 1, 20)

    plot_sky(deneb, observer, time_window, style_kwargs=deneb_style)
    plt.legend(loc='center left', bbox_to_anchor=(1.25, 0.5))
    plt.show()
    '''


    start_time = Time('2019-08-06 18:00:00')
    end_time = Time('2019-08-07 09:00:00')
    delta_t = end_time - start_time
    observe_time = start_time + delta_t*np.linspace(0, 1, 75)
    plot_altitude(deneb, observer, observe_time)

    plt.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
    plt.show()

    return

################################################################################
################################################################################

if __name__ == '__main__':


    astroplan_test()
