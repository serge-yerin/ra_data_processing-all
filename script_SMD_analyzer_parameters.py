#*************************************************************
#                        PARAMETERS                          *
#*************************************************************

path = 'd:/PYTHON/ra_data_processing-all/DATA/'

filename = 'ADR_A150221_211250_PSRB0834+06.gcd.smd'

no_of_DM_steps = 721             # Number of DM steps to plot 361
DM_var_step = 0.002              # Step of optimal DM finding
save_intermediate_data = 0       # Plot intermediate figures? (1 = Yes)
AverageChannelNumber = 32        # Number of points to average in frequency
AverageTPointsNumber = 8         # Number of points to average time
frequency_band_cut = 0           # Plot profiles in small frequency bands?
specify_freq_range = 0           # Specify particular frequency range (1) or whole range (0)


frequency_cuts = [20.625, 24.750, 28.875]  # UTR-2 16.5 - 33 MHz divided into 4 bands
#frequency_cuts = [18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0]  # UTR-2 16.5 - 33 MHz divided bands of 2 MHz or less
#frequency_cuts = [17.0,18.0,19.0,20.0,21.0,22.0,23.0,24.0,25.0,26.0,27.0,28.0,29.0,30.0,31.0,32.0]  # UTR-2 16.5 - 33 MHz divided bands of 1 MHz or less
#frequency_cuts = [12.375, 16.5, 20.625, 24.750, 28.875]  # UTR-2 8.25 - 33 MHz divided into 6 bands
#frequency_cuts = [40.0, 50.0, 60.0]  # GURT 30 - 70 MHz divided into 4 bands

colormap = 'Greys'               # Possible: 'jet', 'Blues', 'Purples'
customDPI = 200

# Begin and end frequency of dynamic spectrum (MHz)
freqStartArray = 20.0
freqStopArray =  30.0

#DM = 0.0 # Dispersion measure of the pulses on Earth
#DM = 10.89   #PSRname='B0031-07' 
#DM = 49.423  #PSRname='B0114+58'
#DM = 34.8    #PSRname='B0138+59'
#DM = 25.66   #PSRname='B0148-06'
#DM = 15.74   #PSRname='B0301+19'
#DM = 26.01   #PSRname='B0320+39'    oldDM = 25.8 
#DM = 26.78   #PSRname='B0329+54'    oldDM = 26.83
#DM = 57.14   #PSRname='B0355+54' 
#DM = 14.3    #PSRname='B0450+55'
#DM = 50.915  #PSRname='B0525+21'  
#DM = 56.791  #PSRname='B0531+21' 
#DM = 27.14   #PSRname='B0609+37'
#DM = 5.750   #PSRname='B0809+74'    oldDM = 5.754    5.762  5.750-interpulse
#DM = 23.73   #PSRname='B0820+02'
#DM = 19.4751 #PSRname='B0823+26'
DM = 12.8579  #PSRname='B0834+06'     12.8579 - from catalogue
#DM = 27.27   #PSRname='B0919+06'
#DM = 15.33   #PSRname='B0943+10'    oldDM = 15.3500
#DM = 2.9730  #PSRname='B0950+08'    oldDM = 2.9702   2.9902
#DM = 9.195   #PSRname='B1112+50'
#DM = 4.8471  #PSRname='B1133+16'
#DM = 9.2755  #PSRname='B1237+25'
#DM = 19.623  #PSRname='B1508+55'
#DM = 14.6100 #PSRname='B1530+27'
#DM = 10.68   #PSRname='B1604-00'
#DM = 35.727  #PSRname='B1642-03'
#DM = 12.4400 #PSRname='B1919+21'    12.4309
#DM = 3.176   #PSRname='B1929+10'
#DM = 24.640  #PSRname='B2020+28'
#DM = 24.7    #PSRname='B2110+27'

#DM = 45.325  #PSRname='J0250+5854'   DM = 45.785    46.065
#DM = 3.8214  #PSRname='J0243+5267' 
#DM = 36.0    #PSRname='J0407+1607'
#DM = 21.02   #PSRname='J0459-0210'
