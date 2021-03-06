# UTR-2 antenna pattern calculation

#*******************************************************************************
#                              L I B R A R I E S                               *
#*******************************************************************************
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pylab
import time
import os

#*******************************************************************************
#                       M A I N   P A R A M E T E R S                          *
#*******************************************************************************

frequency = 18                                   # Frequency, MHz
ku = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])    # U-code (binary)
kv = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) # V-code (binary)
n_points = 501                                   # Number of points to model along each axes
plot_3D = 1                                      # To plot 3D plots which take much time?

#*******************************************************************************
#                A D D I T I O N A L   P A R A M E T E R S                     *
#*******************************************************************************

wavelength = (2.997 * np.power(10,2)) / frequency      # Wavelength, m
norm_freq = 1.570796 * frequency                       # Normalized frequency
h_dip = 3.5                                            # Height of UTR dipole above ground, m
d1 = 7.5                                               # Array spacing along NS direction, m
d2 = 9                                                 # Array spacing along EW direction, m
b = 111 / 90
C = ([1, 1, 1, 1])                                     # Amplitude distribution, for 5% field side lobes C = [1 0.65 0.57 0.35]
Ucur = np.linspace(-1.0, 1.0, num = n_points)          # Current U coordinates
Vcur = np.linspace(-1.0, 1.0, num = n_points)          # Current V coordinates
U, V = np.meshgrid(Ucur, Vcur)
z = np.array([8, 16, 64, 128, 8, 16, 64, 1024, 512])   # Supplementary matrix
center = int(np.floor(n_points/2)+1)                   # Center of both axes (zenith direction)

#*******************************************************************************
#                         M A I N    P R O G R A M                             *
#*******************************************************************************

startTime = time.time()
previousTime = startTime
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('\n  Today is ', currentDate, ' time is ', currentTime, '\n')
print ('\n  Central point is: ',  center)

# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
newpath = "UTR2_pattern"
if not os.path.exists(newpath):
    os.makedirs(newpath)

#*******************************************************************************
#                          C A L C U L A T I O N S                             *
#*******************************************************************************

# UTR-2 dipole antenna pattern
f_dip = np.zeros((n_points, n_points))
for i in range (0, n_points):
    for j in range(0, n_points):
        f_dip[i, j] = (1 - np.power(Ucur[i], 2)) * np.power(np.sin(((2 * np.pi * h_dip) / wavelength) * np.sqrt(1 - np.power(Ucur[i], 2)) - np.power(Vcur[j], 2)),2)

# Calculations of U and V codes in decimal notation
Nu = 0
for i in range (0, 10):
    Nu = Nu + ku[i] * np.power(2, ((i-1) * ku[i]))
Nv = 0
for j in range (0, 11):
    Nv = Nv + kv[j] * np.power(2, ((j-1) * kv[j]))
print ('\n\n  U code: ', Nu, ',    V code: ', Nv, '\n')


# Calculation of codes for different phase shifters
v = np.zeros(9)
u = np.zeros(9)
for i in range (0, 9):
    v[i] = np.power((-1), kv[i]) * (np.fix(((Nv - kv[i] * 1024) * z[i]) / 1024) + 0.5) / z[i]
    u[i] = np.power((-1), ku[i]) * (np.fix(((Nu - ku[i] * 512 ) * z[i]) / 512 ) + 0.5) / (1.2 * z[i])
# print(u, v)


#        *** Array factors of phase shifters of different stages ***

# Phase shifter 6-4 (North-South arm)
x1 = np.zeros(n_points)
f1 = np.zeros(n_points)
for i in range (0, n_points):
    x1[i] = 0.06 * norm_freq * (Ucur[i] - u[0])
    f1[i] = np.power(np.sin(6 * x1[i]) / (6 * np.sin(x1[i])), 2)

# Phase shifter 5-5 (North-South arm)
x2 = np.zeros(n_points)
f2 = np.zeros(n_points)
for j in range (0, n_points):
    x2[j] = 0.05 * norm_freq * (Vcur[j] - v[1])
    f2[j] = np.power(np.sin(5 * x2[j]) / (5 * np.sin(x2[j])), 2)

# Phase shifter 3-7 (North-South arm)
x3 = np.zeros(n_points)
f3 = np.zeros(n_points)
for j in range (0, n_points):
    x3[j] = 0.25 * norm_freq * (Vcur[j] - v[2])
    f3[j] = np.power(np.sin(3 * x3[j]) / (3 * np.sin(x3[j])), 2)

# Phase shifter 2-8 (North-South arm)
x4 = np.zeros(n_points)
f4 = np.zeros(n_points)
for j in range (0, n_points):
    x4[j] = 0.75 * norm_freq * (Vcur[j] - v[3])
    f4[j] = np.power(np.cos(x4[j]), 2)

# Phase shifter 6-4 (West arm)
x5 = np.zeros(n_points)
f5 = np.zeros(n_points)
for j in range (0, n_points):
    x5[j] = 0.05 * norm_freq * (Vcur[j] - v[4])
    f5[j] = np.power(np.sin(6 * x5[j]) / (6 * np.sin(x5[j])), 2)

