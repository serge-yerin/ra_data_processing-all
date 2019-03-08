# FEATURES TO ADD
# Make check of the frequencies to cut lag between the limits of the band
# make possible to average in time the raw dedispersed data to increase SNR
# Incorporate data on UTR-2 and GURT effective area, background temperatures and show data in fluxes
# Make the rolling of SNR curve to easy finding of the noise area
# https://stackoverflow.com/questions/9111711/get-coordinates-of-local-maxima-in-2d-array-above-certain-value
# https://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.ndimage.filters.maximum_filter.html


# Python3
Software_version = '2019.01.21'
# Program intended to read, show and analyze averaged pulse data of pulsar observation from SMD files
# SMD file is a result of data processing by the pipeline written in IDL by V. V. Zakharenko



#*************************************************************
#                   IMPORT LIBRARIES                         *
#*************************************************************
# Common functions
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show
import struct
import math
import pylab
import os
import numpy as np
import time

# My functions
from f_plot_formats import plot1D, plot2D
from f_pulsar_DM_compensation import DM_compensation
from f_pulsar_DM_variation import DM_variation
from f_choose_frequency_range import chooseFreqRange
from f_file_header_ADR import FileHeaderReaderADR
from f_file_header_JDS import FileHeaderReaderDSP
from f_SMD_analyzer_param_reader import SMD_analyzer_param_reader
  
   
    
# ******************************************************************
# *                          MAIN PROGRAM                          *
# ******************************************************************

for i in range (8): print (' ')
print ('   ****************************************************')
print ('   *      Pulsar data processing v.',Software_version,'       *      (c) YeS 2019')
print ('   ****************************************************')
for i in range (3): print (' ')


# Reading parameters of analysis

[filename, path, DM, no_of_DM_steps, DM_var_step, 
    save_intermediate_data, AverageChannelNumber, 
    AverageTPointsNumber, frequency_band_cut, 
    specify_freq_range, frequency_cuts, 
    colormap, customDPI, freqStartArray, freqStopArray] = SMD_analyzer_param_reader()

  
filepath = path + filename

#**************************************************************
# ***                  Opening datafile                     ***
#**************************************************************
print ('  File to be analyzed: ', filename)
print (' ')


smd_filesize = (os.stat(filepath).st_size)       # Size of file
print ('  File size: ', round(smd_filesize/1024/1024, 6), ' Mb')

# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
newpath = filename + '_results'
if not os.path.exists(newpath):
    os.makedirs(newpath)



#**************************************************************
# ***              Reading data file header                 ***
#**************************************************************


# Jumping to the end of the file to read the data file header with parameters of data record

if filename[0:3] == 'ADR':
    [TimeRes, fmin, fmax, df, frequencyList0, FFTsize] = FileHeaderReaderADR(filepath, smd_filesize - 1024 - 131096)  
if filename[0:3] == 'DSP':
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        CLCfrq, df_creation_timeUTC, SpInFile, ReceiverMode, Mode, Navr, 
        TimeRes, fmin, fmax, df, frequencyList0, FFTsize] = FileHeaderReaderDSP(filepath, smd_filesize - 1024)
    df = df / pow(10,6)

file = open(filepath, 'rb')


#   *** Reading pulsar period and number of samples per period ***
print (' Dispersion measure =           ', DM, ' pc / cm3    ')
pulsarPeriod = struct.unpack('d', file.read(8))[0]
print (' Pulsar period =                ', pulsarPeriod, ' s')
samplesPerPeriod = struct.unpack('h', file.read(2))[0]
print (' Number of frequency channels = ', FFTsize)
print (' Number of samples in time =    ', samplesPerPeriod)



#**************************************************************
# ***                Reading data matrix                    ***
#**************************************************************

file.seek(12)   # Jump to 12 byte of the file, where matrix begins

print ('\n  * Redaing data... \n')
initial_matrix = np.fromfile(file, dtype='f4', count = (samplesPerPeriod * FFTsize))
initial_matrix = np.reshape(initial_matrix, [samplesPerPeriod, FFTsize])     

print ('    Matrix shape: ', initial_matrix.shape)

file.close()

#**************************************************************
# ***   Calculations and figures plotting for specified DM  ***
#**************************************************************

print ('\n  * Calculations and figures... \n')

    
# *** Preparing the phase of pulse sequence instead of time ***

phaseOfPulse = [0 for col in range(samplesPerPeriod)]
for i in range (samplesPerPeriod):
    if (i > 0):
        phaseOfPulse[i] = (i / float(samplesPerPeriod)) * 360.
    else:
        phaseOfPulse[i] = 0

# *** Preparing matrix which will be processed to save the initial data ***
inter_matrix = np.zeros((FFTsize,samplesPerPeriod))
initial_matrix = initial_matrix.transpose()
inter_matrix[:,:] = initial_matrix[:,:]

# *** Cutting the array inside frequency range specified by user ***               
if specify_freq_range == 1: 
    frequencyList0, initial_matrix, FFTsize, fmin, fmax = chooseFreqRange (frequencyList0, inter_matrix, freqStartArray, freqStopArray, FFTsize, fmin, fmax)

# *** To save initial matrix for further processing with the same name with or without cut of frequencies
del inter_matrix
inter_matrix = np.zeros((FFTsize,samplesPerPeriod))
inter_matrix[:,:] = initial_matrix[:,:]


