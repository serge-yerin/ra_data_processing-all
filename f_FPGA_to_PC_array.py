'''
'''

import numpy as np        

def FPGAtoPCarrayDSP (FPGAdata, NAvr):
    '''
    FPGAtoPC Transforms FPGA array data format to ordinary PC numbers
    Input parameters:
        FPGAdata - array of values in FPGA format
        NAvr - number of averages apectra to normalize the data
    Output parameters:
        PCdata - result arra in ordinary PC format (numpy float64 array)
    '''
    FPGAdata = np.uint64(FPGAdata)
    B = np.uint64(int('00000000000000000000000000011111', 2)) 
    expn = np.uint64(np.bitwise_and (FPGAdata, B))                     # exponent 
    A = np.uint64(int('11111111111111111111111111000000', 2))
    mant = np.uint32(np.bitwise_and (FPGAdata, A))
    C = np.uint64(int('00000000000000000000000000100000', 2))
    sign = - np.float64(np.bitwise_and (FPGAdata, C)/16)+1.0
    C0 = np.empty_like(mant)
    C0 = np.uint64(C0)
    C0[:] = np.uint64(1)
    C1 = np.left_shift(C0, (expn+14)) 
    C1 = np.float64(C1)
    PCdata = np.float64(sign * np.float64(np.float32(mant) / C1 / NAvr))
    del A, B, 
    return PCdata


# *** FPGAtoPC Transforms FPGA array data format to ordinary PC numbers ***    
def FPGAtoPCarrayADR (FPGAdata, NAvr):
    temp_float = np.uint32(FPGAdata)  
    temp = np.int64(FPGAdata)         
    A = np.int64(int('11111111111111111111111111000000', 2)) 
    temp_mantissa = np.int32(np.bitwise_and (temp, A))
    temp_mantissa = np.float32(temp_mantissa)/64
    B = np.uint32(int('00000000000000000000000000111111', 2))   
    temp_exponent = np.uint8(np.bitwise_and (temp_float, B))
    C0 = np.empty_like(temp_mantissa)
    C0 = np.uint64(C0)
    C0[:] = np.uint64(1)
    C1 = np.left_shift(C0, (temp_exponent+8)) # ! It must be "7" or "10" but "8" works for me
    C1 = np.float64(C1)
    PCdata = np.float64(temp_mantissa / C1 / NAvr)
    del A, B, C0, C1, temp_exponent
    return PCdata