# Phase shifter 5-5 (West arm)
x6 = np.zeros(n_points)
f6 = np.zeros(n_points)
for i in range (0, n_points):
    x6[i] = 0.06 * norm_freq * (Ucur[i] - u[5])
    f6[i] = np.power(np.sin(5 * x6[i]) / (5 * np.sin(x6[i])), 2)

# Phase shifter 5-7 (West arm)
x7 = np.zeros(n_points)
f7 = np.zeros(n_points)
for i in range (0, n_points):
    x7[i] = 0.30 * norm_freq * (Ucur[i] - u[6])
    f7[i] = np.power(np.sin(5 * x7[i]) / (5 * np.sin(x7[i])), 2)

x8 = np.zeros(n_points)
for j in range (0, n_points):
    x8[j] = 1.5 * norm_freq * (Vcur[j] - v[7])

x9 = np.zeros(n_points)
for i in range (0, n_points):
    x9[i] = 1.5 * norm_freq * (Ucur[i] - u[8])


# Antenna patterns of UTR-2 sections

f_north_section = np.zeros((n_points, n_points))
f_west_section = np.zeros((n_points, n_points))

for i in range (0, n_points):
    for j in range (0, n_points):
        f_north_section[i,j] = f_dip[i,j] * f1[i] * f2[j] * f3[j] * f4[j]
        f_west_section [i,j] = f_dip[i,j] * f5[j] * f6[i] * f7[i]


# Antenna patterns of UTR-2 arms

f_northsouth_arm = np.zeros((n_points, n_points))
f_west_arm = np.zeros((n_points, n_points))
for i in range (0, n_points):
    for j in range (0, n_points):
        f_northsouth_arm[i,j] =  f_north_section[i,j] * np.power((C[0] * np.cos(b * x8[j]) + C[1] * np.cos((b+2) * x8[j]) + C[2] * np.cos((b+4) * x8[j]) + C[3] * np.cos((b+6)*x8[j])), 2)
        f_west_arm [i,j] = f_west_section[i,j] * np.power((np.cos(2 * x9[i])), 2) * np.power((np.cos(x9[i])), 2)


# Antenna patterns of UTR-2 correlation beam (beam from the book)

f_utr2_pencil = np.zeros((n_points, n_points))
f_utr2_pencil = np.power(f_northsouth_arm * f_west_arm * np.cos(b * x9[i]), 2)


# Antenna patterns of UTR-2 sum beam (and probably difference beam)

f_utr2_sum = np.zeros((n_points, n_points))
#f_utr2_dif = np.zeros((n_points, n_points))
with np.errstate(divide='ignore', invalid='ignore'):
    f_utr2_sum = f_northsouth_arm * f_west_arm
    #f_utr2_dif = f_northsouth_arm / f_west_arm


