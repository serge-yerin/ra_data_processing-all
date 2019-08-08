Software_version = '2019.09.08'
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

from catalogue_pulsar import catalogue_pulsar
from catalogue_sources import catalogue_sources
from find_max_altitude import find_max_altitude
################################################################################

def astroplan_test(start_time, end_time, pulsar_list, sources_list):
    '''
    '''

    currentDate = time.strftime("%Y-%m-%d")
    currentTime = time.strftime("%H:%M:%S")
    print ('\n  Today is ', currentDate, ', local time is ', currentTime, '\n')

    time_window = start_time + (end_time - start_time) * np.linspace(0, 1, 145)

    # Coordinates of UTR-2 radio telescope
    # longUTR= 2.46273 ;36.941  ;36 56 27.56 E
    # latUTR= 49.6362/!RADEG  ;49 38 10.31 N
    longitude = '36d56m27.560s'
    latitude = '+49d38m10.310s'
    elevation = 156 * u.m
    utr2_location = EarthLocation.from_geodetic(longitude, latitude, elevation)

    observer = Observer(name='UTR-2 radio telescope',
               location=utr2_location,
               timezone=timezone('Europe/Kiev'),
               description="UTR-2 radio telescope (Volokhiv Yar village, Kharkiv region, Ukraine)")

    print('  Observer:', observer.name)

    frame = AltAz(obstime = time_window, location = utr2_location)

    # Coordinates of Deneb
    deneb_coordinates = SkyCoord('20h41m25.9s', '+45d16m49.3s', frame='icrs')
    #deneb = FixedTarget(name = 'Deneb', coord = deneb_coordinates)
    deneb_alt_az = deneb_coordinates.transform_to(frame)

    # Coordiantes of Sun
    from astropy.coordinates import get_sun
    sun_alt_az = get_sun(time_window).transform_to(frame)

    # Coordinates of pulsar
    pulsar_alt_az = []
    for i in range (len(pulsar_list)):
        alt, az, DM = catalogue_pulsar(pulsar_list[i])
        coordinates = SkyCoord(alt, az, frame='icrs')
        pulsar_alt_az.append(coordinates.transform_to(frame))

    # Coordinates of sources
    sources_alt_az = []
    for i in range (len(sources_list)):
        alt, az = catalogue_sources(sources_list[i])
        coordinates = SkyCoord(alt, az, frame='icrs')
        sources_alt_az.append(coordinates.transform_to(frame))


    ticks_list = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144]
    time_ticks_list = []
    for i in range(len(ticks_list)):
        time_ticks_list.append(str(time_window[ticks_list[i]])[10:16])
    color = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']

    rc('font', size = 6, weight='bold')
    fig = plt.figure(figsize = (9, 6))
    ax1 = fig.add_subplot(111)

    #j = np.linspace(0, 145, 145)
    #ax1.scatter(j, altazs.alt, c=altazs.az, label='Deneb', lw=0, s=8, cmap='viridis')
    #ax1.plot(deneb_alt_az.alt, label='Deneb')

    # Culmination lines plots
    xmax, ymax = find_max_altitude(sun_alt_az) # Sun
    plt.axvline(x=xmax, linewidth = '0.8' , color = 'C1', alpha=0.5)
    for i in range (len(pulsar_list)):
        xmax, ymax = find_max_altitude(pulsar_alt_az[i]) # Pulsars
        plt.axvline(x=xmax, linewidth = '0.8' , color = color[i], alpha=0.5)
    for i in range (len(sources_list)):
        xmax, ymax = find_max_altitude(sources_alt_az[i]) # Sources
        plt.axvline(x=xmax, linewidth = '0.8' , color = color[i], alpha=0.5)

    ax1.plot(sun_alt_az.alt, label='Sun', linewidth = '2.5', color = 'C1')
    xmax, ymax = find_max_altitude(sun_alt_az)
    ax1.annotate('Sun', xy=(xmax+1, ymax+1), color = 'C1', fontsize = 6, rotation=45)  #xytext=(xmax, ymax)
    ax1.plot(xmax, ymax, marker='o', markersize=4, color="red")
    del xmax, ymax

    # Pulsars
    for i in range (len(pulsar_list)):
        ax1.plot(pulsar_alt_az[i].alt, label=pulsar_list[i], color = color[i], linestyle = '--', linewidth = '0.8')
        xmax, ymax = find_max_altitude(pulsar_alt_az[i])
        ax1.annotate(pulsar_list[i], xy=(xmax+1, ymax+1), color = color[i], fontsize = 6, rotation=45) #ha='center'
        ax1.plot(xmax, ymax, marker='o', markersize = 3, color = color[i])

        del xmax, ymax

    # Sources
    for i in range (len(sources_list)):
        ax1.plot(sources_alt_az[i].alt, label=sources_list[i], color = color[i], linestyle = '-', linewidth = '0.7')
        xmax, ymax = find_max_altitude(sources_alt_az[i])
        ax1.annotate(sources_list[i], xy=(xmax+1, ymax+1), color = color[i], fontsize = 6, rotation=45)
        ax1.plot(xmax, ymax, marker='o', markersize = 3, color = color[i])
        del xmax, ymax

    plt.fill_between(np.linspace(0, 145, 145), 0, 10, color='0.7')
    plt.fill_between(np.linspace(0, 145, 145), 10, 20, color='0.8')
    plt.fill_between(np.linspace(0, 145, 145), 20, 30, color='0.9')
    plt.fill_between(np.linspace(0, 145, 145), -10, 0, color='0.4')
    ax1.set_xlim([0, 144])
    ax1.set_ylim([-10, 95])
    ax1.xaxis.set_major_locator(mtick.LinearLocator(15))
    ax1.xaxis.set_minor_locator(mtick.LinearLocator(25))
    plt.xticks(ticks_list, time_ticks_list)
    plt.yticks([-10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
    ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-', linewidth = '0.5')
    fig.suptitle('Elevation above horizon of sources for ' + observer.name, fontsize = 8, fontweight='bold')
    ax1.set_title('Time period: '+ str(start_time)[0:19] + ' - ' + str(end_time)[0:19], fontsize = 7)
    fig.subplots_adjust(top=0.9)
    #ax1.legend(loc='center right', fontsize = 8, bbox_to_anchor=(1.17, 0.5))
    plt.ylabel('Altitude above horizon, deg', fontsize = 8, fontweight='bold')
    plt.xlabel('UTC time', fontsize = 8, fontweight='bold')
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(ax1.get_xticks())
    ax2.set_xticklabels(ax1.get_xticklabels())

    fig.text(0.79, 0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
    fig.text(0.11, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)

    pylab.savefig('multiple sources.png', bbox_inches='tight', dpi = 300)
    #plt.show()

    return

################################################################################
################################################################################

if __name__ == '__main__':

    start_time = Time('2019-08-07 12:00:00')
    end_time = Time('2019-08-08 12:00:00')
    pulsar_list = [] #['B0329+54', 'B0031-07', 'B0320+39', 'B0450+55']
    sources_list = ['Cas A', 'Syg A', 'Crab']

    astroplan_test(start_time, end_time, pulsar_list, sources_list)
