import os
import pandas as pd

data_path = ''
excel_file_name = 'TP_corrected_for_VV_2017_June27.xlsx'
excel_sheet_name = 'Лист1'
new_path_part = 'e:/data/'

def xlsx_vvz_pulsar_sources_reader(data_path, excel_file_name, excel_sheet_name, new_path_part):
    """Reads the XLSX database of pulse sources in the survey data, selects the items with file paths,
    corrects these paths to be used on the current pc and checks if these files exist on the PC

    Args:
        data_path (str): path to excel database file
        excel_file_name (str): name of the excel database file
        excel_sheet_name (str): sheet name in the excel files
        new_path_part (str): real path part on this PC to replace the default path in the database

    Returns:
        code_date (python array of str): a code of beam direction and date of observation
        beam (python array of str): the number of beam of UTR-2 radio telescope (5 beam mode)
        source_dm (python array of floats): dispersion measure of the expected source to find
        file_paths (python array of arrays of str): paths to files of the data
    """

    # Normalize and prepare file paths
    new_path_part = os.path.normpath(new_path_part)
    data_path = os.path.normpath(data_path)
    path_to_xlsx_file = os.path.join(data_path, excel_file_name)

    # Read excel file
    dataframe = pd.read_excel(path_to_xlsx_file, sheet_name=excel_sheet_name)

    print('\n  File name:       ', excel_file_name)
    print('  Sheet name:      ', excel_sheet_name)
    print('  Dataframe shape: ', dataframe.shape)

    # Filling the merged cells by the value in the first row of such cells
    dataframe['Code&Date'] = pd.Series(dataframe['Code&Date']).ffill()
    dataframe['Beam'] = pd.Series(dataframe['Beam']).ffill()

    # Selecting lines (rows) fronm correct code&date with indicated paths to files
    # selected_df = dataframe[dataframe['Code&Date'].str.contains('V102')]
    selected_df = dataframe
    selected_df = selected_df[selected_df['Path 1'].notna()]

    # Prepare empty arrays to save items
    code_date = []
    beam = []
    source_dm = []
    file_paths = []

    for i in range (selected_df.shape[0]):
        
        # Replace the initial paths to real data folder path on given PC
        path_01 = os.path.normpath(selected_df.iloc[i]['Path 1'])
        path_02 = os.path.normpath(selected_df.iloc[i]['Path 2'])
        relative_01 = os.path.relpath(path_01, os.path.normpath('f:/Primary_Data/'))
        relative_02 = os.path.relpath(path_02, os.path.normpath('f:/Primary_Data/'))
        path_01 = os.path.join(new_path_part, relative_01)
        path_02 = os.path.join(new_path_part, relative_02)

        # Check if the file paths from the database are real on this PC
        if os.path.isfile(path_01) and os.path.isfile(path_02):

            file_paths.append([path_01, path_02])

            # Saving also code & date, beam and source DM indo into dedicated arrays 
            code_date.append(selected_df.iloc[i]['Code&Date'])
            beam.append(selected_df.iloc[i]['Beam'])
            source_dm.append(float(selected_df.iloc[i]['DM_corr']))
            
        else:
            print(' * File pair ', file_paths[i][0], ' are not fined on the PC, skipped in the list')

    print('\n  Number of file pairs found: ', len(source_dm), '\n')
   
    # for i in range (selected_df.shape[0]):
    #     print(code_date[i], beam[i], source_dm[i], file_paths[i])

    return code_date, beam, source_dm, file_paths


if __name__ == '__main__':

    code_date, beam, source_dm, file_paths = xlsx_vvz_pulsar_sources_reader(data_path, excel_file_name, excel_sheet_name, new_path_part)