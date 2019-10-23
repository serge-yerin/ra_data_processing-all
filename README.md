# "ra_data_processing-all" repository
Scripts and functions for visualizing and processing of radio astronomy data,
mainly from Ukrainian low-frequency radio telescopes UTR-2, URAN, GURT.

# Scripts to read and visualize radio astronomy data

## script_ADR_reader

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