# *** Check the profiles of initial matrix before processing ***
if save_intermediate_data == 1:
    integrProfile0 = np.array([])
    integrProfile1 = np.array([])
    integrProfile0 = (np.sum(inter_matrix, axis = 0))
    integrProfile1 = (np.sum(inter_matrix, axis = 1))
    
    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=None, right=None, top=0.86, wspace=None, hspace=0.3)
    plt.subplot(2, 1, 1)
    plt.title('Raw data integrated over time and over frequency \n File: '+filename, fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
    plt.plot(integrProfile0)
    plt.xlabel('Samples in time', fontsize = 8, fontweight='bold')
    plt.ylabel('Dummy vlues', fontsize = 8, fontweight='bold')
    plt.xticks(fontsize = 6, fontweight = 'bold')    
    plt.yticks(fontsize = 6, fontweight = 'bold')
    
    plt.subplot(2, 1, 2)
    plt.plot(integrProfile1)
    plt.xlabel('Frequency points', fontsize = 8, fontweight='bold')
    plt.ylabel('Dummy vlues', fontsize = 8, fontweight='bold')
    plt.xticks(fontsize = 6, fontweight = 'bold')    
    plt.yticks(fontsize = 6, fontweight = 'bold')
    pylab.savefig(filename + '_results/01.1 - Raw data integrated over time and over frequency.png', bbox_inches='tight', dpi = 250)
    plt.close('all') 


    

# *** Plot of raw data without DM compensation and data reduction ***

if save_intermediate_data == 1:
    plot2D(inter_matrix, filename + '_results/01 - Raw data.png', frequencyList0, colormap, 'Raw pulsar pulse \n File: '+filename, customDPI)
    


# *** Compensation of DM (dispersion delay) ***

matrix, shiftPar = DM_compensation(inter_matrix, FFTsize, fmin, fmax, df, TimeRes, pulsarPeriod, DM, filename, save_intermediate_data, customDPI)
del inter_matrix


# *** Saving shift parameter for dispersion delay compensation vs. frequency to file and plot ***
if save_intermediate_data == 1:

    ShiftParTXT = open(filename + '_results/Shift parameter (initial DM).txt', "w")
    for i in range(FFTsize):
        ShiftParTXT.write(str(fmin + df * i)+'   '+str(shiftPar[i])+' \n' )
    ShiftParTXT.close()
    
    plot1D(shiftPar, filename + '_results/01.2 - Shift parameter (initial DM).png', 'Shift parameter', 'Shift parameter', 'Shift parameter', 'Frequency channel number', customDPI)
 
    

# *** Plot of the data with DM compensation but without data reduction ***

if save_intermediate_data == 1:
    plot2D(matrix, filename + '_results/02 - Dedispersed data.png', frequencyList0, colormap, 'Dedispersed pulsar pulse \n File: '+filename, customDPI)
    


# *** Averaging data in frequency domain ***
    
reducedMatrix = np.array([[0.0 for col in range(samplesPerPeriod)] for row in range(int(FFTsize/AverageChannelNumber))])
for i in range (int(FFTsize/AverageChannelNumber)):
    for j in range (samplesPerPeriod):
        reducedMatrix[i, j] = sum(matrix[i*AverageChannelNumber : (i+1)*AverageChannelNumber, j])


print ('\n    Length of initial frequency axis: ', len(frequencyList0))
frequencyList1 = frequencyList0[::AverageChannelNumber]
print ('    Length of new frequency axis:     ', len(frequencyList1), ' \n')


# *** Plot of raw data with DM compensation and data reduction ***

if save_intermediate_data == 1:
    plot2D(reducedMatrix, filename + '_results/03 - Dedispersed integrated data.png', frequencyList1, colormap, 'Dedispersed and averaged in frequency pulsar pulse \n File: '+filename, customDPI)
    


  
#   *** Integrated over band temporal profile ***

freq_channels, time_points = reducedMatrix.shape 
print ('\n    Matrix shape: ', freq_channels, time_points)


# *** Matrix sum in one dimension for noise area detection ***
integrProfile = np.array([])
integrProfile = (np.sum(reducedMatrix, axis = 0))

print ('\n  * Check the noise segment and close the plot, then enter needed data ')

plt.figure()
plt.plot(integrProfile)
plt.xlabel('Phase of pulsar period')
plt.ylabel('Data')
if save_intermediate_data == 1:
    pylab.savefig(filename + '_results/04 - Raw integrated data to find pulse.png', bbox_inches='tight', dpi = 250)
plt.show()
plt.close('all') 


# *** Entering the first and last index of noise segment in integrated plot

beginIndex  = int(input('\n    First index of noise segment:           '))
endIndex    = int(input('\n    Last index of noise segment:            '))



# ***   Matrix sum in one dimension and mean value extraction  ***

for i in range (freq_channels):
    reducedMatrix[i,:] = reducedMatrix[i,:] - np.mean(reducedMatrix[i, beginIndex:endIndex])
integrProfile = np.array([])
integrProfile = (np.sum(reducedMatrix, axis = 0))


# ***   Calculations of SNR   ***

noise = integrProfile[beginIndex : endIndex]
noise_mean = np.mean(noise)
noise_std = np.std(noise)
integrProfile = (integrProfile - np.mean(noise))/np.std(noise)


# ***   Calculation of number of points to roll the pulse   ***

roll_number = int((len(integrProfile)/2) - np.argmax(integrProfile))

# ***   Rolling the pulse to the center of the plot  ***
integrProfile = np.roll(integrProfile, roll_number) # Rolling the vector to make the pulse in the center
SNRinitMax = np.max(integrProfile)

# ***   Plotting and saving the SNR curve  ***
plot1D(integrProfile, filename + '_results/05 - SNR.png', 'Averaged profile for DM = ' + str(round(DM, 3)), 'Averaged pulse profile in band ' + str(round(frequencyList0[0],3)) + ' - ' + str(round(frequencyList0[len(frequencyList0)-1],3)) + ' MHz \n File: '+filename, 'SNR', 'Phase of pulsar period', customDPI)





#****************************************************************
# ***   Calculations and figures for various frequency bands  ***
#****************************************************************


if frequency_band_cut == 1:     # Plot profiles in small frequency bands?
    
    no_of_freq_bands = len(frequency_cuts) + 1
    band_freq_name = ["" for i in range(no_of_freq_bands)]
    SNRmax_in_band = np.zeros((no_of_freq_bands))
    SNRperMHZ_in_band = np.zeros((no_of_freq_bands))
    band_frequencies = np.zeros((no_of_freq_bands, 2)) # matrix of bands frequency limits
    profiles_varBand = np.zeros((no_of_freq_bands, time_points)) # matrix for all profiles
    for band in range (no_of_freq_bands):
        
        # Find the limits of the frquency range
        if band == 0:
            freqStart = frequencyList0[0]
            freqStop = frequency_cuts[band]
        elif band == no_of_freq_bands-1:
            freqStart = frequency_cuts[band-1]
            freqStop = frequencyList0[len(frequencyList0)-1]
        else:
            freqStart = frequency_cuts[band-1]
            freqStop = frequency_cuts[band]

        print ('\n  * Calculations for frequency subband ', round(freqStart,3), ' - ', round(freqStop,3), ' MHz')
    
        # Forming the array of data in specified subband and frequency list
        A = []
        B = []
        for i in range (len(frequencyList0)):
            A.append(abs(frequencyList0[i] - freqStart))
            B.append(abs(frequencyList0[i] - freqStop))
        ifmin = A.index(min(A))
        ifmax = B.index(min(B))
        array = matrix[ifmin:ifmax, :]
        print ('    New data array shape is: ', array.shape)
        freqBandList = frequencyList0[ifmin:ifmax]
        plot2D(array, filename + '_results/02-'+str(band+1)+' - Dedispersed data for subband '+str(round(freqStart,3))+'-'+str(round(freqStop,3))+' MHz.png', freqBandList, colormap, 'Dedispersed pulsar pulse in frequency range '+str(round(freqStart,3))+'-'+str(round(freqStop,3))+' MHz \n File: '+filename, customDPI)
 

        
        # ***   Matrix sum in one dimension   ***
        for i in range (len(freqBandList)):
            array[i,:] = array[i,:] - np.mean(array[i, beginIndex:endIndex])
        integrBandProfile = np.array([])
        integrBandProfile = (np.sum(array, axis = 0))
        
        
        # ***   Calculations of SNR   ***
        noiseBand = integrBandProfile[beginIndex : endIndex]
        integrBandProfile = (integrBandProfile - np.mean(noiseBand))/np.std(noiseBand)
        
        
        # ***   Rolling the pulse to the center of the plot  ***
        integrBandProfile = np.roll(integrBandProfile, roll_number) # Rolling the vector to make the pulse in the center
        
        
        # ***   Plotting and saving the SNR curve  ***
        plot1D(integrBandProfile, filename + '_results/04-'+str(band+1)+' - SNR for subband '+str(round(freqStart,3))+'-'+str(round(freqStop,3))+' MHz.png', 'Averaged profile', 'Pulsar average pulse profile in range '+str(round(freqStart,3))+'-'+str(round(freqStop,3))+' MHz  \n File: '+filename, 'SNR', 'Samples in pulsar period', customDPI)
        
        profiles_varBand[band, :] = integrBandProfile
        band_frequencies[band, 0] = freqStart
        band_frequencies[band, 1] = freqStop
        SNRmax_in_band[band] = np.max(integrBandProfile)
        band_freq_name[band] = str(round(freqStart,3)) + '-' + str(round(freqStop,3))
        SNRperMHZ_in_band[band] = (SNRmax_in_band[band] / (band_frequencies[band, 1] - band_frequencies[band, 0]))


    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    for band in range (no_of_freq_bands):
        plt.plot(profiles_varBand[band, :], label = str(round(band_frequencies[band, 0],3))+' - '+str(round(band_frequencies[band, 1],3))+' MHz')
    plt.title('All subbands profiles on single figure \n File: '+filename, fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
    plt.legend(loc = 'upper right', fontsize = 10) 
    plt.ylabel('SNR', fontsize = 10, fontweight='bold')
    plt.xlabel('Samples in pulsar period', fontsize = 10, fontweight='bold')
    plt.yticks(fontsize = 8, fontweight = 'bold')
    plt.xticks(fontsize = 8, fontweight = 'bold')
    pylab.savefig(filename + '_results/06.1 - SNR of pulse profile in subbands.png', bbox_inches='tight', dpi = customDPI)
    plt.close('all')

    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    for band in range (no_of_freq_bands):
        plt.plot(profiles_varBand[band, :] / np.max(profiles_varBand[band, :]), label = str(round(band_frequencies[band, 0],3))+' - '+str(round(band_frequencies[band, 1],3))+' MHz')
    plt.title('All subbands normalized profiles on single figure \n File: '+filename, fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
    plt.legend(loc = 'upper right', fontsize = 10) 
    plt.ylabel('Normalized SNR', fontsize = 10, fontweight='bold')
    plt.xlabel('Samples in pulsar period', fontsize = 10, fontweight='bold')
    plt.yticks(fontsize = 8, fontweight = 'bold')
    plt.xticks(fontsize = 8, fontweight = 'bold')
    pylab.savefig(filename + '_results/06.2 - Normalized SNR of pulse profile in subbands.png', bbox_inches='tight', dpi = customDPI)
    plt.close('all')

    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    for band in range (no_of_freq_bands):
        plt.plot(profiles_varBand[band, :] - np.max(profiles_varBand[band, :]), label = str(round(band_frequencies[band, 0],3))+' - '+str(round(band_frequencies[band, 1],3))+' MHz')
    plt.title('All subbands profiles with maximums at the same level \n File: '+filename, fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
    plt.legend(loc = 'upper right', fontsize = 10) 
    plt.ylabel('SNR', fontsize = 10, fontweight='bold')
    plt.xlabel('Samples in pulsar period', fontsize = 10, fontweight='bold')
    plt.yticks(fontsize = 8, fontweight = 'bold')
    plt.xticks(fontsize = 8, fontweight = 'bold')
    pylab.savefig(filename + '_results/06.3 - SNR of pulse profile with same maximum levels in subbands.png', bbox_inches='tight', dpi = customDPI)
    plt.close('all')


    fig, ax = plt.subplots(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    plt.plot(SNRmax_in_band, label = 'SNR vs. frequency band')
    plt.plot(SNRmax_in_band, 'ro', markersize = 3)
    plt.title('SNR values in subbands of analysis  \n File: '+filename, fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
    plt.legend(loc = 'upper left', fontsize = 10) 
    plt.ylabel('SNR', fontsize = 10, fontweight='bold')
    plt.xlabel('Bands of analysis, MHz', fontsize = 10, fontweight='bold')
    plt.yticks(fontsize = 8, fontweight = 'bold')
    plt.xticks(fontsize = 8, fontweight = 'bold', rotation=0)
    a = ax.get_xticks().tolist()
    for i in range(len(a)-1):
        k = int(a[i])
        a[i] = band_freq_name[k]
    ax.set_xticklabels(a)  
    pylab.savefig(filename + '_results/06.4 - SNR value vs. subbands.png', bbox_inches='tight', dpi = customDPI)
    plt.close('all')

    
    fig, ax = plt.subplots(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    plt.plot(SNRperMHZ_in_band, label = 'SNR / MHz vs. frequency band')
    plt.plot(SNRperMHZ_in_band, 'ro', markersize = 3)
    plt.title('SNR per MHz values in subbands of analysis  \n File: '+filename, fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
    plt.legend(loc = 'upper left', fontsize = 10) 
    plt.ylabel('SNR / MHz', fontsize = 10, fontweight='bold')
    plt.xlabel('Bands of analysis, MHz', fontsize = 10, fontweight='bold')
    plt.yticks(fontsize = 8, fontweight = 'bold')
    plt.xticks(fontsize = 8, fontweight = 'bold', rotation=0)
    a = ax.get_xticks().tolist()
    for i in range(len(a)-1):
        k = int(a[i])
        a[i] = band_freq_name[k]
    ax.set_xticklabels(a)  
    pylab.savefig(filename + '_results/06.5 - SNR per MHz value vs. subbands.png', bbox_inches='tight', dpi = customDPI)
    plt.close('all')

    
print('\n  * Calculation of SNR vs. DM plot... ')

# ***   Integration in time of overall average profile   ***

points = math.floor(time_points/AverageTPointsNumber)
integrProfileTimeAver = np.zeros((points))   # preparing the vector
for i in range (points):
    integrProfileTimeAver[i] = sum(integrProfile[i*AverageTPointsNumber : (i+1)*AverageTPointsNumber]) / (AverageTPointsNumber**0.5)

SNRinitDMtimeAver = np.max(integrProfileTimeAver)
    
# ***   Plotting and saving the integrated in time SNR curve  ***
plot1D(integrProfileTimeAver, filename + '_results/06 - Averaged SNR.png', 'Averaged profile', 'Averaged (in frequency and time) pulse profile in band ' + str(round(frequencyList0[0],3)) + ' - ' + str(round(frequencyList0[len(frequencyList0)-1],3)) + ' MHz \n File: '+filename, 'SNR', 'Samples in pulsar period', customDPI)




#*****************************************************************
# ***   Calculations and figures plotting for variation of DM  ***
#*****************************************************************

startTime = time.time()

# Integrated profiles with DM variation calculation
inter_matrix = np.zeros((FFTsize, samplesPerPeriod))
inter_matrix[:,:] = initial_matrix[:,:]
profiles_varDM, DM_vector = DM_variation(inter_matrix.transpose(), no_of_DM_steps, frequencyList0, FFTsize, fmin, fmax, df, TimeRes, pulsarPeriod, samplesPerPeriod, DM, filename, AverageChannelNumber, time_points, noise_mean, noise_std, beginIndex, endIndex, DM_var_step, roll_number, save_intermediate_data, customDPI)
del inter_matrix



# Preparing indexes for showing the maximal SNR value and its coordinates
DM_steps_real, time_points = profiles_varDM.shape
phase_vector = np.linspace(0,1,num = time_points)
optimal_DM_indexes = np.unravel_index(np.argmax(profiles_varDM, axis=None), profiles_varDM.shape) 
optimal_DM_index = optimal_DM_indexes[0]
optimal_pulse_phase = optimal_DM_indexes[1]
MAXpointX = phase_vector[optimal_pulse_phase]
MAXpointY = - (DM_vector[optimal_DM_index] - DM)
DMoptimal = round(DM_vector[optimal_DM_index], 5)

print(' \n\n ')
print('    Initial DM (from catalogue) =          ', DM, ' pc / cm3')
print('    SNR for initial DM =                   ', round(SNRinitMax, 3))
print('    SNR averaged in time for initial DM  = ', round(SNRinitDMtimeAver, 3), ' \n')

print('    Optimal DM =                           ', DMoptimal, ' pc / cm3  \n')
print('  * SNR for optimal DM can be calculated in the next part of the program')


# Saving integrated profiles with DM variation calculation to TXT file
if save_intermediate_data == 1:
    DM_Var_TXT = open(filename + '_results/Average profile vs DM 2D (initial DM).txt', "w")
    for step in range(DM_steps_real-1):
        DM_Var_TXT.write(''.join(format(DM_vector[step], "8.5f")) + '   '.join(format(profiles_varDM[step, i], "12.5f") for i in range(time_points)) + ' \n')
    DM_Var_TXT.close()



plt.figure(1, figsize = (10.0, 6.0))
plt.subplots_adjust(left = None, bottom = None, right = None, top = 0.86, wspace = None, hspace = None)
ImA = plt.imshow(np.flipud(profiles_varDM), aspect = 'auto', vmin = np.min(profiles_varDM), vmax = np.max(profiles_varDM),extent=[0,1,DM_vector[0]-DM,DM_vector[no_of_DM_steps-1]-DM], cmap=colormap) 
plt.title('Pulse profile vs DM in band ' + str(round(frequencyList0[0],3)) + ' - ' + str(round(frequencyList0[len(frequencyList0)-1],3)) + ' MHz \n File: ' + filename, fontsize = 8, fontweight = 'bold', style='italic', y=1.025)
plt.yticks(fontsize=8, fontweight='bold')
plt.xlabel('Phase of pulsar period', fontsize=8, fontweight='bold')
plt.ylabel('deltaDM', fontsize = 8, fontweight='bold')
plt.colorbar()
plt.xticks(fontsize = 8, fontweight = 'bold')
plt.text(0.76, 0.89,'Current SNR \n    '+str(round(SNRinitMax, 3)), fontsize=7, fontweight='bold', transform=plt.gcf().transFigure)
plt.text(0.76, 0.05, '  Current DM  \n'+str(round(DM, 4))+' pc / cm3', fontsize=7, fontweight='bold', transform=plt.gcf().transFigure)
pylab.savefig(filename + '_results/08 - SNR vs DM.png', bbox_inches='tight', dpi = customDPI) 
plt.close('all')        

endTime = time.time()    # Stop timer of calculations because next figure will popup and wait for response of user

plt.figure(1, figsize = (10.0, 6.0))
plt.subplots_adjust(left = None, bottom = None, right = None, top = 0.86, wspace = None, hspace = None)
ImA = plt.imshow(np.flipud(profiles_varDM), aspect = 'auto', vmin = np.min(profiles_varDM), vmax = np.max(profiles_varDM),extent=[0,1,DM_vector[0]-DM,DM_vector[no_of_DM_steps-1]-DM], cmap=colormap) 
plt.axhline(y = 0,   color = 'r', linestyle = '-', linewidth = 0.4)
plt.axvline(x = 0.5, color = 'r', linestyle = '-', linewidth = 0.4)
plt.plot(MAXpointX, - MAXpointY, marker = 'o', markersize = 1.5, color = 'chartreuse') 
plt.title('Pulse profile vs DM in band ' + str(round(frequencyList0[0],3)) + ' - ' + str(round(frequencyList0[len(frequencyList0)-1],3)) + ' MHz \n File: ' + filename, fontsize = 8, fontweight = 'bold', style='italic', y=1.025)
plt.yticks(fontsize=8, fontweight='bold')
plt.xlabel('Phase of pulsar period', fontsize=8, fontweight='bold')
plt.ylabel('deltaDM', fontsize = 8, fontweight='bold')
plt.colorbar()
plt.xticks(fontsize = 8, fontweight = 'bold')
plt.text(0.76, 0.89,'Current SNR \n    '+str(round(SNRinitMax, 3)), fontsize=7, fontweight='bold', transform=plt.gcf().transFigure)
plt.text(0.76, 0.05, '  Current DM  \n'+str(round(DM, 4))+' pc / cm3', fontsize=7, fontweight='bold', transform=plt.gcf().transFigure)
pylab.savefig(filename + '_results/07 - SNR vs DM.png', bbox_inches='tight', dpi = customDPI) 
plt.show()
plt.close('all')    



    
for i in range (2): print (' ')
print ('  In band calculations and DM variation lasted for ', round((endTime - startTime),3), 'seconds')
for i in range (2): print (' ')




if DM != DMoptimal:
    print ('  Current DM differs from fouund optimal DM. \n')
    optimization_switch = int(input('\n  Enter "1" for optimal DM pulse analysis (or "0" tp stop):        '))    
else:
    print ('  Current DM and optimal DM coincide. \n')
    optimization_switch = 0
    
    
del reducedMatrix, integrProfile, matrix, DM






#****************************************************************
# ***               Repeat program for optimal DM             ***
#****************************************************************




if optimization_switch == 1:
    DM = DMoptimal
    
    print ('\n\n  * Working with optimal DM = '+str(DMoptimal)+' pc / cm3 ...')

    # *** Preparing matrix which will be processed to save the initial data ***

    inter_matrix = np.zeros((FFTsize, samplesPerPeriod))
    inter_matrix[:,:] = initial_matrix[:,:]


    # *** Compensation of DM (dispersion delay) ***

    matrix, shiftPar = DM_compensation(inter_matrix, FFTsize, fmin, fmax, df, TimeRes, pulsarPeriod, DM, filename, save_intermediate_data, customDPI)
    del inter_matrix
    

    # *** Plot of the data with DM compensation but without data reduction ***

    if save_intermediate_data == 1:
        plot2D(matrix, filename + '_results/12 - Dedispersed data optimal DM.png', frequencyList0, colormap, 'Dedispersed pulsar pulse \n File: '+filename, customDPI)
        #print ('\n    12 - Dedispersed data.png created \n')


    # *** Averaging data in frequency domain ***
    reducedMatrix = np.array([[0.0 for col in range(samplesPerPeriod)] for row in range(int(FFTsize/AverageChannelNumber))])
    for i in range (int(FFTsize/AverageChannelNumber)):
        for j in range (samplesPerPeriod):
            reducedMatrix[i, j] = sum(matrix[i*AverageChannelNumber : (i+1)*AverageChannelNumber, j])

    frequencyList1 = frequencyList0[::AverageChannelNumber]
    

    # *** Plot of raw data with DM compensation and data reduction ***
    if save_intermediate_data == 1:
        plot2D(reducedMatrix, filename + '_results/13 - Dedispersed integrated data optimal DM.png', frequencyList1, colormap, 'Dedispersed and averaged in frequency pulsar pulse \n File: '+filename, customDPI)
        #print ('\n    03 - Dedispersed integrated data.png created \n')


    #   *** Integrated over band temporal profile ***
    freq_channels, time_points = reducedMatrix.shape 
    #print ('\n  Matrix shape: ', freq_channels, time_points)


    # *** Matrix sum in one dimension for noise area detection ***
    integrProfile = np.array([])
    integrProfile = (np.sum(reducedMatrix, axis = 0))

    print ('\n  * Check the noise segment and close the plot, then enter needed data ')

    plt.figure()
    plt.plot(integrProfile)
    plt.xlabel('Phase of pulsar period')
    plt.ylabel('Data')
    if save_intermediate_data == 1:
        pylab.savefig(filename + '_results/14 - Raw integrated data to find pulse optimal DM.png', bbox_inches='tight', dpi = 250)
    plt.show()
    plt.close('all') 

    # *** Entering the first and last index of noise segment in integrated plot
    beginIndex  = int(input('\n    First index of noise segment:           '))
    endIndex    = int(input('\n    Last index of noise segment:            '))

    startTime = time.time()

    # ***   Matrix sum in one dimension   ***
    for i in range (freq_channels):
        reducedMatrix[i,:] = reducedMatrix[i,:] - np.mean(reducedMatrix[i, beginIndex:endIndex])
    integrProfile = np.array([])
    integrProfile = (np.sum(reducedMatrix, axis = 0))

    # ***   Calculations of SNR   ***
    noise = integrProfile[beginIndex : endIndex]
    noise_mean = np.mean(noise)
    noise_std = np.std(noise)
    integrProfile = (integrProfile - np.mean(noise))/np.std(noise)

    # ***   Calculation of number of points to roll the pulse   ***
    roll_number = int((len(integrProfile)/2) - np.argmax(integrProfile))

    # ***   Rolling the pulse to the center of the plot  ***
    integrProfile = np.roll(integrProfile, roll_number) # Rolling the vector to make the pulse in the center
    SNRoptMax = np.max(integrProfile)

    # ***   Plotting and saving the SNR curve  ***
    plot1D(integrProfile, filename + '_results/15 - SNR optimal DM.png', 'Averaged profile for DM = ' + str(round(DM, 3)), 'Averaged pulse profile with optimal DM in band ' + str(round(frequencyList0[0],3)) + ' - ' + str(round(frequencyList0[len(frequencyList0)-1],3)) + ' MHz \n File: '+filename, 'SNR', 'Phase of pulsar period', customDPI)



    #****************************************************************
    # ***   Calculations and figures for various frequency bands  ***
    #****************************************************************


    if frequency_band_cut == 1:     # Plot profiles in small frequency bands?

        no_of_freq_bands = len(frequency_cuts) + 1
        band_freq_name = ["" for i in range(no_of_freq_bands)]
        SNRmax_in_band = np.zeros((no_of_freq_bands))
        SNRperMHZ_in_band = np.zeros((no_of_freq_bands))
        band_frequencies = np.zeros((no_of_freq_bands, 2)) # matrix of bands frequency limits
        profiles_varBand = np.zeros((no_of_freq_bands, time_points)) # matrix for all profiles

        for band in range (no_of_freq_bands):
        
            # Find the limits of the frquency range
            if band == 0:
                freqStart = frequencyList0[0]
                freqStop = frequency_cuts[band]
            elif band == no_of_freq_bands-1:
                freqStart = frequency_cuts[band-1]
                freqStop = frequencyList0[len(frequencyList0)-1]
            else:
                freqStart = frequency_cuts[band-1]
                freqStop = frequency_cuts[band]

            print ('\n  * Calculations for frequency range', round(freqStart,3), '-', round(freqStop,3), 'MHz')
        
            # Forming the array of data in specified range and frequency list
            A = []
            B = []
            for i in range (len(frequencyList0)):
                A.append(abs(frequencyList0[i] - freqStart))
                B.append(abs(frequencyList0[i] - freqStop))
            ifmin = A.index(min(A))
            ifmax = B.index(min(B))
            array = matrix[ifmin:ifmax, :]
            print ('    New data array shape is: ', array.shape)
            freqBandList = frequencyList0[ifmin:ifmax]
            plot2D(array, filename + '_results/12-'+str(band+1)+' - Dedispersed data for range '+str(round(freqStart,3))+'-'+str(round(freqStop,3))+' MHz optimal DM.png', freqBandList, colormap, 'Dedispersed pulsar pulse in frequency range '+str(round(freqStart,3))+'-'+str(round(freqStop,3))+' MHz \n File: '+filename, customDPI)
    
            
            # ***   Matrix sum in one dimension   ***
            for i in range (len(freqBandList)):
                array[i,:] = array[i,:] - np.mean(array[i, beginIndex:endIndex])
            integrBandProfile = np.array([])
            integrBandProfile = (np.sum(array, axis = 0))
            
            # ***   Calculations of SNR   ***
            noiseBand = integrBandProfile[beginIndex : endIndex]
            integrBandProfile = (integrBandProfile - np.mean(noiseBand))/np.std(noiseBand)
            
            # ***   Rolling the pulse to the center of the plot  ***
            integrBandProfile = np.roll(integrBandProfile, roll_number) # Rolling the vector to make the pulse in the center
            
            # ***   Plotting and saving the SNR curve  ***
            plot1D(integrBandProfile, filename + '_results/14-'+str(band+1)+' - SNR for range '+str(round(freqStart,3))+'-'+str(round(freqStop,3))+' MHz optimal DM.png', 'Averaged profile', 'Pulsar average pulse profile in range '+str(round(freqStart,3))+'-'+str(round(freqStop,3))+' MHz  \n File: '+filename, 'SNR', 'Samples in pulsar period', customDPI)
            
   
            profiles_varBand[band, :] = integrBandProfile
            band_frequencies[band, 0] = freqStart
            band_frequencies[band, 1] = freqStop
            SNRmax_in_band[band] = np.max(integrBandProfile)
            band_freq_name[band] = str(round(freqStart,3)) + '-' + str(round(freqStop,3))
            SNRperMHZ_in_band[band] = (SNRmax_in_band[band] / (band_frequencies[band, 1] - band_frequencies[band, 0]))

    
        plt.figure(1, figsize=(10.0, 6.0))
        plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
        for band in range (no_of_freq_bands):
            plt.plot(profiles_varBand[band, :], label = str(round(band_frequencies[band, 0],3))+' - '+str(round(band_frequencies[band, 1],3))+' MHz')
        plt.title('All band profiles on single figure', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
        plt.legend(loc = 'upper right', fontsize = 10) 
        plt.ylabel('SNR', fontsize = 10, fontweight='bold')
        plt.xlabel('Samples in pulsar period', fontsize = 10, fontweight='bold')
        plt.yticks(fontsize = 8, fontweight = 'bold')
        plt.xticks(fontsize = 8, fontweight = 'bold')
        pylab.savefig(filename + '_results/16.1 - Averaged SNR in bands optimal DM.png', bbox_inches='tight', dpi = customDPI)
        plt.close('all')
    
        plt.figure(1, figsize=(10.0, 6.0))
        plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
        for band in range (no_of_freq_bands):
            plt.plot(profiles_varBand[band, :] / np.max(profiles_varBand[band, :]), label = str(round(band_frequencies[band, 0],3))+' - '+str(round(band_frequencies[band, 1],3))+' MHz')
        plt.title('All band normalized profiles on single figure', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
        plt.legend(loc = 'upper right', fontsize = 10) 
        plt.ylabel('SNR', fontsize = 10, fontweight='bold')
        plt.xlabel('Samples in pulsar period', fontsize = 10, fontweight='bold')
        plt.yticks(fontsize = 8, fontweight = 'bold')
        plt.xticks(fontsize = 8, fontweight = 'bold')
        pylab.savefig(filename + '_results/16.2 - Averaged normalized SNR in bands optimal DM.png', bbox_inches='tight', dpi = customDPI)
        plt.close('all')

        plt.figure(1, figsize=(10.0, 6.0))
        plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
        for band in range (no_of_freq_bands):
            plt.plot(profiles_varBand[band, :] - np.max(profiles_varBand[band, :]), label = str(round(band_frequencies[band, 0],3))+' - '+str(round(band_frequencies[band, 1],3))+' MHz')
        plt.title('All band profiles with maximums at the same level \n File: '+filename, fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
        plt.legend(loc = 'upper right', fontsize = 10) 
        plt.ylabel('SNR', fontsize = 10, fontweight='bold')
        plt.xlabel('Samples in pulsar period', fontsize = 10, fontweight='bold')
        plt.yticks(fontsize = 8, fontweight = 'bold')
        plt.xticks(fontsize = 8, fontweight = 'bold')
        pylab.savefig(filename + '_results/16.3 - Averaged SNR with same maximum levels in bands optimal DM.png', bbox_inches='tight', dpi = customDPI)
        plt.close('all')
    
        fig, ax = plt.subplots(1, figsize=(10.0, 6.0))
        plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
        plt.plot(SNRmax_in_band, label = 'SNR vs. frequency band')
        plt.plot(SNRmax_in_band, 'ro', markersize = 3)
        plt.title('SNR values in subbands of analysis  \n File: '+filename, fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
        plt.legend(loc = 'upper left', fontsize = 10) 
        plt.ylabel('SNR', fontsize = 10, fontweight='bold')
        plt.xlabel('Bands of analysis, MHz', fontsize = 10, fontweight='bold')
        plt.yticks(fontsize = 8, fontweight = 'bold')
        plt.xticks(fontsize = 8, fontweight = 'bold', rotation=0)
        a = ax.get_xticks().tolist()
        for i in range(len(a)-1):
            k = int(a[i])
            a[i] = band_freq_name[k]
        ax.set_xticklabels(a)  
        pylab.savefig(filename + '_results/16.4 - SNR value vs. subbands optimal DM.png', bbox_inches='tight', dpi = customDPI)
        plt.close('all')
    
        
        fig, ax = plt.subplots(1, figsize=(10.0, 6.0))
        plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
        plt.plot(SNRperMHZ_in_band, label = 'SNR / MHz vs. frequency band')
        plt.plot(SNRperMHZ_in_band, 'ro', markersize = 3)
        plt.title('SNR per MHz values in subbands of analysis  \n File: '+filename, fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
        plt.legend(loc = 'upper left', fontsize = 10) 
        plt.ylabel('SNR / MHz', fontsize = 10, fontweight='bold')
        plt.xlabel('Bands of analysis, MHz', fontsize = 10, fontweight='bold')
        plt.yticks(fontsize = 8, fontweight = 'bold')
        plt.xticks(fontsize = 8, fontweight = 'bold', rotation=0)
        a = ax.get_xticks().tolist()
        for i in range(len(a)-1):
            k = int(a[i])
            a[i] = band_freq_name[k]
        ax.set_xticklabels(a)  
        pylab.savefig(filename + '_results/16.5 - SNR per MHz value vs. subbands optimal DM.png', bbox_inches='tight', dpi = customDPI)
        plt.close('all')

    
    print('\n  * Calculation of SNR vs. DM plot... ')
    
    # ***   Integration in time   ***
    
    points = math.floor(time_points/AverageTPointsNumber)
    integrProfileTimeAver = np.zeros((points))   # preparing the vector
    for i in range (points):
        integrProfileTimeAver[i] = sum(integrProfile[i*AverageTPointsNumber : (i+1)*AverageTPointsNumber]) / (AverageTPointsNumber**0.5)
        
    # ***   Plotting and saving the integrated in time SNR curve  ***
    plot1D(integrProfileTimeAver, filename + '_results/16 - Averaged SNR optimal DM.png', 'Averaged profile', 'Averaged (in frequency and time) pulse profile in band ' + str(round(frequencyList0[0],3)) + ' - ' + str(round(frequencyList0[len(frequencyList0)-1],3)) + ' MHz \n File: '+filename, 'SNR', 'Samples in pulsar period', customDPI)

    SNRoptimDMtimeAver = np.max(integrProfileTimeAver)
    
    
    #*****************************************************************
    # ***   Calculations and figures plotting for variation of DM  ***
    #*****************************************************************
    
    
    # Integrated profiles with DM variation calculation
    profiles_varDM, DM_vector = DM_variation(initial_matrix.transpose(), no_of_DM_steps, frequencyList0, FFTsize, fmin, fmax, df, TimeRes, pulsarPeriod, samplesPerPeriod, DM, filename, AverageChannelNumber, time_points, noise_mean, noise_std, beginIndex, endIndex, DM_var_step, roll_number, save_intermediate_data, customDPI)
    
    # Preparing indexes for showing the maximal SNR value and its coordinates
    freq_channels, time_points = profiles_varDM.shape
    phase_vector = np.linspace(0,1,num = time_points)
    optimal_DM_indexes = np.unravel_index(np.argmax(profiles_varDM, axis=None), profiles_varDM.shape) #np.argmax(profiles_varDM)
    optimal_DM_index = optimal_DM_indexes[0]
    optimal_pulse_phase = optimal_DM_indexes[1]
    MAXpointX = phase_vector[optimal_pulse_phase]
    MAXpointY = - (DM_vector[optimal_DM_index] - DM)
    
    print(' \n\n ')
    print('    Maximal SNR for optimal DM =           ', round(SNRoptMax, 3))
    print('    SNR averaged in time for optimal DM  = ', round(SNRoptimDMtimeAver, 3), ' \n')

    print('    Optimal DM  =                          ', round(DM, 4), ' pc / cm3')
    
    
    
    plt.figure(1, figsize = (10.0, 6.0))
    plt.subplots_adjust(left = None, bottom = None, right = None, top = 0.86, wspace = None, hspace = None)
    ImA = plt.imshow(np.flipud(profiles_varDM), aspect = 'auto', vmin = np.min(profiles_varDM), vmax = np.max(profiles_varDM),extent=[0,1,DM_vector[0]-DM,DM_vector[no_of_DM_steps-1]-DM], cmap=colormap) 
    plt.axhline(y = 0,   color = 'r', linestyle = '-', linewidth = 0.4)
    plt.axvline(x = 0.5, color = 'r', linestyle = '-', linewidth = 0.4)
    plt.plot(MAXpointX, - MAXpointY, marker = 'o', markersize = 1.5, color = 'chartreuse') # 'y' '#008000'
    plt.title('Pulse profile vs DM in band ' + str(round(frequencyList0[0],3)) + ' - ' + str(round(frequencyList0[len(frequencyList0)-1],3)) + ' MHz \n File: ' + filename, fontsize = 8, fontweight = 'bold', style='italic', y=1.025)
    plt.yticks(fontsize=8, fontweight='bold')
    plt.xlabel('Phase of pulsar period', fontsize=8, fontweight='bold')
    plt.ylabel('deltaDM', fontsize = 8, fontweight='bold')
    plt.colorbar()
    plt.xticks(fontsize = 8, fontweight = 'bold')
    plt.text(0.76, 0.89,'Current SNR \n    '+str(round(SNRoptMax, 3)), fontsize=7, fontweight='bold', transform=plt.gcf().transFigure)
    plt.text(0.76, 0.05, '  Current DM  \n' +str(round(DM, 4))+' pc / cm3', fontsize=7, fontweight='bold', transform=plt.gcf().transFigure)
    
    pylab.savefig(filename + '_results/17 - SNR vs DM for optimal DM.png', bbox_inches='tight', dpi = customDPI) 
    plt.show()
    plt.close('all')    
        

    plt.figure(1, figsize = (10.0, 6.0))
    plt.subplots_adjust(left = None, bottom = None, right = None, top = 0.86, wspace = None, hspace = None)
    ImA = plt.imshow(np.flipud(profiles_varDM), aspect = 'auto', vmin = np.min(profiles_varDM), vmax = np.max(profiles_varDM),extent=[0,1,DM_vector[0]-DM,DM_vector[no_of_DM_steps-1]-DM], cmap=colormap) 
    plt.title('Pulse profile vs DM in band ' + str(round(frequencyList0[0],3)) + ' - ' + str(round(frequencyList0[len(frequencyList0)-1],3)) + ' MHz \n File: ' + filename, fontsize = 8, fontweight = 'bold', style='italic', y=1.025)
    plt.yticks(fontsize=8, fontweight='bold')
    plt.xlabel('Phase of pulsar period', fontsize=8, fontweight='bold')
    plt.ylabel('deltaDM', fontsize = 8, fontweight='bold')
    plt.colorbar()
    plt.xticks(fontsize = 8, fontweight = 'bold')
    plt.text(0.76, 0.89,'Current SNR \n    '+str(round(SNRoptMax, 3)), fontsize=7, fontweight='bold', transform=plt.gcf().transFigure)
    plt.text(0.76, 0.05, '  Current DM  \n'+str(round(DM, 4))+' pc / cm3', fontsize=7, fontweight='bold', transform=plt.gcf().transFigure)
    pylab.savefig(filename + '_results/18 - SNR vs DM for optimal DM.png', bbox_inches='tight', dpi = customDPI) 
    plt.close('all')   




for i in range (4): print (' ')
print ('    *** Program has finished! ***')
for i in range (3): print (' ')















