
import numpy as np
from package_pulsar_processing.pulsar_DM_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes
from package_pulsar_processing.pulsar_dm_shift_calculation_aver_pulse import pulsar_dm_shift_calculation_aver_pulse


def pulsar_DM_variation(array, no_of_dm_steps, fft_size, fmin, fmax, df, time_res, pulsar_period, samples_per_period,
                        pulsar_dm,  noise_mean, noise_std, begin_index, end_index, dm_var_step, roll_number):
    """
    Variation of DM for average pulsar profile with defined step and number of steps
    """
    # ***   Preparing matrices for variation of DM value   ***
    profiles_var_dm = np.zeros((no_of_dm_steps, samples_per_period))
    dm_vector = np.zeros((no_of_dm_steps))

    #  Preparing the vector of DMs to calculate profiles
    for step in range(no_of_dm_steps):
        dm_vector[step] = pulsar_dm + ((step - int(no_of_dm_steps/2)) * dm_var_step)

    # ***   Step by step calculate profiles for each DM value as in the main program   ***
    for step in range(no_of_dm_steps):

        # Preparing matrices
        matrix = np.zeros((fft_size, samples_per_period))
        matrix[:, :] = array[:, :]

        # DM compensation
        shift_param = pulsar_dm_shift_calculation_aver_pulse(fft_size, fmin, fmax, df, time_res,
                                                             dm_vector[step], pulsar_period)
        matrix = pulsar_DM_compensation_with_indices_changes(matrix, shift_param)

        for i in range(fft_size):
            matrix[i, :] = matrix[i, :] - np.mean(matrix[i, begin_index: end_index])

        # Calculation of integrated profile
        integrated_profile = np.sum(matrix, axis=0)

        integrated_profile = (integrated_profile - noise_mean) / noise_std

        # Adding the calculated average profile to the matrix of profiles
        profiles_var_dm[step, :] = integrated_profile

    #  Rolling to central position of pulse the whole matrix
    profiles_var_dm = np.roll(profiles_var_dm, roll_number)

    return profiles_var_dm, dm_vector
