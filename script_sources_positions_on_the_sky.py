Software_version = '2019.09.08'
'''
'''
import os
import time
import pylab
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker as mtick
from matplotlib import rc
from pytz import timezone
import astropy.units as u
from astropy.coordinates import EarthLocation, AltAz
from astropy.coordinates import SkyCoord
from astropy.coordinates import solar_system_ephemeris
from astropy.coordinates import get_body_barycentric
from astropy.coordinates import get_body
from astropy.coordinates import get_sun
from astropy.time import Time

from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_astronomy.catalogue_sources import catalogue_sources
from package_astronomy.find_max_altitude import find_max_altitude
from package_astronomy.find_rize_and_set_points import find_rize_and_set_points
################################################################################

def sources_positions_on_the_sky(start_time, end_time, pulsars_list, sources_list):
    '''
    '''

    currentDate = time.strftime("%Y-%m-%d")
    currentTime = time.strftime("%H:%M:%S")
    print ('\n  Today is ', currentDate, ', local time is ', currentTime, '\n')

    newpath = "Sources_positions"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    n_points = 1441 # Number of points to calculate within the time window
    center = int(n_points/2) + 1
    time_window = start_time + (end_time - start_time) * np.linspace(0, 1, n_points)

    # Coordinates of UTR-2 radio telescope
    longitude = '36d56m27.560s'
    latitude = '+49d38m10.310s'
    elevation = 156 * u.m
    observatory = 'UTR-2, Ukraine'
    utr2_location = EarthLocation.from_geodetic(longitude, latitude, elevation)

    print('  Observatory:', observatory, '\n')
    print('  Coordinates: \n  * Longitude: ', str(utr2_location.lon).replace("d", "\u00b0 " ).replace("m", "\' " ).replace("s", "\'\' " ),' \n  * Latitude:   '+ str(utr2_location.lat).replace("d", "\u00b0 " ).replace("m", "\' " ).replace("s", "\'\' " ) + '\n')
    print('  Plot time window: \n  * From: ', str(start_time)[0:19],' UTC \n  * Till:  '+ str(end_time)[0:19] + '  UTC \n')

    frame = AltAz(obstime = time_window, location = utr2_location)

    # Coordiantes of Sun
    sun_alt_az = get_sun(time_window).transform_to(frame)

    # Coordinates of Jupiter
    with solar_system_ephemeris.set('builtin'):
        jupiter_alt_az = get_body('jupiter', time_window, utr2_location).transform_to(frame)

    # Coordinates of pulsars
    pulsars_alt_az = []
    for i in range (len(pulsars_list)):
        alt, az, DM = catalogue_pulsar(pulsars_list[i])
        coordinates = SkyCoord(alt, az, frame='icrs')
        pulsars_alt_az.append(coordinates.transform_to(frame))

    # Coordinates of sources
    sources_alt_az = []
    for i in range (len(sources_list)):
        alt, az = catalogue_sources(sources_list[i])
        coordinates = SkyCoord(alt, az, frame='icrs')
        sources_alt_az.append(coordinates.transform_to(frame))


    ticks_list = [0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440]
    time_ticks_list = []
    for i in range(len(ticks_list)):
        time_ticks_list.append(str(time_window[ticks_list[i]])[10:16])
    color = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']


    # *** Sources elevation above horizon with time plot figure ***
    rc('font', size = 6, weight='bold')
    fig = plt.figure(figsize = (9, 6))
    ax1 = fig.add_subplot(111)

    xmax, ymax = find_max_altitude(sun_alt_az) # Sun
    plt.axvline(x=xmax, linewidth = '0.8' , color = 'C1', alpha=0.5)
    xmax, ymax = find_max_altitude(jupiter_alt_az) # Sun
    plt.axvline(x=xmax, linewidth = '0.8' , color = 'C4', alpha=0.5)
    for i in range (len(pulsars_list)):
        xmax, ymax = find_max_altitude(pulsars_alt_az[i]) # Pulsars
        plt.axvline(x=xmax, linewidth = '0.8' , color = color[i], alpha=0.5)
    for i in range (len(sources_list)):
        xmax, ymax = find_max_altitude(sources_alt_az[i]) # Sources
        plt.axvline(x=xmax, linewidth = '0.8' , color = color[i], alpha=0.5)

    # Sun
    ax1.plot(sun_alt_az.alt, label='Sun', linewidth = '2.5', color = 'C1')
    xmax, ymax = find_max_altitude(sun_alt_az)
    ax1.annotate('Sun', xy=(xmax+1, ymax+1), color = 'C1', fontsize = 6, rotation=45)  #xytext=(xmax, ymax)
    ax1.plot(xmax, ymax, marker='o', markersize=4, color="red")
    del xmax, ymax

    # Jupiter
    ax1.plot(jupiter_alt_az.alt, label='Jupiter', linewidth = '2.5', color = 'C4')
    xmax, ymax = find_max_altitude(jupiter_alt_az)
    ax1.annotate('Jupiter', xy=(xmax+1, ymax+1), color = 'C4', fontsize = 6, rotation=45)  #xytext=(xmax, ymax)
    ax1.plot(xmax, ymax, marker='o', markersize=4, color="red")
    del xmax, ymax

    # Pulsars
    for i in range (len(pulsars_list)):
        ax1.plot(pulsars_alt_az[i].alt, label=pulsars_list[i], color = color[i], linestyle = '--', linewidth = '0.8')
        xmax, ymax = find_max_altitude(pulsars_alt_az[i])
        ax1.annotate(pulsars_list[i], xy=(xmax+1, ymax+1), color = color[i], fontsize = 6, rotation=45) #ha='center'
        ax1.plot(xmax, ymax, marker='o', markersize = 3, color = color[i])
        del xmax, ymax

    # Sources
    for i in range (len(sources_list)):
        ax1.plot(sources_alt_az[i].alt, label=sources_list[i], color = color[i], linestyle = '-', linewidth = '0.7')
        xmax, ymax = find_max_altitude(sources_alt_az[i])
        ax1.annotate(sources_list[i], xy=(xmax+1, ymax+1), color = color[i], fontsize = 6, rotation=45)
        ax1.plot(xmax, ymax, marker='o', markersize = 3, color = color[i])
        del xmax, ymax

    plt.fill_between(np.linspace(0, n_points, n_points), 0, 10, color='0.7')
    plt.fill_between(np.linspace(0, n_points, n_points), 10, 20, color='0.8')
    plt.fill_between(np.linspace(0, n_points, n_points), 20, 30, color='0.9')
    plt.fill_between(np.linspace(0, n_points, n_points), -10, 0, color='0.4')
    ax1.set_xlim([0, n_points-1])
    ax1.set_ylim([-10, 95])
    ax1.xaxis.set_major_locator(mtick.LinearLocator(15))
    ax1.xaxis.set_minor_locator(mtick.LinearLocator(25))
    plt.xticks(ticks_list, time_ticks_list)
    plt.yticks([-10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
    ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-', linewidth = '0.5')
    fig.suptitle('Elevation above horizon of sources for ' + observatory, fontsize = 8, fontweight='bold')
    ax1.set_title('Time period: '+ str(start_time)[0:19] + ' - ' + str(end_time)[0:19], fontsize = 7)
    fig.subplots_adjust(top=0.9)
    #ax1.legend(loc='center right', fontsize = 8, bbox_to_anchor=(1.17, 0.5))
    plt.ylabel('Altitude above horizon, deg', fontsize = 8, fontweight='bold')
    plt.xlabel('UTC time', fontsize = 8, fontweight='bold')
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(ax1.get_xticks())
    ax2.set_xticklabels(ax1.get_xticklabels())
    fig.text(0.79, 0.04, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
    fig.text(0.11, 0.04, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
    pylab.savefig(newpath + '/'+ str(start_time)[0:10] + ' sources elevation.png', bbox_inches='tight', dpi = 300)
    #plt.show()


    # Preparing data for correct sky plot (Altitutde / Azimuth)
    # Sun
    r_sun = np.zeros(len(sun_alt_az))
    r_sun[:] = sun_alt_az[:].alt.degree
    r_sun[r_sun < 0] = 0
    r_sun[:] = (90 - r_sun[:])
    r_sun[r_sun > 89] = np.inf

    # Jupiter
    r_jupiter = np.zeros(len(jupiter_alt_az))
    r_jupiter[:] = jupiter_alt_az[:].alt.degree
    r_jupiter[r_jupiter < 0] = 0
    r_jupiter[:] = (90 - r_jupiter[:])
    r_jupiter[r_jupiter > 89] = np.inf


    r_sources = np.zeros((len(sources_alt_az), n_points), dtype=np.float)
    for i in range (len(sources_list)):
        r_sources[i][:] = sources_alt_az[i][:].alt.degree
    r_sources[r_sources < 0] = 0
    for i in range (len(sources_list)):
        r_sources[i][:] = (90 - r_sources[i][:])

    r_pulsars = np.zeros((len(pulsars_alt_az), n_points), dtype=np.float)
    for i in range (len(pulsars_list)):
        r_pulsars[i][:] = pulsars_alt_az[i][:].alt.degree
    r_pulsars[r_pulsars < 0] = 0
    for i in range (len(pulsars_list)):
        r_pulsars[i][:] = (90 - r_pulsars[i][:])


    # *** Sky altitude/azimuth polar plot figure ***

    rc('font', size = 6, weight='bold')
    fig = plt.figure(figsize = (9, 6))

    ax1 = fig.add_subplot(111, projection='polar')
    ax1.set_theta_zero_location("N")
    ax1.plot(sun_alt_az.az.rad, r_sun, label = 'Sun', color = 'C1', linewidth = 5, alpha = 0.5) #
    ax1.plot(sun_alt_az[center].az.rad,  r_sun[center], marker='o', markersize = 5, color ='C1')
    ax1.plot(jupiter_alt_az.az.rad, r_jupiter, label = 'Jupiter', color = 'C4', linewidth = 5, alpha = 0.5) #
    ax1.plot(jupiter_alt_az[center].az.rad,  r_jupiter[center], marker='o', markersize = 5, color = 'C4')

    for i in range (len(sources_list)):
        ax1.plot(sources_alt_az[i].az.rad, r_sources[i], label = sources_list[i], linewidth = 1, color = color[i]) #
        ax1.plot(sources_alt_az[i][center].az.rad,  r_sources[i][center], marker='o', markersize = 3, color = color[i])
    for i in range (len(pulsars_list)):
        ax1.plot(pulsars_alt_az[i].az.rad, r_pulsars[i], label = pulsars_list[i], linestyle = '--', linewidth = 0.5, color = color[i]) #
        ax1.plot(pulsars_alt_az[i][center].az.rad,  r_pulsars[i][center], marker='o', markersize = 3, color = color[i])

    ax1.set_ylim(0, 90)
    ax1.set_yticks(np.arange(0, 90, 10))
    ax1.set_rlabel_position(180)
    plt.legend(loc='upper right', bbox_to_anchor=(1.10, 0.22))

    fig.text(0.497, 0.890, 'North', fontsize=6, color = 'b', transform=plt.gcf().transFigure)
    fig.text(0.225, 0.470, 'East', fontsize=6, transform=plt.gcf().transFigure)
    fig.text(0.775, 0.470, 'West', fontsize=6, transform=plt.gcf().transFigure)
    fig.text(0.496, 0.090, 'South', fontsize=6, color = 'r', transform=plt.gcf().transFigure)
    fig.text(0.210, 0.900, 'Position of sources in the sky', fontsize=8, transform=plt.gcf().transFigure)
    fig.text(0.210, 0.880, 'Observatory: ' + observatory, fontsize=6, transform=plt.gcf().transFigure)
    fig.text(0.210, 0.860, 'Lon:', fontsize=5, transform=plt.gcf().transFigure)
    fig.text(0.210, 0.845, 'Lat:', fontsize=5, transform=plt.gcf().transFigure)
    fig.text(0.230, 0.860, str(utr2_location.lon).replace("d", "\u00b0 " ).replace("m", "\' " ).replace("s", "\'\' " ), fontsize=5, transform=plt.gcf().transFigure)
    fig.text(0.230, 0.845, str(utr2_location.lat).replace("d", "\u00b0 " ).replace("m", "\' " ).replace("s", "\'\' " ), fontsize=5, transform=plt.gcf().transFigure)
    fig.text(0.640, 0.890, 'From:', fontsize=5, transform=plt.gcf().transFigure)
    fig.text(0.640, 0.875, 'Till:', fontsize=5, transform=plt.gcf().transFigure)
    fig.text(0.682, 0.890, str(start_time)[0:19] + ' UTC', fontsize=5, transform=plt.gcf().transFigure)
    fig.text(0.682, 0.875, str(end_time)[0:19] + ' UTC', fontsize=5, transform=plt.gcf().transFigure)
    fig.text(0.640, 0.860, 'Markers:', fontsize=5, transform=plt.gcf().transFigure)
    fig.text(0.682, 0.860, str(time_window[center])[0:19] + ' UTC', fontsize=5, transform=plt.gcf().transFigure)
    fig.text(0.640, 0.845, '(for middle of predefined time window)', fontsize=5, transform=plt.gcf().transFigure)

    fig.text(0.210, 0.080, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
    fig.text(0.210, 0.070, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)

    pylab.savefig(newpath + '/'+ str(start_time)[0:10] + ' sky map.png', bbox_inches='tight', dpi = 300)
    #plt.show()


    # Plot of culmination times
    objects = ['', 'Sun', 'Jupiter']
    for i in range (len(sources_list)):
        objects.append(sources_list[i])
    for i in range (len(pulsars_list)):
        objects.append(pulsars_list[i])
    objects.append('')


    rc('font', size = 6, weight='bold')
    fig, ax1 = plt.subplots(figsize=(9, 6))


    # Sun
    xmax, ymax = find_max_altitude(sun_alt_az) # Sun
    x_rise, x_set = find_rize_and_set_points(sun_alt_az)
    plt.axvline(x=xmax, linewidth = '0.8' , color = 'C1', alpha=0.7)
    if x_rise < xmax and xmax < x_set:
        plt.barh(1, x_set-x_rise, left = x_rise, height = 0.5, color = 'C1', alpha = 0.4)
    plt.barh(1, 241, left = xmax-120, height = 0.5, color = 'C1', alpha = 0.7)
    plt.barh(1, 121, left = xmax-60,  height = 0.5, color = 'C1')
    plt.barh(1, 3,   left = xmax-1,   height = 0.5, color = 'r')
    plt.annotate(str(time_window[int(xmax)])[11:19], xy=(xmax, 1 + 0.3), fontsize = 6, ha='center')
    if x_rise > 0: plt.annotate(str(time_window[x_rise])[11:19], xy=(x_rise, 1 + 0.3), fontsize = 6, ha='left')
    if x_set < n_points-1: plt.annotate(str(time_window[x_set])[11:19], xy=(x_set, 1 + 0.3), fontsize = 6, ha='right')

    # Jupiter`
    xmax, ymax = find_max_altitude(jupiter_alt_az) # Jupiter`
    x_rise, x_set = find_rize_and_set_points(jupiter_alt_az)
    if x_rise < xmax and xmax < x_set:
        plt.barh(2, x_set-x_rise, left = x_rise, height = 0.5, color = 'C4', alpha = 0.4)
    if x_rise > xmax and xmax > x_set:
        plt.barh(2, x_set, left = 0, height = 0.5, color = 'C4', alpha = 0.4)
    plt.axvline(x=xmax, linewidth = '0.8' , color = 'C4', alpha=0.7)
    plt.barh(2, 241, left = xmax-120, height = 0.5, color = 'C4', alpha = 0.7)
    plt.barh(2, 121, left = xmax-60,  height = 0.5, color = 'C4')
    plt.barh(2, 3,   left = xmax-1,   height = 0.5, color = 'r')
    plt.annotate(str(time_window[int(xmax)])[11:19], xy=(xmax, 2 + 0.3), fontsize = 6, ha='center')
    if x_rise > 0: plt.annotate(str(time_window[x_rise])[11:19], xy=(x_rise, 2 + 0.3), fontsize = 6, ha='left')
    if x_set < n_points-1: plt.annotate(str(time_window[x_set])[11:19], xy=(x_set, 2 + 0.3), fontsize = 6, ha='right')



    '''
    # Jupiter`
    xmax, ymax = find_max_altitude(jupiter_alt_az) # Jupiter`
    x_rise, x_set = find_rize_and_set_points(jupiter_alt_az, 0)

    print(x_rise, xmax, x_set)

    k_rize = 0
    k_sets = 0
    if len(x_rise) == 0 and len(x_set) == 0 and ymax > 0:
        plt.barh(2, n_points, left = 0, height = 0.5, color = 'C4', alpha = 0.4)
    if len(x_rise) > len(x_set):
        k_rize = 1
        plt.barh(2, n_points-x_rise[-1], left = x_rise[-1], height = 0.5, color = 'C4', alpha = 0.4)
    if len(x_rise) < len(x_set):
        k_sets = 1
        plt.barh(2, x_set[-1], left = 0, height = 0.5, color = 'C4', alpha = 0.4)

    num = np.min([len(x_rise) - k_rize, len(x_set) - k_sets])
    for i in range (num):
        plt.barh(2, x_set[i]-x_rise[i], left = x_rise[i], height = 0.5, color = 'C4', alpha = 0.4)

    plt.axvline(x=xmax, linewidth = '0.8' , color = 'C4', alpha=0.7)
    plt.barh(2, 241, left = xmax-120, height = 0.5, color = 'C4', alpha = 0.7)
    plt.barh(2, 121, left = xmax-60,  height = 0.5, color = 'C4')
    plt.barh(2, 3,   left = xmax-1,   height = 0.5, color = 'r')
    plt.annotate(str(time_window[int(xmax)])[11:19], xy=(xmax, 2 + 0.3), fontsize = 6, ha='center')
    if len(x_rise) > 0:
        if x_rise[0] > 0: plt.annotate(str(time_window[x_rise[0]])[11:19], xy=(x_rise[0], 2 + 0.3), fontsize = 6, ha='left')
    if len(x_set) > 0:
        if x_set[0] < n_points-1: plt.annotate(str(time_window[x_set[0]])[11:19], xy=(x_set[0], 2 + 0.3), fontsize = 6, ha='right')
    '''


    for i in range (len(sources_list)):
        n = i+3
        xmax, ymax = find_max_altitude(sources_alt_az[i]) # Sources
        x_rise, x_set = find_rize_and_set_points(sources_alt_az[i])
        if x_rise < xmax and xmax < x_set:
            plt.barh(n, x_set-x_rise, left = x_rise, height = 0.5, color = color[i], alpha = 0.4)
        plt.axvline(x=xmax, linewidth = '0.8' , color = color[i], alpha=0.7)
        plt.barh(n, 241, left = xmax-120, height = 0.5, color = color[i], alpha = 0.7)
        plt.barh(n, 121, left = xmax-60,  height = 0.5, color = color[i])
        plt.barh(n, 3,   left = xmax-1,   height = 0.5, color = 'r')
        plt.annotate(str(time_window[int(xmax)])[11:19], xy=(xmax, n + 0.3), fontsize = 6, ha='center')
        if x_rise > 0: plt.annotate(str(time_window[x_rise])[11:19], xy=(x_rise, n + 0.3), fontsize = 6, ha='left')
        if x_set < n_points-1: plt.annotate(str(time_window[x_set])[11:19], xy=(x_set, n + 0.3), fontsize = 6, ha='right')


    for i in range (len(pulsars_list)):
        n = i+3 + len(sources_list)
        xmax, ymax = find_max_altitude(pulsars_alt_az[i]) # Pulsars
        x_rise, x_set = find_rize_and_set_points(pulsars_alt_az[i])
        if x_rise < xmax and xmax < x_set:
            plt.barh(n, x_set-x_rise, left = x_rise, height = 0.5, color = color[i], alpha = 0.4)
        plt.axvline(x=xmax, linewidth = '0.8' , color = color[i], alpha=0.7)
        plt.barh(n, 241, left = xmax-120, height = 0.5, color = color[i], alpha = 0.7)
        plt.barh(n, 121, left = xmax-60,  height = 0.5, color = color[i])
        plt.barh(n, 3,   left = xmax-1,   height = 0.5, color = 'r')
        plt.annotate(str(time_window[int(xmax)])[11:19], xy=(xmax, n + 0.3), fontsize = 6, ha='center')
        if x_rise > 0: plt.annotate(str(time_window[x_rise])[11:19], xy=(x_rise, n + 0.3), fontsize = 6, ha='left')
        if x_set < n_points-1: plt.annotate(str(time_window[x_set])[11:19], xy=(x_set, n + 0.3), fontsize = 6, ha='right')


    plt.xlabel('UTC time', fontsize = 8, fontweight='bold')
    ax1.set_xlim([0, n_points-1])
    ax1.yaxis.set_major_locator(mtick.LinearLocator(len(objects)))
    ax1.set_ylim([0, len(objects) - 1])
    ax1.set_yticklabels(objects[:])

    ax1.xaxis.set_major_locator(mtick.LinearLocator(15))
    ax1.xaxis.set_minor_locator(mtick.LinearLocator(25))
    plt.xticks(ticks_list, time_ticks_list)
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(ax1.get_xticks())
    ax2.set_xticklabels(ax1.get_xticklabels())
    fig.suptitle('Culmination and observation time of sources for ' + observatory, fontsize = 8, fontweight='bold')
    ax1.set_title('Time period: '+ str(start_time)[0:19] + ' - ' + str(end_time)[0:19], fontsize = 7)
    fig.subplots_adjust(top=0.9)
    fig.text(0.79, 0.04, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
    fig.text(0.11, 0.04, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)

    pylab.savefig(newpath + '/'+ str(start_time)[0:10] +' culmination times.png', bbox_inches='tight', dpi = 300)

    return

################################################################################
################################################################################

if __name__ == '__main__':

    start_time = Time('2019-10-01 12:00:00')
    end_time = Time('2019-10-02 12:00:00')
    pulsars_list = ['B0329+54', 'B0809+74', 'B1133+16', 'B1508+55', 'B1919+21']
    sources_list = ['Cas A', 'Syg A', 'Vir A', 'Crab'] #

    sources_positions_on_the_sky(start_time, end_time, pulsars_list, sources_list)
