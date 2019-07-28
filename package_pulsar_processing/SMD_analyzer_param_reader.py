'''
'''

from package_common_modules.text_manipulations import find_between


def SMD_analyzer_param_reader():
    '''
    Reads parameters of average pulsar pulse analysis from file "script_SMD_analyzer_parameters.py"
    and passes them to the main script "script_SMD_analyzer.py"
    '''

    file = open('script_SMD_analyzer_parameters.py', 'r')

    print ('\n  * Parameters of analysis: \n')

    for line in file:
        if not line.startswith('#') and len(line)>1:

            if line.startswith('path ='):
                path = find_between(line.split()[2], "'", "'")
                print (' File path:  ', path, '\n')

            if line.startswith('filename ='):
                filename = find_between(line.split()[2], "'", "'")
                print (' File name:  ', filename, '\n')

            if line.startswith('no_of_DM_steps ='):
                no_of_DM_steps = int(line.split()[2])
                print (' Number of DM analysis steps =        ', no_of_DM_steps)

            if line.startswith('DM_var_step ='):
                DM_var_step = float(line.split()[2])
                print (' Step of DM analysis =                ', DM_var_step)

            if line.startswith('save_intermediate_data ='):
                save_intermediate_data = int(line.split()[2])
                print (' Save intermediate data?              ', save_intermediate_data)

            if line.startswith('AverageChannelNumber ='):
                AverageChannelNumber = int(line.split()[2])
                print (' Number of channels to average =      ', AverageChannelNumber)

            if line.startswith('AverageTPointsNumber ='):
                AverageTPointsNumber = int(line.split()[2])
                print (' Number of time points to average =   ', AverageTPointsNumber)

            if line.startswith('frequency_band_cut ='):
                frequency_band_cut = int(line.split()[2])
                print (' Make cuts of frequency bands?        ', frequency_band_cut)

            if line.startswith('specify_freq_range ='):
                specify_freq_range = int(line.split()[2])
                print (' Specify particular frequency range?  ', specify_freq_range)



            if line.startswith('frequency_cuts ='):
                temp = find_between(line, '[', ']')
                frequency_cuts = []
                for i in range (len(temp.split(','))):
                    frequency_cuts.append(float(temp.split(',')[i]))
                print (' Frequencies to cut the range         ', frequency_cuts)

            if line.startswith('colormap ='):
                colormap = find_between(line.split()[2], "'", "'")
                print (' Color map =                          ', colormap)
            if line.startswith('customDPI ='):
                customDPI = int(line.split()[2])
                print (' DPI of plots =                       ', customDPI)
            if line.startswith('freqStartArray ='):
                freqStartArray = float(line.split()[2])
                print (' Lowest frequency of the band =       ', freqStartArray)
            if line.startswith('freqStopArray ='):
                freqStopArray = float(line.split()[2])
                print (' Highest frequency of the band =      ', freqStopArray)
            if line.startswith('DM ='):
                DM = float(line.split()[2])
                print (' Initial Dispersion measure =         ', DM, ' pc / cm3 \n')


    return filename, path, DM, no_of_DM_steps, DM_var_step, save_intermediate_data, AverageChannelNumber, AverageTPointsNumber, frequency_band_cut, specify_freq_range, frequency_cuts, colormap, customDPI, freqStartArray, freqStopArray
