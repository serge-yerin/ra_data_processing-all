'''
'''
import numpy as np
import matplotlib.pyplot as plt
import pylab
import math
import time


def clean_lines_of_pixels(array, num_of_iterations, theshold_sigm, min_line_length):

    line_len = 1

    startTime = time.time()
    previousTime = startTime

    # Preparing mask array for all iterations
    mask_full = np.zeros_like(array, dtype = bool) # mask for cleaning the data

    # Making numpy array able to be masked
    array = np.ma.array(array, mask = False)

    no_of_lines, no_of_columns = array.shape

    for iter in range(num_of_iterations):
        print ('\n * Iteration # ', iter+1, ' of ', num_of_iterations)
        print (' ****************************************************************** \n')

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

        # Preparing mask array for current iteration
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
        print ('\n  *** Making the mask took                    ', round((nowTime - previousTime), 2), 'seconds \n')
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


        '''
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
        '''

        mask_full = np.logical_xor(mask_full, mask_result)


    return array, mask_full, cleaned_pixels_num
