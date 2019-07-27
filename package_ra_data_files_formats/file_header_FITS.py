'''
'''
import numpy as np
from astropy.io import fits

################################################################################

def FileHeaderReaderFITS(foldpath, filename):
    '''
    Reads info from FITS (.fits) data file header, prints to terminal
    all names, dimensions and units of fields, returns nothing
    Input parameters:
        foldpath - path to folder with file
        filename - name of file
    Output parameters:
        no
    '''

    hdul = fits.open(foldpath + filename)
    print ('\n  File: ', filename)
    #hdul.info()

    num_of_groups = len(hdul)
    num_of_fields = np.zeros(num_of_groups, dtype = 'int')
    num_of_column = np.zeros(num_of_groups, dtype = 'int')
    for i in range (num_of_groups):
        num_of_fields[i] = int(hdul.info(0)[i][4])

    for group in range (1, num_of_groups):
        num_of_column[group] = int(len(hdul[group].columns))

    # ******************************************************
    # ***         Reading data from headers              ***
    # ******************************************************

    # Zero header have special format
    print('\n * Header # 0    PRIMARY \n')
    for i in range (len(hdul[0].header)):
        print (' %2i' % i, ' %50s: ' % hdul[0].header.comments[i], hdul[0].header[i])

    # Next headers
    for group in range (1, num_of_groups):
        print ('\n ********************************************************************************** \n')
        print(' * Header # ', group,'   ', hdul.info(0)[group][1],'\n')
        for i in range (num_of_column[group]):
            hdr = hdul[0].header
            cols = hdul[1].columns
            data = hdul[1].data

            if hdul[group].data.field(i).shape == (1,):
                temp_string = hdul[group].data.field(i)[0]
            else:
                temp_string = 'Data dimensions = ' + str(hdul[group].data.field(i).shape)
            print (' %2i' % i, ' %15s' % hdul[group].columns.names[i], ' %10s ' % hdul[group].columns.units[i], temp_string)

            #hdul[group].data.field(i)
            #print (' * %2i' % i, ' %50s: ' % hdul[group].header.comments[i], hdul[group].header[i])
            # print(repr(hdul[group].header)) - representation as it is in file
            # print(list(hdul[group].header.keys())) - prints all keywords in header

    hdul.close()
    print ('\n ********************************************************************************** \n')

################################################################################

if __name__ == '__main__':

    filename = '20190407_094300_BST.fits'
    foldpath = 'DATA/'

    FileHeaderReaderFITS(foldpath, filename)
