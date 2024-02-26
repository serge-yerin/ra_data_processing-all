# Low-Frequency Radio Astronomy tools

Scripts and functions for visualizing and processing of radio astronomy data from Ukrainian low-frequency radio telescopes UTR-2, URAN, GURT (DSP and ADR receivers) as well as to control the ADR receivers to make scheduled observation.

Additional libraries needed are listed in **requirements.txt**. The most used scripts were sucessfully run with **Python 3.11.8**, but there could be some files that were not tested for a long time.

On Linux you may have to install tkinter if the error 'No module named 'Tkinter'' appears with the command:

``` python
sudo apt-get install python3-tk
```

Instead of usual **opencv-python library** we use **opencv-python-headless** to avoid conflicts with **PyQt5** GUI framework.

Each script has several lines at its beginning with all variables to be defined by user, so no need to search processing parameters in the code. Short descriptions of each parameters are given in the comments.

## Parameters of radio astronomy data to keep in mind

There are 2 receiver types:

* DSPZ (mainly used at UTR-2 & URAN with data files format **.jds**)
* ADR (Advanced Digital Receiver, mainly used at GURT with **.adr** data files extensions).

Both have similar structure but different format, so there are 2 corresponding types of scripts.

DSPZ & ADR receivers can record data in 3 main data types:

* auto-spectra (1 or 2 channels)
* cross-spectra (2 channels of auto-spectra + real & imaginary parts of cross-spectra)
* waveform data (1 or 2 channels).

Connection of antennas to receiver channels

* At UTR-2 channel A typically received signals from NS arm and the B channel from W arm of the antenna array, but there could be any other configurations like separate sections of the telescopes etc.

* At URAN-2 channels A & B were typically connected to 2 perpendicular linear polarizations of dipole subarray.

* At GURT for single subarray observations channels A & B were connected to 2 perpendicular linear polarizations of dipole subarray. For interferometer observations channels A & B were connected to the same linear polarizations of 2 dipole subarrays.

Receivers can work with an external clock generator which provides ADC samplig rate. The sampling rate can be adjusted. Typical sample rates used:

* **66 MHz** clock frequency provides 33 MHz band of receiver (usual at UTR-2 and URAN for DSPZ)
* **160 MHz** clock frequency provides 80 MHz band of receiver (usual at GURT fo ADR)
* **33 MHz** clock frequency provides 16.5 MHz band of receiver (sometimes used at UTR-2 to record waveform data to save data rate and record signal in 2-nd Niquist zone **16.5-33.0 MHz** where UTR-2 has maximal sensitivity).

Usually receivers store data into 2GB files consequently, but ADR receiver can save data into a continuous **.adr** file of any length. Each file has a 1024 byte header where parameters of the receiver and observations are stored.

### Calibration data for UTR-2

There are 2 main calibration goals to calibrate data:

* by noise level (amplitude),

* by phase difference in 2 receiver channels.

The typical calibration process includes switching the radio telescope to calibration mode, e.g. automatic connection of a reference noise generator (RNG) to an amplifier and splitter which distributes the noise signal among the 12 telescope sections outputs. The amplifier is an analogue of the 1 stage UTR-2 antenna amplifier and is used in the calibration scheme to take into account the 1st stage amplifiers in the antenna array which are not subjected to calibration. Operator attaches reference attenuators of fifferent values between the RNG and the splitter, so the calibration files can be recoreded. The most detailed claibration included values from 36 dB to 0 dB (direct connection without attenuator) with 2 dB step, but each observer had its own calibration algorithm. Also the self-noise mode was used, when instead of the RNG the open-ended high-value attenuator was attached. The self-noise mode emulated the noise of the radio telescope system itself when no external noise is received.

With such a clibration dataset we can:

* calibrate the linearity of the noise levels in the telecope (mixture of the external noise and the internal noise of the system)

* calibrate phase between 2 channels as the same noise from the RNG was splitted to all sections of the telescope, e.g. the NS and W arms as well as A and B receiver channels respectively.

* possibly make an absolute measurements assuming we know exactly the noise temperature of the noise from RNG and convert the ADC samples or spectra levels to brightness temperatures or flux densities.

## Scripts to visualize radio astronomy data

