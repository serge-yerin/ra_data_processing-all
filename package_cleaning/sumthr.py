import numpy as np


def sumthr(x, M, thr, y):
    # x - input 1D array
    # M - size of sliding window
    # thr - specified threshold for average of sequence size M
    # y - previous mask of bad pixels (1=good, 0=bad)
    
    w = np.where(y == 1)[0]
    if  not w[0]: 
        return
    
    xx = x[w]
    nxx = len(xx)
    if nxx < M:
        return
    
    xxa = np.zeros(nxx - M + 1)
    for i in range(M):
        xxa += xx[i:]
    
    p = np.ones((nxx,), dtype=int)
    wa = np.where(xxa > thr*M)[0]
    if wa:
        for i in range(M):
            p[wa + i] = 0
    
    y[w] = p
    return x, M, thr, y
