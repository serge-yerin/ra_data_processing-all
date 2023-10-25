# "ra_data_processing-all" repository
Scripts and functions for visualizing and processing of radio astronomy data,
mainly from Ukrainian low-frequency radio telescopes UTR-2, URAN, GURT.

Additional libraries needed are listed in requirements.txt. 
On Linux you may have to install tkinter if the error 'No module named 'Tkinter'' appears with the command:

*sudo apt-get install python3-tk*


Each script has a so-called header, several lines in the beginning of the script
with all variables to be defined by user, so user does not need to search needed
parameter in the code. Short descriptions of each parameters are given in the 
comments.

## Scripts to control receivers
These scripts are in "package_common_modules" folder
### script_ADR_control.py
Basic script for single observations with ADR receiver. Script makes a folder 
to observe, synchronize receiver, each minute talks to the ADR server to stay 
connected, waits the time of recording start and stop, turns on and off the 
recording, reports via telegram. If checked, copies and processes data on 
the GURT server.  

### script_ADR_control_by_schedule.py
Script to observe with ADR receiver. Has the same basic functionality as the 
script_ADR_control.py but takes the schedule from txt file and able to make 
multiple observations. Use copy and process data option only if you are sure
that copying and processing will finish at least 5 minutes before the next 
scheduled observation!!! 

## Scripts to read and visualize radio astronomy data

### script_ADR_reader.py
This script is intended to read, visualize, normalize the data from ADR
(Advanced Digital Receiver) of GURT radio telescope. Also it can save these data
in a simpler to read format ".dat". This file contains data of particular type
(channel A or channel B or correlation imaginary part or correlation real part
or correlation module or correlation phase) of all initial ADR data files.
To supplement these data the ".txt" file is saved to provide information of date
and time of each spectra saved in ".dat" files.
DAT files can be further processed by script_DAT_reader.py to obtain dynamic
specter of all the observation (multiple ADR files) with averaging of spectra
in time.
Tu use the script one should specify the path to the folder with data (.adr
files) and specify the parameters of processing in the file header. 

### script_ADR_multifolder_reader.py
The script has the same basic functionality as script_ADR_reader.py but deals 
with multiple observation results folders stored in one parent folder.

## Scripts to process data of Cas A secular flux decrease
These scripts are in "package_cas_a_secular_decrease" folder
### script_DAT_casA_secular_decrease.py
### script_DAT_casA_secular_decrease_GURT_long.py
### script_TXT3_casA_secular_decrease_stat.py
### script_TXT4_casA_secular_decrease_FFT_test.py
### script_TXT5_casA_secular_decrease_time_variations.py

## Scripts to process pulsar data
These scripts are mostly stored in "package_pulsar_processing" folder.

# Searching of pulsar AIPs appearance time
To obtain integrated over frequency profile of dedsipersed spectra data from waveform data
one should:

1) use "script_JDS_WF_reader.py" from main project directory with parameters
 
* no_of_spectra_to_average = 16 (for 33 MHz clock it results in 7.942 ms time resolution)

* save_long_file_aver = 1 (to save '.dat' and 'timeline.txt' files)

  to convert from WF to spectra data in '.dat' file.

2) process the '.dat' and 'timeline.txt' files with script "script_pulsar_single_pulses.py" from 
"package_pulsar_processing" folder using
as parameters the name of the pulsar observed (DM will be taken from local pulsar catalogue automatically), and
the name of the '.dat' file from first stage.
The pictures will appear in folder "RESULTS_pulsar_single_pulses_..." in the main project folder.
