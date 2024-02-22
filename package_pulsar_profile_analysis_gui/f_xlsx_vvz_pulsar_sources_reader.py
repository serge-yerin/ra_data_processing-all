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

    # print('\n\n')
    # print(dataframe.loc[[10]])

    print('\n\n')

    # Filling the merged cells by the value in the first row of such cells
    dataframe['Code&Date'] = pd.Series(dataframe['Code&Date']).fillna(method='ffill')
    dataframe['Beam'] = pd.Series(dataframe['Beam']).fillna(method='ffill')

    print(dataframe.head(40))

    print('\n\n')

    # Selecting lines (rows) fronm correct code&date with indicated paths to files
    selected_df = dataframe[dataframe['Code&Date'].str.contains('V102')]
    selected_df = selected_df[selected_df['Path 1'].notna()]
    print (selected_df)

    code_date = []
    beam = []
    source_dm = []
    file_paths = []

    for i in range (selected_df.shape[0]):
        code_date.append(selected_df.iloc[i]['Code&Date'])
        beam.append(selected_df.iloc[i]['Beam'])
        source_dm.append(selected_df.iloc[i]['DM_corr'])
        file_paths.append([selected_df.iloc[i]['Path 1'], selected_df.iloc[i]['Path 2']])

    for i in range (selected_df.shape[0]):
        print(code_date[i], beam[i], source_dm[i], file_paths[i])

    return


if __name__ == '__main__':

    source_list = xlsx_vvz_pulsar_sources_reader(data_path, excel_file_name, excel_sheet_name)