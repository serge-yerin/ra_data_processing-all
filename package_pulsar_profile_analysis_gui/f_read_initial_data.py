import numpy as np
import numpy.ma as ma

from package_astronomy.catalogue_pulsar import catalogue_pulsar


def read_and_prepare_data(profile_data, pulsar_name, time_resolution, harmonics_to_show):

    # Getting pulsar parameters from catalogue
    pulsar_ra, pulsar_dec, source_dm, pulsar_period = catalogue_pulsar(pulsar_name)

    # Data frequency resolution, Hz
    frequency_resolution = 1 / (time_resolution * len(profile_data))

    # Calculate pulsar harmonics frequency
    pulsar_frequency = 1 / pulsar_period  # frequency of pulses, Hz

    frequency_limit = (harmonics_to_show + 1.5) * pulsar_frequency

    freq_points_per_harmonic = np.ceil(pulsar_frequency / frequency_resolution).astype(int)
    # n_harmonics = int(np.floor(len(profile_data) / (2 * freq_points_per_harmonic)))
    n_harmonics = harmonics_to_show + 1

    pulsar_harmonics = pulsar_frequency * np.linspace(1, n_harmonics, num=n_harmonics)
    pulsar_harmonics_points = np.ceil(pulsar_harmonics / frequency_resolution).astype(int)
    max_interval = int(freq_points_per_harmonic / 4)

    # print('  Pulsar frequency: ', pulsar_frequency, ' Hz')
    # print('  Frequency resolution: ', frequency_resolution, ' s')
    # print('  Time resolution: ', time_resolution, ' s')
    # print('  Number of points per harmonic: ', freq_points_per_harmonic)
    # print('  Number harmonics to highlight: ', n_harmonics)
    # print('  Interval to search the harmonic: ', max_interval, ' points')

    # Calculating the spectrum
    profile_spectrum = np.power(np.real(np.fft.fft(profile_data[:])), 2)  # calculation of the spectrum
    profile_spectrum = profile_spectrum[0:int(len(profile_spectrum) / 2)]  # delete second part of the spectrum

    frequency_axis = [frequency_resolution * i for i in range(len(profile_spectrum))]

    # Finding the maximal spectrum amplitudes near expected harmonics
    max_harmonics = []
    noise_mean = []
    noise_std = []
    signal_to_noise = []
    for i in range(n_harmonics):
        # Maximal points near expected harmonics
        data_bunch_near_harmonic = profile_spectrum[pulsar_harmonics_points[i] - max_interval:
                                                    pulsar_harmonics_points[i] + max_interval].copy()

        max_near_harmonic = np.max(data_bunch_near_harmonic)
        max_harmonics.append(max_near_harmonic)

        # Masking the maximal value
        data_bunch_near_harmonic_masked = ma.masked_values(data_bunch_near_harmonic, max_near_harmonic, copy=True)

        # Calculating mean and std of noise around harmonic but without it
        current_noise_mean = np.mean(data_bunch_near_harmonic_masked)
        current_noise_std = np.std(data_bunch_near_harmonic_masked)

        noise_mean.append(current_noise_mean)
        noise_std.append(3 * current_noise_std)
        signal_to_noise.append(max_near_harmonic / (current_noise_mean + 3 * current_noise_std))

    # Calculating the limit o vertical axis of the spectrum plot
    spectrum_max = np.max(max_harmonics)

    return profile_data,  frequency_axis, profile_spectrum, spectrum_max, frequency_limit
