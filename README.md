# "ra_data_processing-all" repository

Scripts and functions for visualizing and processing of radio astronomy data from Ukrainian low-frequency radio telescopes UTR-2, URAN, GURT (DSP and ADR receivers) as well as to control the ADR receivers to make scheduled observation.

Additional libraries needed are listed in **requirements.txt**.

On Linux you may have to install tkinter if the error 'No module named 'Tkinter'' appears with the command:

``` python
sudo apt-get install python3-tk
```

Instead of usual **opencv-python library** we use **opencv-python-headless** to avoid conflicts with **PyQt5** GUI frqmework.

Each script has several lines at its beginning with all variables to be defined by user, so user does not need to search parameters of processing in the code. Short descriptions of each parameters are given in the comments.

## Parameters of radio astronomy data to keep in mind

There are 2 receiver types:

* DSPZ (mainly used at UTR-2 & URAN with data files format **.jds**)
* ADR (Advanced Digital Receiver, mainly used at GURT with **.adr** data files extensions).

Both have similar structure but different format, so there are 2 corresponding types of scripts.

DSPZ & ADR receivers can record data in 3 main data types:

* auto-spectra (1 or 2 channels)
* cross-spectra (2 channels of auto-spectra + real & imaginary parts of cross-spectra)
* waveform data (1 or 2 channels).

Receivers can work with external clock generator which provides ADC samplig rate. The sampling rate can be adjusted. Typical sample rated used:

* **66 MHz** clock frequency provides 33 MHz band of receiver (usual at UTR-2 and URAN for DSPZ)
* **160 MHz** clock frequency provides 80 MHz band of receiver (usual at GURT fo ADR)
* **33 MHz** clock frequency provides 16.5 MHz band of receiver (sometimes used at UTR-2 to record waveform data to save data rate and record signal in 2-nd Niquist zone 16.5-33.0 MHz where UTR-2 has maximal sensitivity).

Usually receivers store data into 2GB files consequently, but ADR receiver can save data into continuous **.adr** file of any length. Each file has a 1024 byte header where parameters of the receiver and observations are stored.

## Scripts to visualize radio astronomy data

**Note:** The first step of any data processing is saving the original data into long **".dat"** (one per receiver channel data recorded or their combination) files which are convenient for further processing. Each file contains data of particular type (channel A or channel B or cross-spectra imaginary part or cross-spectra real part
or cross-spectra module or cross-spectra phase) of all initial data files.

These **".dat"** files are usually supplied with **"timeline.txt"** files which carry time stamps for data points.

 **".dat"** files can be processed with the **script_DAT_reader.py** to make PNG dynamic spectra of the whole observation with spectra averaging in time.

### script_ADR_multifolder_reader.py

This script makes **PNG images** of immediate and dynamic spectra for  auto and cross-spectra data from ADR. Also it can convert these data into **".dat"** format for further processing. It is convenient to analyze the observations data. One can indicate the path to a folder with a bunch of observations data in many subfolders. The script will anaylize each subfolder separately.

## Scripts to process pulsar data

These scripts are mostly stored in **"package_pulsar_processing"** folder.

### Processing of spectra observations: _script_sp_pulsar_pulses_incoherent_search.py_

**Input:** .jds files of pulsar or transients observations and pulsar name.

**Output:** dedispersed dynamic spectra & time profile of pulses, averaged (integrated) pulse.

### Processing of waveform observations

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

## Scripts to process data of Cas A secular flux decrease

These scripts are in "package_cas_a_secular_decrease" folder

### script_DAT_casA_secular_decrease.py

### script_DAT_casA_secular_decrease_GURT_long.py

### script_TXT3_casA_secular_decrease_stat.py

### script_TXT4_casA_secular_decrease_FFT_test.py

### script_TXT5_casA_secular_decrease_time_variations.py

To be described

## Scripts to control receivers

These scripts are in "package_receiver_control" folder.

### script_ADR_control.py

Basic script for single observations with ADR receiver. Script makes a folder to observe, synchronize receiver, each minute talks to the ADR server to stay connected, waits the time of recording start and stop, turns on and off the recording, reports via telegram. If checked, copies and processes data on the GURT server.  

### script_ADR_control_by_schedule.py

Script to observe with ADR receiver. Has the same basic functionality as the script_ADR_control.py but takes the schedule from txt file and able to make multiple observations. Use copy and process data option only if you are sure that copying and processing will finish at least 5 minutes before the next scheduled observation!