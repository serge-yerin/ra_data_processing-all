'''
'''
import numpy as np
        
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
    
    
    
def pulsar_data_clean(Data):
    '''
    Takes an array of data, calculates its standart deviation, then forms a mask of 
    data which is bigger than 3*StD. 
    '''
    
    StD_data = []
    StD_data = np.std(Data)
    mean_data = np.mean(Data)
    a, b = Data.shape 

    print (' Data shape:                    ',  a, b)
    print (' StD of Data:                   ', StD_data)
    print (' Mean of Data is:               ', mean_data)
        
    #cleaning_mask = np.ones_like(Data) # Making cleaning mask filled with ones
    '''
    for col in range (a):
        if np.mean(Data[col, :]) > StD_data:
            cleaning_mask[col, :] = 0.0000001
            print('  yes!')
    for line in range (b):
        if np.mean(Data[:, line]) > mean_data:
            cleaning_mask[:, line] = 0.0000001
            print('  yes!')
    '''
    
    Data[Data > (mean_data + 0.5 * StD_data)] = mean_data
    #cleaning_mask[1000:2000,1000:2000] = 0.0000001
    #plot2D(cleaning_mask, 'Cleaning mask.png', frequencyList0, np.min(cleaning_mask), np.max(cleaning_mask), colormap, 'Cleaning mask', customDPI)
    #Data[:,:] = Data[:,:] * cleaning_mask[:,:]
    
    '''
    #StD_data = np.std(Data, axis=0)
    for i in range (0, len(Data[0])):
        if StDdata[i] > RFImeanConst * np.mean(StDdata): 
            Data[:,i] = np.mean(Data)
    '''
    #del cleaning_mask
    return Data

