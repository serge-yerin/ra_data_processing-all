'''
'''

import numpy as np
from package_pulsar_processing.pulsar_DM_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes
from package_pulsar_processing.pulsar_DM_shift_calculation_aver_pulse import pulsar_DM_shift_calculation_aver_pulse

def pulsar_DM_variation(array, no_of_DM_steps, FFTsize, fmin, fmax, df, TimeRes, pulsarPeriod, samplesPerPeriod, DM, noise_mean, noise_std, begin_index, end_index, DM_var_step, roll_number, save_intermediate_data, customDPI):
    '''
    Variation of DM for average pulsar profile with defined step and number of steps
    '''
    # ***   Preparing matrices for variation of DM value   ***
    profiles_varDM = np.zeros((no_of_DM_steps, samplesPerPeriod))
    DM_vector = np.zeros((no_of_DM_steps))


    # ***   Preparing the vector of DMs to calculate profiles   ***
    for step in range (no_of_DM_steps):
        DM_vector[step] = DM + ((step - int(no_of_DM_steps/2)) * DM_var_step)

    # ***   Step by step calculate profiles for each DM value as in the main program   ***
    for step in range (no_of_DM_steps):

        # Preparing matrices
        matrix = np.zeros((FFTsize, samplesPerPeriod))
        matrix[:,:] = array[:,:]

        # DM compensation
        shiftPar = pulsar_DM_shift_calculation_aver_pulse(FFTsize, fmin, fmax, df, TimeRes, DM_vector[step], pulsarPeriod)
        matrix = pulsar_DM_compensation_with_indices_changes (matrix, shiftPar)

        for i in range (FFTsize):
            matrix[i,:] = matrix[i,:] - np.mean(matrix[i, begin_index : end_index])

        # Calcultation of integrated profile
        integrated_profile = np.sum(matrix, axis = 0)


        integrated_profile = (integrated_profile - noise_mean) / noise_std

        # Adding the calcultaed average profile to the matrix of profiles
        profiles_varDM[step, :] = integrated_profile


    # ***   Rolling to central position of pulse the whole matrix   ***
    profiles_varDM = np.roll(profiles_varDM, roll_number)


    return profiles_varDM, DM_vector
