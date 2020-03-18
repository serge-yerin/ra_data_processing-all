# package "pulsar processing" of "ra_data_processing-all" repository 
Scripts and functions for visualizing and processing of pulsar radio astronomy data.

Additional libraries needed: numpy, matplotlib, astropy

In the package there are functions for doing one particular task and scripts for 
processing pipelines.
Each script has a so-called header "PARAMETERS" - several lines in the beginning 
of the script with all variables to be defined by user, so user does not need 
to search needed parameter in the code.

## script_pulsar_single_pulses.py
This script takes dynamic spectra data from ".dat" files made by other 
scripts (from spectra or waveform data), compensates the dispersion delay,
saves ".dat" file with compensated delay, plots spectra with compensated
delay and its time profile (data integrated in frequency range), saves the 
profile to ".txt" file, makes and plots its FFT (spectrum of time profile).


The script also has options for data cleaning, but the cleaning functions
are not ready and using implemented cleaning is very time consuming and 
not recommended.

Main parameters to specify:

*common_path* - path to ".dat" files and results. (empty string means project directory)

*filename* - name of ".dat" file to analyze (there must be the timeline ".txt" file as well)

*pulsar_name* - name of pulsar to take its DM from catalogue

*average_const* - number of frequency channels to appear in result dynamic spectra figure

*save_profile_txt* - '1' means to save ".txt" time profile and calculate its spectrum

*save_compensated_data* - '1' means to save data with compensated delay to new ".dat" file
 

 