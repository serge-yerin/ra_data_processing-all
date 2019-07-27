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
