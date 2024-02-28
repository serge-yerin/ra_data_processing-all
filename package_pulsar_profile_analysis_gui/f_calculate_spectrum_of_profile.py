import numpy as np


def calculate_spectrum_of_profile(profile_data, time_resolution):

    # Data frequency resolution, Hz
    frequency_resolution = 1 / (time_resolution * len(profile_data))

    # Calculating the spectrum
    profile_spectrum = np.power(np.real(np.fft.fft(profile_data[:])), 2)  # calculation of the spectrum
    profile_spectrum = profile_spectrum[0:int(len(profile_spectrum) / 2)]  # delete second part of the spectrum
    profile_spectrum[0] = 0

    frequency_axis = [frequency_resolution * i for i in range(len(profile_spectrum))]

    # Calculating the limit of vertical axis of the spectrum plot
    spectrum_max = np.max(profile_spectrum)

    return frequency_axis, profile_spectrum, spectrum_max