nowTime = time.time()
print ('\n  Setup and patterns calculations      took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime


#*******************************************************************************
#                                F I G U R E S                                 *
#*******************************************************************************

#                          *** SINGLE UTR-2 DIPOLE ***

# Plot of antenna pattern of single UTR-2 dipole (heatmap)

fig = plt.figure(figsize = (16,8))
ax1 = fig.add_subplot(121)
ax1.imshow(f_dip.transpose(), cmap = 'jet')
ax1.set_title('UTR-2 dipole')
ax1 = fig.add_subplot(122)
ax1.imshow(f_dip.transpose(), cmap = 'jet')
ax1.set_title('UTR-2 dipole')
fig.suptitle('Antenna pattern of single UTR-2 dipole')
#fig.colorbar(fig, ax = ax1)
pylab.savefig(newpath+'/Map_fig_01_dipole.png', bbox_inches='tight', dpi = 300)
plt.close('all')

nowTime = time.time()
print ('\n  Plotting of Map_fig_01_dipole        took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime

# Plot of antenna pattern of single UTR-2 dipole (3D linear plot)

if plot_3D == 1:
    fig = plt.figure(figsize = (16,8))
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(U, V, f_dip, cmap = 'jet', rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax1.set_title('UTR-2 dipole')
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot_surface(U, V, f_dip, cmap = 'jet', rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax2.set_title('UTR-2 dipole')
    fig.suptitle('Antenna pattern of single UTR-2 dipole')
    pylab.savefig(newpath+'/3D_fig_01_dipole.png', bbox_inches='tight', dpi = 300)
    plt.close('all')

    nowTime = time.time()
    print ('\n  Plotting of 3D_fig_01_dipole         took ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime

# Calculation of the antenna pattern in logscale

with np.errstate(divide='ignore', invalid='ignore'):
    f_dip_log10 = np.log10(np.power(f_dip, 2))

nowTime = time.time()
print ('\n  Calculations of logarythmic pattern  took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime

# Plot of antenna pattern of single UTR-2 dipole (3D log plot)

fig = plt.figure(figsize = (16,8))
ax1 = fig.add_subplot(121)
ax1.imshow(f_dip_log10.transpose(), cmap = 'jet')
ax1.set_title('UTR-2 dipole')
ax1 = fig.add_subplot(122)
ax1.imshow(f_dip_log10.transpose(), cmap = 'jet')
ax1.set_title('UTR-2 dipole')
fig.suptitle('Antenna pattern of single UTR-2 dipole')
#fig.colorbar(fig, ax = ax1)
pylab.savefig(newpath+'/Map_dB_fig_01_dipole.png', bbox_inches='tight', dpi = 300)
plt.close('all')

nowTime = time.time()
print ('\n  Plotting of Map_dB_fig_01_dipole     took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime

if plot_3D == 1:
    with np.errstate(divide='ignore', invalid='ignore'):
        fig = plt.figure(figsize = (16,8))
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.plot_surface(U, V, f_dip_log10, rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax1.set_title('UTR-2 dipole')
        ax2 = fig.add_subplot(122, projection='3d')
        ax2.plot_surface(U, V, f_dip_log10, rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax2.set_title('UTR-2 dipole')
        fig.suptitle('Antenna pattern of single UTR-2 dipole in logarythmic scale')
        pylab.savefig(newpath+'/Log_fig_01_dipole.png', bbox_inches='tight', dpi = 300)
        plt.close('all')

    nowTime = time.time()
    print ('\n  Plotting of Log_fig_01_dipole        took ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime


#                        *** UTR-2 section patterns ***

# Plot of antenna pattern of UTR-2 sections (heatmap)

fig = plt.figure(figsize = (16,8))
ax1 = fig.add_subplot(121)
ax1.imshow(f_north_section.transpose(), cmap = 'jet')
ax1.set_title('North or South section of UTR-2')
ax2 = fig.add_subplot(122)
ax2.imshow(f_west_section.transpose(), cmap = 'jet')
ax2.set_title('West section of UTR-2')
fig.suptitle('Antenna pattern of UTR-2 sections')
pylab.savefig(newpath+'/Map_fig_02_sections.png', bbox_inches='tight', dpi = 300)
plt.close('all')

nowTime = time.time()
print ('\n  Plotting of Map_fig_02_sections      took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime

if plot_3D == 1:
    fig = plt.figure(figsize = (16,8))
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(U, V, f_north_section, cmap = 'jet', rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax1.set_title('North or South section of UTR-2')
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot_surface(U, V, f_west_section , cmap = 'jet', rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax2.set_title('West section of UTR-2')
    fig.suptitle('Antenna pattern of UTR-2 sections')
    pylab.savefig(newpath+'/3D_fig_02_sections.png', bbox_inches='tight', dpi = 300)
    plt.close('all')

    nowTime = time.time()
    print ('\n  Plotting of 3D_fig_02_sections       took ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime


f_norm_north_section = f_north_section / np.max(f_north_section)
f_norm_west_section  = f_west_section / np.max (f_west_section)

nowTime = time.time()
print ('\n  Pattern normalization                took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime


with np.errstate(divide='ignore', invalid='ignore'):
    f_norm_north_section_log10 = np.log10(np.power(f_norm_north_section, 2))
    f_norm_west_section_log10 = np.log10(np.power(f_norm_west_section, 2))


nowTime = time.time()
print ('\n  Calculations of logarythmic pattern  took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime


fig = plt.figure(figsize = (16,8))
ax1 = fig.add_subplot(121)
ax1.imshow(f_norm_north_section_log10.transpose(), cmap = 'jet')
ax1.set_title('North or South section of UTR-2')
ax1 = fig.add_subplot(122)
ax1.imshow(f_norm_west_section_log10.transpose(), cmap = 'jet')
ax1.set_title('West section of UTR-2')
fig.suptitle('Antenna pattern of UTR-2 sections in logarythmic scale (map)')
#fig.colorbar(fig, ax = ax1)
pylab.savefig(newpath+'/Map_dB_fig_02_sections.png', bbox_inches='tight', dpi = 300)
plt.close('all')

nowTime = time.time()
print ('\n  Plotting of Map_dB_fig_02_sections   took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime

if plot_3D == 1:
    with np.errstate(divide='ignore', invalid='ignore'):
        fig = plt.figure(figsize = (16,8))
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.plot_surface(U, V, f_norm_north_section_log10, rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax1.set_title('North or South section of UTR-2')
        ax2 = fig.add_subplot(122, projection='3d')
        ax2.plot_surface(U, V, f_norm_west_section_log10, rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax2.set_title('West section of UTR-2')
        fig.suptitle('Antenna pattern of UTR-2 sections in logarythmic scale')
        pylab.savefig(newpath+'/Log_fig_02_sections.png', bbox_inches='tight', dpi = 300)
        plt.close('all')

    nowTime = time.time()
    print ('\n  Plotting of Log_fig_02_sections      took ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime

#                        *** UTR-2 arms patterns ***

# Plot of antenna patterns of UTR-2 arms (heatmap)

fig = plt.figure(figsize = (16,8))
ax1 = fig.add_subplot(121)
ax1.imshow(f_northsouth_arm.transpose(), cmap = 'jet')
ax1.set_title('North or South arm of UTR-2')
ax2 = fig.add_subplot(122)
ax2.imshow(f_west_arm.transpose(), cmap = 'jet')
ax2.set_title('West arm of UTR-2')
fig.suptitle('Antenna pattern of UTR-2 arms')
pylab.savefig(newpath+'/Map_fig_03_arms.png', bbox_inches='tight', dpi = 300)
plt.close('all')

nowTime = time.time()
print ('\n  Plotting of Map_fig_03_arms          took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime

if plot_3D == 1:
    fig = plt.figure(figsize = (16,8))
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(U, V, f_northsouth_arm, cmap = 'jet', rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax1.set_title('North or South arm of UTR-2')
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot_surface(U, V, f_west_arm , cmap = 'jet', rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax2.set_title('West arm of UTR-2')
    fig.suptitle('Antenna pattern of UTR-2 arms')
    pylab.savefig(newpath+'/3D_fig_03_arms.png', bbox_inches='tight', dpi = 300)
    plt.close('all')

    nowTime = time.time()
    print ('\n  Plotting of 3D_fig_03_arms           took ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime

with np.errstate(divide='ignore', invalid='ignore'):
    f_northsouth_arm_log10 = np.log10(np.power(f_northsouth_arm, 2))
    f_west_arm_log10 = np.log10(np.power(f_west_arm, 2))


nowTime = time.time()
print ('\n  Calculations of logarythmic pattern  took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime


fig = plt.figure(figsize = (16,8))
ax1 = fig.add_subplot(121)
ax1.imshow(f_northsouth_arm_log10.transpose(), cmap = 'jet')
ax1.set_title('North-South arm of UTR-2')
ax1 = fig.add_subplot(122)
ax1.imshow(f_west_arm_log10.transpose(), cmap = 'jet')
ax1.set_title('West arm of UTR-2')
fig.suptitle('Antenna pattern of UTR-2 arms in logarythmic scale (map)')
#fig.colorbar(fig, ax = ax1)
pylab.savefig(newpath+'/Map_dB_fig_03_arms.png', bbox_inches='tight', dpi = 300)
plt.close('all')

nowTime = time.time()
print ('\n  Plotting of Map_dB_fig_03_arms       took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime


if plot_3D == 1:
    with np.errstate(divide='ignore', invalid='ignore'):
        fig = plt.figure(figsize = (16,8))
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.plot_surface(U, V, f_northsouth_arm_log10, rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax1.set_title('North-South arm of UTR-2')
        ax2 = fig.add_subplot(122, projection='3d')
        ax2.plot_surface(U, V, f_west_arm_log10, rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax2.set_title('West arm of UTR-2')
        fig.suptitle('Antenna pattern of UTR-2 arms in logarythmic scale')
        pylab.savefig(newpath+'/Log_fig_03_arms.png', bbox_inches='tight', dpi = 300)
        plt.close('all')

    nowTime = time.time()
    print ('\n  Plotting of Log_fig_03_arms          took ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime


#                        *** 2D plots of patterns ***


with np.errstate(divide='ignore'):
    fig = plt.figure(figsize = (16,12))

    ax1 = fig.add_subplot(221)
    ax1.plot(f_northsouth_arm[:,center] / np.max(f_northsouth_arm[:,center]), label = 'NS arm')
    ax1.plot(f_west_arm[:,center] / np.max(f_west_arm[:,center]), label = 'W arm')
    ax1.plot(f_north_section[:,center] / np.max(f_north_section[:,center]), label = 'NS section')
    ax1.plot(f_west_section[:,center] / np.max(f_west_section[:,center]), label = 'W section')
    ax1.plot(f_dip[:,center] / np.max(f_dip[:,center]), label = 'Dipole')
    ax1.legend(loc = 'upper right', fontsize = 8)

    ax2 = fig.add_subplot(222)
    ax2.plot(f_northsouth_arm[center,:] / np.max(f_northsouth_arm[center,:]), label = 'NS arm')
    ax2.plot(f_west_arm[center,:] / np.max(f_west_arm[center,:]), label = 'W arm')
    ax2.plot(f_north_section[center,:] / np.max(f_north_section[center,:]), label = 'NS section')
    ax2.plot(f_west_section[center,:] / np.max(f_west_section[center,:]), label = 'W section')
    ax2.plot(f_dip[center,:] / np.max(f_dip[center,:]), label = 'Dipole')
    ax2.legend(loc = 'upper right', fontsize = 8)

    ax3 = fig.add_subplot(223)
    ax3.plot(np.log10(f_northsouth_arm[:,center] / np.max(f_northsouth_arm[:,center])), label = 'NS arm')
    ax3.plot(np.log10(f_west_arm[:,center] / np.max(f_west_arm[:,center])), label = 'W arm')
    ax3.plot(np.log10(f_north_section[:,center] / np.max(f_north_section[:,center])), label = 'NS section')
    ax3.plot(np.log10(f_west_section[:,center] / np.max(f_west_section[:,center])), label = 'W section')
    ax3.plot(np.log10(f_dip[:,center] / np.max(f_dip[:,center])), label = 'Dipole')
    ax3.legend(loc = 'lower center', fontsize = 8)

    ax4 = fig.add_subplot(224)
    ax4.plot(np.log10(f_northsouth_arm[center,:] / np.max(f_northsouth_arm[center,:])), label = 'NS arm')
    ax4.plot(np.log10(f_west_arm[center,:] / np.max(f_west_arm[center,:])), label = 'W arm')
    ax4.plot(np.log10(f_north_section[center,:] / np.max(f_north_section[center,:])), label = 'NS section')
    ax4.plot(np.log10(f_west_section[center,:] / np.max(f_west_section[center,:])), label = 'W section')
    ax4.plot(np.log10(f_dip[center,:] / np.max(f_dip[center,:])), label = 'Dipole')
    ax4.legend(loc = 'lower center', fontsize = 8)

    pylab.savefig(newpath+'/2D_Fig_03_antenna_patterns.png', bbox_inches='tight', dpi = 300)
    plt.close('all')


nowTime = time.time()
print ('\n  Plotting of 2D antenna patterns      took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime


with np.errstate(divide='ignore'):
    fig = plt.figure(figsize = (16,12))

    ax1 = fig.add_subplot(221)
    ax1.plot(f_northsouth_arm[:,center] / np.max(f_northsouth_arm[:,center]), label = 'NS arm')
    ax1.plot(f_west_arm[:,center] / np.max(f_west_arm[:,center]), label = 'W arm')
    ax1.set_xlim(center - 100, center + 100)
    ax1.legend(loc = 'upper right', fontsize = 8)

    ax2 = fig.add_subplot(222)
    ax2.plot(f_northsouth_arm[center,:] / np.max(f_northsouth_arm[center,:]), label = 'NS arm')
    ax2.plot(f_west_arm[center,:] / np.max(f_west_arm[center,:]), label = 'W arm')
    ax2.set_xlim(center - 100, center + 100)
    ax2.legend(loc = 'upper right', fontsize = 8)

    ax3 = fig.add_subplot(223)
    ax3.plot(np.log10(f_northsouth_arm[:,center] / np.max(f_northsouth_arm[:,center])), label = 'NS arm')
    ax3.plot(np.log10(f_west_arm[:,center] / np.max(f_west_arm[:,center])), label = 'W arm')
    ax3.set_xlim(center - 100, center + 100)
    ax3.legend(loc = 'lower center', fontsize = 8)

    ax4 = fig.add_subplot(224)
    ax4.plot(np.log10(f_northsouth_arm[center,:] / np.max(f_northsouth_arm[center,:])), label = 'NS arm')
    ax4.plot(np.log10(f_west_arm[center,:] / np.max(f_west_arm[center,:])), label = 'W arm')
    ax4.set_xlim(center - 100, center + 100)
    ax4.legend(loc = 'lower center', fontsize = 8)

    pylab.savefig(newpath+'/2D_Fig_04_antenna_patterna_magnified.png', bbox_inches='tight', dpi = 300)
    plt.close('all')


with np.errstate(divide='ignore'):
    fig = plt.figure(figsize = (16,12))

    ax1 = fig.add_subplot(221)
    ax1.plot(f_northsouth_arm[:,center], label = 'NS arm')
    ax1.plot(f_west_arm[:,center], label = 'W arm')
    ax1.set_xlim(center - 100, center + 100)
    ax1.legend(loc = 'upper right', fontsize = 8)

    ax2 = fig.add_subplot(222)
    ax2.plot(f_northsouth_arm[center,:], label = 'NS arm')
    ax2.plot(f_west_arm[center,:], label = 'W arm')
    ax2.set_xlim(center - 100, center + 100)
    ax2.legend(loc = 'upper right', fontsize = 8)

    ax3 = fig.add_subplot(223)
    ax3.plot(np.log10(f_northsouth_arm[:,center]), label = 'NS arm')
    ax3.plot(np.log10(f_west_arm[:,center]), label = 'W arm')
    ax3.set_xlim(center - 100, center + 100)
    ax3.legend(loc = 'lower center', fontsize = 8)

    ax4 = fig.add_subplot(224)
    ax4.plot(np.log10(f_northsouth_arm[center,:]), label = 'NS arm')
    ax4.plot(np.log10(f_west_arm[center,:]), label = 'W arm')
    ax4.set_xlim(center - 100, center + 100)
    ax4.legend(loc = 'lower center', fontsize = 8)

    pylab.savefig(newpath+'/2D_Fig_05_antenna_patterna_magnified.png', bbox_inches='tight', dpi = 300)
    plt.close('all')

nowTime = time.time()
print ('\n  Plotting of big 2D antenna patterns  took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime


#*******************************************************************************

fig = plt.figure(figsize = (16,8))
ax1 = fig.add_subplot(121)
ax1.imshow(f_utr2_pencil.transpose(), cmap = 'jet')
ax1.set_title('Pencil beam of UTR-2')
ax2 = fig.add_subplot(122)
ax2.imshow(f_utr2_pencil.transpose(), cmap = 'jet')
ax2.set_title('Pencil beam of UTR-2')
fig.suptitle('Antenna pattern of entire UTR-2 pencil beam')
pylab.savefig(newpath+'/Map_fig_04_pencil.png', bbox_inches='tight', dpi = 300)
plt.close('all')

nowTime = time.time()
print ('\n  Plotting of Map_fig_04_pencil        took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime

fig = plt.figure(figsize = (16,8))
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(U, V, f_utr2_pencil, cmap = 'jet', rstride=1, cstride=1, linewidth=0, antialiased=False)
ax1.set_title('Pencil beam of UTR-2')
ax2 = fig.add_subplot(122, projection='3d')
ax2.plot_surface(U, V, f_utr2_pencil , cmap = 'jet', rstride=1, cstride=1, linewidth=0, antialiased=False)
ax2.set_title('Pencil beam of UTR-2')
fig.suptitle('Antenna pattern of entire UTR-2 pencil beam')
pylab.savefig(newpath+'/3D_fig_04_pencil.png', bbox_inches='tight', dpi = 300)
plt.close('all')

nowTime = time.time()
print ('\n  Plotting of fig_04_pencil            took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime

with np.errstate(divide='ignore', invalid='ignore'):
    f_utr2_pencil_log10 = np.log10(np.power(f_utr2_pencil, 2))


nowTime = time.time()
print ('\n  Calculations of logarythmic pattern  took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime


fig = plt.figure(figsize = (16,8))
ax1 = fig.add_subplot(121)
ax1.imshow(f_utr2_pencil_log10.transpose(), cmap = 'jet')
ax1.set_title('Pencil beam of UTR-2')
ax1 = fig.add_subplot(122)
ax1.imshow(f_utr2_pencil_log10.transpose(), cmap = 'jet')
ax1.set_title('Pencil beam of UTR-2')
fig.suptitle('Antenna pattern of entire UTR-2 pencil beam in logarythmic scale (map)')
#fig.colorbar(fig, ax = ax1)
pylab.savefig(newpath+'/Map_dB_fig_04_pencil.png', bbox_inches='tight', dpi = 300)
plt.close('all')

nowTime = time.time()
print ('\n  Plotting of Map_dB_fig_04_pencil     took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime



with np.errstate(divide='ignore', invalid='ignore'):
    fig = plt.figure(figsize = (16,8))
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(U, V, f_utr2_pencil_log10, rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax1.set_title('Pencil beam of UTR-2')
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot_surface(U, V, f_utr2_pencil_log10, rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax2.set_title('Pencil beam of UTR-2')
    fig.suptitle('Antenna pattern of entire UTR-2 pencil beam in logarythmic scale')
    pylab.savefig(newpath+'/Log_fig_04_pencil.png', bbox_inches='tight', dpi = 300)
    plt.close('all')

nowTime = time.time()
print ('\n  Plotting of Log_fig_04_pencil        took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime


#*******************************************************************************

nowTime = time.time()
print ('\n  Calculation of sum-dif patterns      took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime

fig = plt.figure(figsize = (16,8))
ax1 = fig.add_subplot(121)
ax1.imshow(f_utr2_sum.transpose(), cmap = 'jet')
ax1.set_title('Sum beam of UTR-2')
ax2 = fig.add_subplot(122)
ax2.imshow(f_utr2_sum.transpose(), cmap = 'jet')
ax2.set_title('Sum beam of UTR-2')
fig.suptitle('Antenna pattern of sum UTR-2 beam')
pylab.savefig(newpath+'/Map_fig_05_sum.png', bbox_inches='tight', dpi = 300)
plt.close('all')

nowTime = time.time()
print ('\n  Plotting of Map_fig_05_sum           took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime

if plot_3D == 1:
    with np.errstate(divide='ignore', invalid='ignore'):
        fig = plt.figure(figsize = (16,8))
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.plot_surface(U, V, f_utr2_sum, cmap = 'jet', rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax1.set_title('Sum beam of UTR-2')
        ax2 = fig.add_subplot(122, projection='3d')
        ax2.plot_surface(U, V, f_utr2_sum , cmap = 'jet', rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax2.set_title('Sum beam of UTR-2')
        fig.suptitle('Antenna pattern of sum UTR-2 beam')
        pylab.savefig(newpath+'/3D_fig_05_sum.png', bbox_inches='tight', dpi = 300)
        plt.close('all')

    nowTime = time.time()
    print ('\n  Plotting of 3D_fig_05_sum.png        took ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime

with np.errstate(divide='ignore', invalid='ignore'):
    f_utr2_sum_log10 = np.log10(np.power(f_utr2_sum, 2))
    #f_utr2_dif_log10 = np.log10(np.power(f_utr2_dif, 2))


nowTime = time.time()
print ('\n  Calculations of logarythmic pattern  took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime


fig = plt.figure(figsize = (16,8))
ax1 = fig.add_subplot(121)
ax1.imshow(f_utr2_sum_log10.transpose(), cmap = 'jet')
ax1.set_title('Sum beam of UTR-2')
ax1 = fig.add_subplot(122)
ax1.imshow(f_utr2_sum_log10.transpose(), cmap = 'jet')
ax1.set_title('Sum beam of UTR-2')
fig.suptitle('Antenna pattern of sum UTR-2 beam in logarythmic scale (map)')
#fig.colorbar(fig, ax = ax1)
pylab.savefig(newpath+'/Map_dB_fig_05_sum.png', bbox_inches='tight', dpi = 300)
plt.close('all')

nowTime = time.time()
print ('\n  Plotting of Map_dB_fig_05_sum        took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime


if plot_3D == 1:
    with np.errstate(divide='ignore', invalid='ignore'):
        fig = plt.figure(figsize = (16,8))
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.plot_surface(U, V, f_utr2_sum_log10, rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax1.set_title('Sum beam of UTR-2')
        ax2 = fig.add_subplot(122, projection='3d')
        ax2.plot_surface(U, V, f_utr2_sum_log10, rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax2.set_title('Sum beam of UTR-2')
        fig.suptitle('Antenna pattern of sum UTR-2 beam in logarythmic scale')
        pylab.savefig(newpath+'/Log_fig_05_sum.png', bbox_inches='tight', dpi = 300)
        plt.close('all')

    nowTime = time.time()
    print ('\n  Plotting of Log_fig_05_sum           took ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime


#*******************************************************************************
'''
f_utr2_pencil = np.zeros((n_points, n_points))
f_utr2_pencil = f_utr2_sum - f_utr2_dif


nowTime = time.time()
print ('\n  Calculation of pencil pattern        took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime

fig = plt.figure(figsize = (16,8))
ax1 = fig.add_subplot(121)
ax1.imshow(f_utr2_pencil.transpose(), cmap = 'jet')
ax1.set_title('Pencil beam of UTR-2')
ax2 = fig.add_subplot(122)
ax2.imshow(f_utr2_pencil.transpose(), cmap = 'jet')
ax2.set_title('Pencil beam of UTR-2')
fig.suptitle('Antenna pattern of entire UTR-2 pencil beam')
pylab.savefig(newpath+'/Map_fig_06_pencil.png', bbox_inches='tight', dpi = 300)
plt.close('all')

nowTime = time.time()
print ('\n  Plotting of Map_fig_06_pencil        took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime

if plot_3D == 1:
    fig = plt.figure(figsize = (16,8))
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(U, V, f_utr2_pencil, cmap = 'jet', rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax1.set_title('Pencil beam of UTR-2')
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot_surface(U, V, f_utr2_pencil , cmap = 'jet', rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax2.set_title('Pencil beam of UTR-2')
    fig.suptitle('Antenna pattern of entire UTR-2 pencil beam')
    pylab.savefig(newpath+'/3D_fig_06_pencil.png', bbox_inches='tight', dpi = 300)
    plt.close('all')

    nowTime = time.time()
    print ('\n  Plotting of fig_06_pencil            took ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime


with np.errstate(divide='ignore', invalid='ignore'):
    f_utr2_pencil_log10 = np.log10(np.power(f_utr2_pencil, 2))


nowTime = time.time()
print ('\n  Calculations of logarythmic pattern  took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime


fig = plt.figure(figsize = (16,8))
ax1 = fig.add_subplot(121)
ax1.imshow(f_utr2_pencil_log10.transpose(), cmap = 'jet')
ax1.set_title('Pencil beam of UTR-2')
ax1 = fig.add_subplot(122)
ax1.imshow(f_utr2_pencil_log10.transpose(), cmap = 'jet')
ax1.set_title('Pencil beam of UTR-2')
fig.suptitle('Antenna pattern of entire UTR-2 pencil beam in logarythmic scale (map)')
#fig.colorbar(fig, ax = ax1)
pylab.savefig(newpath+'/Map_dB_fig_06_pencil.png', bbox_inches='tight', dpi = 300)
plt.close('all')

nowTime = time.time()
print ('\n  Plotting of Map_dB_fig_06_pencil     took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime


if plot_3D == 1:
    with np.errstate(divide='ignore', invalid='ignore'):
        fig = plt.figure(figsize = (16,8))
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.plot_surface(U, V, f_utr2_pencil_log10, rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax1.set_title('Pencil beam of UTR-2')
        ax2 = fig.add_subplot(122, projection='3d')
        ax2.plot_surface(U, V, f_utr2_pencil_log10, rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax2.set_title('Pencil beam of UTR-2')
        fig.suptitle('Antenna pattern of entire UTR-2 pencil beam in logarythmic scale')
        pylab.savefig(newpath+'/Log_fig_06_pencil.png', bbox_inches='tight', dpi = 300)
        plt.close('all')

    nowTime = time.time()
    print ('\n  Plotting of Log_fig_06_pencil        took ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime


#*******************************************************************************
'''
with np.errstate(divide='ignore', invalid='ignore'):
    fig = plt.figure(figsize = (16,12))

    ax1 = fig.add_subplot(221)
    ax1.plot(f_utr2_sum[:,center], label = 'UTR-2 sum')
    #ax1.plot(f_utr2_dif[:,center], label = 'UTR-2 dif')
    ax1.plot(f_utr2_pencil[:,center], label = 'UTR-2 pencil')
    ax1.set_xlim(center - 100, center + 100)
    ax1.legend(loc = 'upper right', fontsize = 8)

    ax2 = fig.add_subplot(222)
    ax2.plot(f_utr2_sum[center,:], label = 'UTR-2 sum')
    #ax2.plot(f_utr2_dif[center,:], label = 'UTR-2 dif')
    ax2.plot(f_utr2_pencil[center,:], label = 'UTR-2 pencil')
    ax2.set_xlim(center - 100, center + 100)
    ax2.legend(loc = 'upper right', fontsize = 8)

    ax3 = fig.add_subplot(223)
    ax3.plot(np.log10(f_utr2_sum[:,center]), label = 'UTR-2 sum')
    #ax3.plot(np.log10(f_utr2_dif[:,center]), label = 'UTR-2 dif')
    ax3.plot(np.log10(f_utr2_pencil[:,center]), label = 'UTR-2 pencil')
    ax3.set_xlim(center - 100, center + 100)
    ax3.legend(loc = 'lower center', fontsize = 8)

    ax4 = fig.add_subplot(224)
    ax4.plot(np.log10(f_utr2_sum[center,:]), label = 'UTR-2 sum')
    #ax4.plot(np.log10(f_utr2_dif[center,:]), label = 'UTR-2 dif')
    ax4.plot(np.log10(f_utr2_pencil[center,:]), label = 'UTR-2 pencil')
    ax4.set_xlim(center - 100, center + 100)
    ax4.legend(loc = 'lower center', fontsize = 8)

    pylab.savefig(newpath+'/2D_Fig_06_antenna_patterns.png', bbox_inches='tight', dpi = 300)
    plt.close('all')



with np.errstate(divide='ignore', invalid='ignore'):
    fig = plt.figure(figsize = (16,12))

    ax1 = fig.add_subplot(221)
    ax1.plot(f_utr2_sum[:,center] / np.max(f_utr2_sum[:,center]), label = 'UTR-2 sum')
    #ax1.plot(f_utr2_dif[:,center] / np.max(f_utr2_dif[:,center]), label = 'UTR-2 dif')
    ax1.plot(f_utr2_pencil[:,center] / np.max(f_utr2_pencil[:,center]), label = 'UTR-2 pencil')
    ax1.set_xlim(center - 100, center + 100)
    ax1.legend(loc = 'upper right', fontsize = 8)

    ax2 = fig.add_subplot(222)
    ax2.plot(f_utr2_sum[center,:] / np.max(f_utr2_sum[center,:]), label = 'UTR-2 sum')
    #ax2.plot(f_utr2_dif[center,:] / np.max(f_utr2_dif[center,:]), label = 'UTR-2 dif')
    ax2.plot(f_utr2_pencil[center,:] / np.max(f_utr2_pencil[center,:]), label = 'UTR-2 pencil')
    ax2.set_xlim(center - 100, center + 100)
    ax2.legend(loc = 'upper right', fontsize = 8)

    ax3 = fig.add_subplot(223)
    ax3.plot(np.log10(f_utr2_sum[:,center] / np.max(f_utr2_sum[:,center])), label = 'UTR-2 sum')
    #ax3.plot(np.log10(f_utr2_dif[:,center] / np.max(f_utr2_dif[:,center])), label = 'UTR-2 dif')
    ax3.plot(np.log10(f_utr2_pencil[:,center] / np.max(f_utr2_pencil[:,center])), label = 'UTR-2 pencil')
    ax3.set_xlim(center - 100, center + 100)
    ax3.legend(loc = 'lower center', fontsize = 8)

    ax4 = fig.add_subplot(224)
    ax4.plot(np.log10(f_utr2_sum[center,:] / np.max(f_utr2_sum[center,:])), label = 'UTR-2 sum')
    #ax4.plot(np.log10(f_utr2_dif[center,:] / np.max(f_utr2_dif[center,:])), label = 'UTR-2 dif')
    ax4.plot(np.log10(f_utr2_pencil[center,:] / np.max(f_utr2_pencil[center,:])), label = 'UTR-2 pencil')
    ax4.set_xlim(center - 100, center + 100)
    ax4.legend(loc = 'lower center', fontsize = 8)

    pylab.savefig(newpath+'/2D_Fig_07_antenna_patterns.png', bbox_inches='tight', dpi = 300)
    plt.close('all')


nowTime = time.time()
print ('\n  Plotting of 2D antenna patterns      took ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime



endTime = time.time()
print ('\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n\n\n')
