'''
'''

import numpy as np
from package_pulsar_processing.pulsar_DM_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes
from package_pulsar_processing.pulsar_DM_shift_calculation_aver_pulse import pulsar_DM_shift_calculation_aver_pulse

def pulsar_DM_variation(array, no_of_DM_steps, frequencyList0, FFTsize, fmin, fmax, df, TimeRes, pulsarPeriod, samplesPerPeriod, DM, filename, AverageChannelNumber, time_points, noise_mean, noise_std, beginIndex, endIndex, DM_var_step, roll_number, save_intermediate_data, customDPI):
    '''
    Variation of DM for average pulsar profile with defined step and number of steps
    '''
    # ***   Preparing matrices for variation of DM value   ***
    profiles_varDM = np.zeros((no_of_DM_steps, time_points))
    DM_vector = np.zeros((no_of_DM_steps))

    # ***   Rolling to central position of pulse the whole matrix   ***
    for i in range (FFTsize):
        array[:,i] = np.roll(array[:,i], roll_number)

    # ***   Preparing the vector of DMs to calculate profiles   ***
    for step in range (no_of_DM_steps):
        DM_vector[step] = DM + ((step - int(no_of_DM_steps/2)) * DM_var_step)

    # ***   Step by step calculate profiles for each DM value as in the main program   ***
    for step in range (no_of_DM_steps):
        # Preparing matrices
        inter_matrix = np.zeros((FFTsize, samplesPerPeriod))
        inter_matrix[:,:] = array.transpose()[:,:]
        # DM compensation
        shiftPar = pulsar_DM_shift_calculation_aver_pulse(FFTsize, fmin, fmax, df, TimeRes, DM_vector[step], pulsarPeriod)
        matrix = pulsar_DM_compensation_with_indices_changes (inter_matrix, shiftPar)


        del inter_matrix
        # Averaging in frequency

        #reducedMatrix = np.array([[0.0 for col in range(samplesPerPeriod)] for row in range(int(FFTsize/AverageChannelNumber))])
        #for i in range (int(FFTsize/AverageChannelNumber)):
        #    for j in range (samplesPerPeriod):
        #        reducedMatrix[i, j] = sum(matrix[i*AverageChannelNumber : (i+1)*AverageChannelNumber, j])
        #frequencyList1 = frequencyList0[::AverageChannelNumber]

        #freq_channels, time_points = reducedMatrix.shape
        #integrProfile = np.array([])
        #integrProfile = (np.sum(matrix, axis = 0))

        for i in range (freq_channels):
            matrix[i,:] = matrix[i,:] - np.mean(matrix[i, beginIndex:endIndex])
        # Calcultation of integrated profile
        integrProfile = np.array([])
        integrProfile = (np.sum(matrix, axis = 0))
        integrProfile = (integrProfile - noise_mean)/noise_std
        # Adding the calcultaed average profile to the matrix of profiles
        profiles_varDM[step, :] = integrProfile

    return profiles_varDM, DM_vector
