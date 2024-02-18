import os
import pandas as pd

data_path = ''
excel_file_name = 'TP_corrected_for_VV_2017_June27.xlsx'
excel_sheet_name = 'Лист1'

def xlsx_vvz_pulsar_sources_reader(data_path, excel_file_name, excel_sheet_name):

    data_path = os.path.normpath(data_path)
    path_to_xlsx_file = os.path.join(data_path, excel_file_name)

    dataframe = pd.read_excel(path_to_xlsx_file, sheet_name=excel_sheet_name)

    print('\n  File name:       ', excel_file_name)
    print('  Sheet name:      ', excel_sheet_name)
    print('  Dataframe shape: ', dataframe.shape)
    print('\n  Keys in table:')
    for key in dataframe.keys():
        print('   -', key)

    print('\n\n')
    print(dataframe.loc[[10]])

    return


if __name__ == '__main__':

    source_list = xlsx_vvz_pulsar_sources_reader(data_path, excel_file_name, excel_sheet_name)