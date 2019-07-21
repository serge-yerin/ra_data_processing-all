'''
'''
import numpy as np
import matplotlib.pyplot as plt
import pylab
import math
import time

# *** Deleting cahnnels with strong RFI ***
def simple_channel_clean(Data, RFImeanConst):
    '''
    Simplest cleaning of entire frequency channels polluted with RFI
    Input parameters:
        Data -
        RFImeanConst -
    Output parameters:
        Data -
    '''
    StDdata = []
    StDdata = np.std(Data, axis=0)
    for i in range (0, len(Data[0])):
        if StDdata[i] > RFImeanConst * np.mean(StDdata):
            Data[:,i] = np.mean(Data)
    return Data






def array_clean_by_STD_value(array, theshold_sigm):

    startTime = time.time()
    previousTime = startTime

    no_of_lines, no_of_columns = array.shape
    init_sigm = np.std(array)
    init_mean = np.mean(array)

    print ('\n * Simple standard deviation cleaning ')
    print (' ****************************************************************** \n')
    print(' * Array shape:                               ', no_of_lines,' * ', no_of_columns)
    print(' * Initial mean value of array:               ', init_mean)
    print(' * Initial standard deviation value of array: ', init_sigm,'\n')

    #ma.masked_outside(x, -0.3, 0.3)

    array = np.ma.masked_outside(array, init_mean - theshold_sigm * init_sigm, init_mean + theshold_sigm * init_sigm)

    nowTime = time.time()
    print ('\n  *** Masking took                            ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime

    new_mean = np.mean(array)
    new_sigm = np.std(array)

    mask = array.mask.astype(int)
    array.mask = False
    array = array * np.abs(mask - 1) + mask * new_mean
    cleaned_pixels_num = np.sum(mask)

    print(' * New mean value of array:                   ', new_mean)
    print(' * New standard deviation value of array:     ', new_sigm)
    print(' * Number of cleaned pixels:                  ', int(cleaned_pixels_num))
    print(' * In percent to the array dimensions:        ', np.round(100 * (cleaned_pixels_num / (no_of_lines * no_of_columns)), 2),' % \n')

    nowTime = time.time()
    print ('\n  *** Applying mask and printing took        ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime

    return array, cleaned_pixels_num






def array_clean_by_lines_and_STD(array, num_of_iterations, theshold_sigm, min_line_length):
    '''
    # Takes an array and cleans lines and columns of specified lengths where all elements
    # are greater than specified number of STDs of array
    '''

    startTime = time.time()
    previousTime = startTime

    for iter in range(num_of_iterations):
        print ('\n * Iteration # ', iter+1, ' of ', num_of_iterations)
        print (' ****************************************************************** \n')

        no_of_lines, no_of_columns = array.shape
        init_sigm = np.std(array)

        print(' * Array shape:                               ', no_of_lines,' * ', no_of_columns)
        print(' * Initial mean value of array:               ', np.mean(array))
        print(' * Initial standard deviation value of array: ', init_sigm)

        column_len_list = []
        n = no_of_columns
        no_iter_column = np.int(np.floor(math.log(no_of_columns, min_line_length)))
        for i in range (no_iter_column):
            n = int(n / min_line_length)
            column_len_list.append(n)

        line_len_list = []
        n = no_of_lines
        no_iter_lines = np.int(np.floor(math.log(no_of_lines, min_line_length)))
        for i in range (no_iter_lines):
            n = int(n / min_line_length)
            line_len_list.append(n)

        mask = np.zeros_like(array) # mask for cleaning the data

        nowTime = time.time()
        print ('\n  *** Preparation to make mask took           ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime

        # Vertical lines mapping
        #for line_len in column_len_list:
        line_len = 1
        for j in range (no_of_columns):
            for i in range (no_of_lines - line_len * min_line_length):
                if all(array[i : i + line_len * min_line_length, j] > theshold_sigm * init_sigm):
                    mask[i : i + line_len * min_line_length, j] = 1
                if all(array[i : i + line_len * min_line_length, j] < - theshold_sigm * init_sigm):
                    mask[i : i + line_len * min_line_length, j] = 1


        nowTime = time.time()
        print ('\n  *** Half of mask making took                ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime


        # Horizontal lines mapping
        #for line_len in column_len_list:
        for j in range (no_of_lines):
            for i in range (no_of_columns - line_len * min_line_length):
                if all(array[j, i : i + line_len * min_line_length] > theshold_sigm * init_sigm):
                    mask[j, i : i + line_len * min_line_length] = 1
                if all(array[j, i : i + line_len * min_line_length] < - theshold_sigm * init_sigm):
                    mask[j, i : i + line_len * min_line_length] = 1


        nowTime = time.time()
        print ('\n  *** Making the mask took                    ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime

        array = np.ma.array(array, mask = mask)
        mean_new = np.mean(array)
        cleaned_pixels_num = np.sum(mask)

        print(' * New mean value of array:                   ', mean_new)
        print(' * New standard deviation value of array:     ', np.std(array))
        print(' * Number of cleaned pixels:                  ', int(cleaned_pixels_num))
        print(' * In percent to the array dimensions:        ', np.round(100 * (cleaned_pixels_num / (no_of_lines * no_of_columns)), 2),' %')

        nowTime = time.time()
        print ('\n  *** Applying mask and printing took         ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime

        array.mask = False
        array = array * np.abs(mask - 1) + mask * mean_new

        nowTime = time.time()
        print ('\n  *** Cleaning took                           ', round((nowTime - previousTime), 2), 'seconds \n')
        previousTime = nowTime

    return array, cleaned_pixels_num

'''
plt.figure(1, figsize=(10.0, 6.0))
plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
ImA = plt.imshow(mask, aspect='auto', vmin=0, vmax=1, cmap='Greys')
plt.title('Full log initial data', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
plt.ylabel('One dimension', fontsize = 10, fontweight='bold')
plt.xlabel('Second dimensions', fontsize = 10, fontweight='bold')
plt.colorbar()
plt.yticks(fontsize = 8, fontweight = 'bold')
plt.xticks(fontsize = 8, fontweight = 'bold')
pylab.savefig("RFI_mitigation_try"+'/00 - mask.png', bbox_inches='tight', dpi = 300)
plt.close('all')
'''


'''
def pulsar_data_clean(Data):

    Takes an array of data, calculates its standart deviation, then forms a mask of
    data which is bigger than 3*StD.

    StD_data = []
    StD_data = np.std(Data)
    mean_data = np.mean(Data)
    a, b = Data.shape

    print (' Data shape:                    ',  a, b)
    print (' StD of Data:                   ', StD_data)
    print (' Mean of Data is:               ', mean_data)


    cols_mean = np.zeros(a)
    for col in range (a):
        cols_mean[col] = np.mean(Data[col, :])

    rows_mean = np.zeros(b)
    for row in range (b):
        rows_mean[row] = np.mean(Data[:, row])


    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    plt.plot(cols_mean)
    plt.title('Columns mean values', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
    plt.ylabel('column num', fontsize = 10, fontweight='bold')
    plt.xlabel('value', fontsize = 10, fontweight='bold')
    plt.yticks(fontsize = 8, fontweight = 'bold')
    plt.xticks(fontsize = 8, fontweight = 'bold')
    pylab.savefig('PULSAR_single_pulses'+'/03 - Average colums.png', bbox_inches='tight', dpi = 300)
    plt.close('all')


    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    plt.plot(rows_mean)
    plt.title('Rows mean values', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
    plt.ylabel('row num', fontsize = 10, fontweight='bold')
    plt.xlabel('value', fontsize = 10, fontweight='bold')
    plt.yticks(fontsize = 8, fontweight = 'bold')
    plt.xticks(fontsize = 8, fontweight = 'bold')
    pylab.savefig('PULSAR_single_pulses'+'/03 - Average rows.png', bbox_inches='tight', dpi = 300)
    plt.close('all')



    indexes = np.where(rows_mean > 1 * np.mean(rows_mean))
    print(' Indexes = ', indexes)

    for i in indexes:
        Data[:, i] = mean_data #np.min(Data)


    rows_mean = np.zeros(b)
    for row in range (b):
        rows_mean[row] = np.mean(Data[:, row])


    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    plt.plot(rows_mean)
    plt.title('Rows mean values', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
    plt.ylabel('row num', fontsize = 10, fontweight='bold')
    plt.xlabel('value', fontsize = 10, fontweight='bold')
    plt.yticks(fontsize = 8, fontweight = 'bold')
    plt.xticks(fontsize = 8, fontweight = 'bold')
    pylab.savefig('PULSAR_single_pulses'+'/03 - Average rows 2.png', bbox_inches='tight', dpi = 300)
    plt.close('all')


    return Data
'''
def clean_try(array, num_of_iterations, theshold_sigm, min_line_length):

    line_len = 1

    startTime = time.time()
    previousTime = startTime
    array = np.ma.array(array, mask = False)

    for iter in range(num_of_iterations):
        print ('\n * Iteration # ', iter+1, ' of ', num_of_iterations)
        print (' ****************************************************************** \n')

        no_of_lines, no_of_columns = array.shape
        init_sigm = np.std(array)

        print(' * Array shape:                               ', no_of_lines,' * ', no_of_columns)
        print(' * Initial mean value of array:               ', np.mean(array))
        print(' * Initial standard deviation value of array: ', init_sigm)


        nowTime = time.time()
        print ('\n  *** Preparation to make mask took           ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime


        masked_array = np.ma.masked_outside(array, - theshold_sigm * init_sigm, theshold_sigm * init_sigm)
        mask_array = masked_array.mask
        del masked_array

        mask_result = np.zeros_like(mask_array) # mask for cleaning the data

        for j in range (no_of_lines):
            for i in range (no_of_columns - line_len * min_line_length):
                if all(mask_array[j, i : i + line_len * min_line_length] == 1):
                    mask_result[j, i : i + line_len * min_line_length] = 1

        for j in range (no_of_columns):
            for i in range (no_of_lines - line_len * min_line_length):
                if all(mask_array[i : i + line_len * min_line_length, j] == 1):
                    mask_result[i : i + line_len * min_line_length, j] = 1


        nowTime = time.time()
        print ('\n  *** Making the mask took                    ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime


        array = np.ma.array(array, mask = mask_result)
        mean_new = np.mean(array)
        array.mask = False

        array = array * np.abs(mask_result - 1) + mask_result * mean_new
        cleaned_pixels_num = np.sum(mask_result)


        print(' * New mean value of array:                   ', mean_new)
        print(' * New standard deviation value of array:     ', np.std(array))
        print(' * Number of cleaned pixels:                  ', int(cleaned_pixels_num))
        print(' * In percent to the array dimensions:        ', np.round(100 * (cleaned_pixels_num / (no_of_lines * no_of_columns)), 2),' %')


        nowTime = time.time()
        print ('\n  *** Applying mask and printing took         ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime



        plt.figure(1, figsize=(10.0, 6.0))
        plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
        ImA = plt.imshow(mask_result, aspect='auto', vmin=0, vmax=1, cmap='Greys')
        plt.title('Full log initial data', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
        plt.ylabel('One dimension', fontsize = 10, fontweight='bold')
        plt.xlabel('Second dimensions', fontsize = 10, fontweight='bold')
        plt.colorbar()
        plt.yticks(fontsize = 8, fontweight = 'bold')
        plt.xticks(fontsize = 8, fontweight = 'bold')
        pylab.savefig("PULSAR_single_pulses"+'/00_'+str(iter)+' - mask_result.png', bbox_inches='tight', dpi = 300)
        plt.close('all')

        plt.figure(1, figsize=(10.0, 6.0))
        plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
        ImA = plt.imshow(mask_array, aspect='auto', vmin=0, vmax=1, cmap='Greys')
        plt.title('Full log initial data', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
        plt.ylabel('One dimension', fontsize = 10, fontweight='bold')
        plt.xlabel('Second dimensions', fontsize = 10, fontweight='bold')
        plt.colorbar()
        plt.yticks(fontsize = 8, fontweight = 'bold')
        plt.xticks(fontsize = 8, fontweight = 'bold')
        pylab.savefig("PULSAR_single_pulses"+'/00_'+str(iter)+' - mask_sigm.png', bbox_inches='tight', dpi = 300)
        plt.close('all')


        nowTime = time.time()
        print ('\n  *** Making the picture took                 ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime

    return array, cleaned_pixels_num