**Note:** The first step of any data processing is saving the original **spectra** data into long **".dat"** (one per receiver channel data recorded or their combination) files which are convenient for further processing. Such files are also usually used as internediate reults, for example after dispersion delay removing for pulsar processing. Each file contains data of particular type (channel A or channel B or cross-spectra imaginary part or cross-spectra real part or cross-spectra module or cross-spectra phase) of all initial data files. These **".dat"** files are usually supplied with **"timeline.txt"** files which carry time stamps for data points. The 1024 byte header of each **".dat"** file is a copy of the header of the first initial file processed in a bunch. If the time or frequency resolution of data were changed during processing the header will contain the changed values.

 **".dat"** files can be processed with the **script_DAT_reader.py** to make PNG dynamic spectra of the whole observation with spectra averaging in time.

 For **waveform** intermediate data format we use **".wdat"** and **"timeline.wtxt"** formats respectively. Additional info in each sample time is stored in special time format.

### script_ADR_multifolder_reader.py

This script makes **PNG images** of immediate and dynamic spectra for  auto and cross-spectra data from ADR. Also it can convert these data into **".dat"** format for further processing. It is convenient to analyze the observations data. One can indicate the path to a folder with a bunch of observations data in many subfolders. The script will anaylize each subfolder separately and store the images for further analysis by observer. It is a main tool to search for well-visible emissions like solar bursts, Jupiter DAM emission etc.

### script_JDS_multifolder_reader.py

This script performs the same tasks as the previous **script_ADR_multifolder_reader.py** but for auto and cross-spectra data from **DSPZ**.

## Scripts to process pulsed emissions (pulsars and transients)

These scripts and functions specific for pulsar and transients processing are mostly stored in **"package_pulsar_processing"** folder. There is also a folder **"package_pulsar_profile_analysis_gui"** where GUI tool for pulsar and transient spectral data analysis in spectral domain is placed.

### Processing of spectra observations.

Script **script_sp_pulsar_pulses_incoherent_search.py**

**Input:** .jds files of pulsar or transients observations and pulsar name.

**Output:** dedispersed dynamic spectra & time profile of pulses, averaged (integrated) pulse.

### Analysis of pulse profile in frequency domain

**Note: only A channel data is analyzed here**, no data summation or B channel analysis for now.

For the analysis of pulse profile in frequency domain there is a special GUI program **pulsar_profile_analysis_gui_main.py** which is located in the **package_pulsar_profile_analysis_gui** folder. It performs 2 main tasks:

1) makes pulses 1D time profile from spectral data observations by means of unpacking the spectra data, oerforming the incoherent dedispersion and intergrated the data iver frequency to obtain time profile

2) allows to apply median filter to smooth the low-frequency changes of the profile, clip the profile from top and botton, and finally, analyze the full profile and each 1/2, 1/4, 1/8, and 1/16 parts of the profile.

You can perform these tasks consequently or pick only one of them to be executed. As it is a GUI program the interface is more or less self-explanatory. There are multiple ways of the first task, e.g. making time profile of the pulses:

1) You select any number of consequtive .jds spectra data files form single observation (single DM value to be dedispersed) to be processed to make a pulse profile.

2) You can specify the folder with multiple consequtive .jds spectral data files, and these files will be split into consequtive pairs and for each files pair there will be a separate time profile.

3) Processing of the special kind of a database of expected sources in an excel file made of transient survey with UTR-2. Here you can select an excel database list, the actual folder with data sorted into dedicated folders and a folder for temporary files which will be deleted during processing. 
   

### Processing of waveform observations

The main goal of waveform pulsar or transient data processing is and anomalous intense pulse (AIP) or transient pulse (TP) search, coherent dedispersion and analysis. This task solution is now realized for the case of 1 or 2 cahnnels waveform with 33 MHz clock frequency.

1) Analysis of all waveform files in the observation to find the AIPs or TPs themselves and the time of their arrival. The script **script_wf_pulsar_pulses_incoherent_search.py** reads the .jds waveform files converts the data into spectra, makes the incoherent dispersion delay compensation and make dynamic spectra images with integrated over frequency profile to visual search of the pulses.

2) This step is relevant only for 2 channel observations and calibration data saved. Using the data of calibration we obtain the phase difference between 2 receiver channels for further phase calibration. The script **script_wf_calibration_data_analysis.py** taked the folder with calibration data, analyses all the files, builds the amplitude calibration matrix as a png image and saves calibration phases for each level to txt files. User analyses the images and picks one phase clibration txt file for further calibration.

3) Script **script_wf_pulsar_coherent_dispersion_delay_removing.py**

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
