# Python3
Software_version = '2020.06.24'

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Directory of files to be analyzed:
directory = 'DATA/' #'/media/server2a/PSR_2020.01/B0950p08_29_Jan_2020_Clk_33_WF_NS1ch_EW2ch_1beam/' #'/media/server2a/PSR_2020.01/B0740p6620_29_Jan_2020_Clk_33_WF_NS1ch_EW2ch_1beam/'  #

pulsar_name = 'B0809+74' # 'B1919+21' # 'B0950+08' #'B1133+16' #  'B1604-00' 'B0950+08'

no_of_spectra_to_average = 16   # Number of spectra to average for dynamic spectra (16 - 7.9 ms)


# ###############################################################################
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
from script_JDS_WF_reader  import  jds_wf_simple_reader
from package_pulsar_processing.script_pulsar_single_pulses import pulsar_incoherent_dedispersion
from package_pulsar_processing.script_pulsar_compensated_DAT_reader import pulsar_period_DM_compensated_pics
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader

# ###############################################################################


print('\n\n  * Conversion from wavefrom to spectra... \n\n')
results_files_list = jds_wf_simple_reader(directory, no_of_spectra_to_average, 0, 0, 8, 'Greys', 300, 1, 0, 1)

print('\n\n  * Making dynamic spectra of the initial data... \n\n')

typesOfData = ['chA']

if len(results_files_list) > 1:
    typesOfData.append('chB')

result_folder_name =  directory.split('/')[-2] + '_initial'

ok = DAT_file_reader('', results_files_list[0][:-13], typesOfData, '', result_folder_name,
                    0, 0, 0, -120, -10, 0, 6, 6, 300, 'jet', 0, 0, 0, 20 * 10**(-12),
                    16.5, 33.0, '', '', 16.5, 33.0, [], 0)

#results_files_list = ['E280120_205409.jds_Data_chA.dat']

print('\n\n  *  Dispersion delay removing... \n\n')
dedispersed_data_file_list = []
for i in range (len(results_files_list)):
    dedispersed_data_file_name = pulsar_incoherent_dedispersion('', results_files_list[i], pulsar_name, 512, -0.15, 0.55, 0, 0, 0, 1, 10, 2.8, 0, 0.0, 16.5, 1, 1, 300, 'Greys')
    dedispersed_data_file_list.append(dedispersed_data_file_name)

print('\n\n  *  Making figures of 3 pulsar periods... \n\n')
for dedispersed_data_file_name in dedispersed_data_file_list:
    pulsar_period_DM_compensated_pics('', dedispersed_data_file_name, -0.15, 0.55, -0.2, 3, 3, 500, 'Greys')


#dedispersed_data_file_list = ['B0809+74_DM_5.75066_E280120_205409.jds_Data_chA.dat']

result_folder_name =  directory.split('/')[-2] + '_dedispersed'

print('\n\n  * Making dynamic spectra of the dedispersed data... \n\n')
ok = DAT_file_reader('', dedispersed_data_file_list[0][:-13], typesOfData, '', result_folder_name,
                    0, 0, 0, -120, -10, 0, 6, 6, 300, 'jet', 0, 0, 0, 20 * 10**(-12),
                    16.5, 33.0, '', '', 16.5, 33.0, [], 0)

print('\n\n  *  Pipeline finished successfully! \n\n')
