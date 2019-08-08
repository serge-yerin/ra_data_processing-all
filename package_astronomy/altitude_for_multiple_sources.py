'''
'''
import time
import pylab
import numpy as np
import astropy.units as u
from astropy.coordinates import EarthLocation, AltAz
from pytz import timezone
from astroplan import Observer
from astropy.coordinates import SkyCoord
from astroplan import FixedTarget
from astroplan import Observer
from astropy.time import Time
from astroplan.plots import plot_sky
from astroplan.plots import plot_altitude
import matplotlib.pyplot as plt
from matplotlib import ticker as mtick
from matplotlib import rc

################################################################################

def astroplan_test(start_time, end_time):
    '''
    '''

    currentDate = time.strftime("%Y-%m-%d")
    currentTime = time.strftime("%H:%M:%S")
    print ('\n  Today is ', currentDate, ', local time is ', currentTime, '\n')

    time_window = start_time + (end_time - start_time) * np.linspace(0, 1, 145)

    # Coordinates of UTR-2 radio telescope
    longitude = '36d56m29.000s'
    latitude = '+49d38m10.000s'
    elevation = 156 * u.m
    utr2_location = EarthLocation.from_geodetic(longitude, latitude, elevation)

    observer = Observer(name='UTR-2 radio telescope',
               location=utr2_location,
               timezone=timezone('Europe/Kiev'),
               description="UTR-2 radio telescope (Volokhiv Yar village, Kharkiv region, Ukraine)")

    print('  Observer:', observer.name)


    # Coordinates of celestial body
    coordinates = SkyCoord('20h41m25.9s', '+45d16m49.3s', frame='icrs')
    deneb = FixedTarget(name = 'Deneb', coord = coordinates)

    frame = AltAz(obstime=time_window, location=utr2_location)
    altazs = coordinates.transform_to(frame)


    from astropy.coordinates import get_sun
    frame = AltAz(obstime=time_window, location=utr2_location)
    sun_alt_az = get_sun(time_window).transform_to(frame)

    from astropy.coordinates import get_jupiter


    ticks_list = [0, 24, 48, 72, 96, 120, 144]
    time_ticks_list = []
    for i in range(len(ticks_list)):
        time_ticks_list.append(str(time_window[ticks_list[i]])[10:19])

    rc('font', size = 10, weight='bold')
    fig = plt.figure(figsize = (9, 5))
    ax1 = fig.add_subplot(111)
    #j = np.linspace(0, 145, 145)
    #ax1.scatter(j, altazs.alt, c=altazs.az, label='Deneb', lw=0, s=8, cmap='viridis')
    ax1.plot(altazs.alt, label='Deneb')
    ax1.plot(sun_alt_az.alt, label='Sun')
    plt.fill_between(np.linspace(0, 145, 145), 0, 10, color='0.6')
    plt.fill_between(np.linspace(0, 145, 145), 10, 20, color='0.7')
    plt.fill_between(np.linspace(0, 145, 145), 20, 30, color='0.8')
    plt.fill_between(np.linspace(0, 145, 145), -10, 0, color='0.3')
    ax1.set_xlim([0, 144])
    ax1.set_ylim([-10, 90])
    ax1.xaxis.set_major_locator(mtick.LinearLocator(7))
    ax1.xaxis.set_minor_locator(mtick.LinearLocator(13))
    plt.xticks(ticks_list, time_ticks_list)
    plt.yticks([-10,0,10,20,30,40,50,60,70,80,90])
    ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
    ax1.legend(loc='center right', fontsize = 10, bbox_to_anchor=(1.2, 0.5))
    plt.ylabel('Altitude above horizon, deg', fontsize = 10, fontweight='bold')
    plt.xlabel('UTC time', fontsize = 10, fontweight='bold')
    pylab.savefig('multiple sources.png', bbox_inches='tight', dpi = 300)
    #plt.show()


    #utr2 = Observer.at_site(observer)

    #obs_time = Time(currentDate +' '+ currentTime)   # Pay attention, not UTC, local time!
    '''
    print(' At', start_time, ' Night is: ', observer.is_night(start_time))
    print(' Is Deneb on the sky: ', observer.target_is_up(start_time, deneb))


    sunset_tonight = observer.sun_set_time(start_time, which='nearest')
    sunrise_tonight = observer.sun_rise_time(end_time, which='nearest')

    print(' Sunset:', sunset_tonight.iso, ' Sunrise: ', sunrise_tonight.iso)


    # Plotting
    deneb_rise = observer.target_rise_time(start_time, deneb) + 5*u.minute
    deneb_set = observer.target_set_time(end_time, deneb) - 5*u.minute
    print(' Deneb is up from ',deneb_rise,'till',deneb_set)







    from astropy.coordinates import get_sun
    #delta_midnight = np.linspace(0, 24, 100)*u.hour
    #times_July12_to_13 = start_time + np.linspace(0, 24, 100)*u.hour
    frame = AltAz(obstime=time_window, location=utr2_location)
    sun_alt_az = get_sun(time_window).transform_to(frame)

    #plt.plot(delta_midnight, sunaltazs_July12_to_13.alt, color='r', label='Sun')
    #plt.show()

    #deneb_style = {'color': 'r'}

    plot_sky(deneb, observer, time_window) # style_kwargs=deneb_style
    plt.legend(loc='center left', bbox_to_anchor=(1.25, 0.5))
    plt.show()


    plot_altitude(deneb, observer, time_window)
    plot_altitude(sun_alt_az, observer, time_window)
    plt.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
    plt.show()
    '''
    return

################################################################################
################################################################################

if __name__ == '__main__':

    start_time = Time('2019-08-07 00:00:00')
    end_time = Time('2019-08-08 00:00:00')

    astroplan_test(start_time, end_time)
