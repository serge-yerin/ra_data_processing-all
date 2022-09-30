'''
'''
import numpy as np
from package_ra_data_files_formats.read_file_header_adr import FileHeaderReaderADR

################################################################################

def check_if_ADR_files_of_equal_parameters(folder_path, file_list):
    '''
    The function checks if main parameters of the ADR files are equal (are they from the same observation)
    Input parameters:
        folder_path - path to folder with files
        file_list - list of files in the folder to check
    Output parameters:
        equal_or_not - "1" if files have equal parameters, "0" - otherwise
    '''
    df_system_name_list = []
    df_obs_place_list = []
    df_description_list = []
    ADRmode_list = []
    sumDifMode_list = []
    TimeRes_list = []
    FFT_Size_list = []
    SLine_list = []
    Width_list = []
    BlockSize_list = []

    for file_no in range (len(file_list)):
        filepath = folder_path + file_list[file_no]
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
            F_ADC, df_creation_timeUTC, ReceiverMode, ADRmode,
            sumDifMode, NAvr, TimeRes, fmin, fmax, df, frequency,
            FFT_Size, SLine, Width, BlockSize] = FileHeaderReaderADR(filepath, 0, 0)

        df_system_name_list.append(df_system_name)
        df_obs_place_list.append(df_obs_place)
        df_description_list.append(df_description)
        ADRmode_list.append(ADRmode)
        sumDifMode_list.append(sumDifMode)
        TimeRes_list.append(TimeRes)
        FFT_Size_list.append(FFT_Size)
        SLine_list.append(SLine)
        Width_list.append(Width)
        BlockSize_list.append(BlockSize)

    i = 0
    if df_system_name_list.count(df_system_name_list[0]) == len(df_system_name_list):  i = i + 1
    if df_obs_place_list.count(df_obs_place_list[0]) == len(df_obs_place_list):  i = i + 1
    if df_description_list.count(df_description_list[0]) == len(df_description_list):  i = i + 1
    if ADRmode_list.count(ADRmode_list[0]) == len(ADRmode_list):  i = i + 1
    if sumDifMode_list.count(sumDifMode_list[0]) == len(sumDifMode_list):  i = i + 1
    if TimeRes_list.count(TimeRes_list[0]) == len(TimeRes_list):  i = i + 1
    if FFT_Size_list.count(FFT_Size_list[0]) == len(FFT_Size_list):  i = i + 1
    if SLine_list.count(SLine_list[0]) == len(SLine_list):  i = i + 1
    if Width_list.count(Width_list[0]) == len(Width_list):  i = i + 1
    if BlockSize_list.count(BlockSize_list[0]) == len(BlockSize_list):  i = i + 1

    if i == 10:
        equal_or_not = 1
        print('   OK: all files have the same parameters!')
    else:
        equal_or_not = 0
        print('\n **********************************************************\n !!!   WARNING: Parameters of files in folder differ    !!! \n **********************************************************')
        print('\n   * Check letteral parameters of the files in list: \n')
        for file_no in range (len(file_list)):
            print('   ',  file_no+1 ,') ', df_system_name_list[file_no], '  ', df_obs_place_list[file_no], '  ', df_description_list[file_no])
        print('\n   * Check numerical parameters of the files in list: \n')
        print('   No  ADR mode  Sum/Diff  Time res.   FFT size   Start line   Width  Block size\n')
        for file_no in range (len(file_list)):
            #print('   ',  file_no+1 ,')    ', str(ADRmode_list[file_no]), '     ',str(sumDifMode_list[file_no]), '   ',np.round(TimeRes_list[file_no], 6), '   ', FFT_Size_list[file_no], '  ', SLine_list[file_no], Width_list[file_no], ' ', BlockSize_list[file_no])
            print('  {:0>4d}'.format(file_no+1),'   {:0>1d}'.format(ADRmode_list[file_no]), '        {}'.format(sumDifMode_list[file_no]), '      {:.6f}'.format(np.round(TimeRes_list[file_no], 6)), '     {:5.0f}'.format(FFT_Size_list[file_no]), '       {:1.0f}'.format(SLine_list[file_no]), '         {:1.0f}'.format(Width_list[file_no]), '     {:6.0f}'.format(BlockSize_list[file_no]))



    return equal_or_not

################################################################################

################################################################################

if __name__ == '__main__':

    folder_path = 'DATA/'
    file_list = ['A170712_160219.adr', 'File 10 2048FFT A 100 ms 141119_164450.adr']
    equal_or_not = chaeck_if_ADR_files_of_equal_parameters(folder_path, file_list)
