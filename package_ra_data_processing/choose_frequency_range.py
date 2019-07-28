'''
'''

def chooseFreqRange (frequencyList, matrix, freqStart, freqStop, FFTsize, fmin, fmax):
    '''
    Cut from array of data the range of needed frequencies
    '''
    num_freq = len(frequencyList)
    if (frequencyList[0]<freqStart<frequencyList[num_freq-1]) and (frequencyList[0]<freqStop<frequencyList[num_freq-1]) and (freqStart<freqStop):
        print ('\n  * You have chosen the frequency range', freqStart, '-', freqStop, 'MHz')
        A = []
        B = []
        for i in range (len(frequencyList)):
            A.append(abs(frequencyList[i] - freqStart))
            B.append(abs(frequencyList[i] - freqStop))
        ifmin = A.index(min(A))
        ifmax = B.index(min(B))
        matrix = matrix[ifmin:ifmax, :]  # Reshaping matrix
        print ('\n    New data matrix shape is: ', matrix.shape)
        
        # Changing other data for further processing
        freqLine = frequencyList[ifmin:ifmax]
        frequencyList = freqLine
        FFTsize = len(frequencyList)
        fmin = frequencyList[0]
        fmax = frequencyList[FFTsize-1]
        
        del A, B, freqLine, ifmin, ifmax, num_freq
    else:
        print ('  !!! Error of frequency limits !!! \n    Continue processing the whole array')

    return frequencyList, matrix, FFTsize, fmin, fmax
