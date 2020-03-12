from package_cleaning.erov import erov
#from erov import erov
import numpy as np
from package_cleaning.sumthr import sumthr
#from sumthr import sumthr


def launch_sumthr(x, p, med):
    # clean rows and columns separately
    print('in:')
    print(x.shape)
    x = np.transpose(x)
    p = np.transpose(p)
    print('proc:')
    print(x.shape)
    
    nt, nf = x.shape
    p1 = np.copy(p)
    p2 = np.copy(p)
    
    # columns  - VERTICAL
    M = [256]
    # M = [2, 8, 16, 128, 256]
    nm = len(M)
    thr = np.zeros(nm)
    for i in range(nm):
        thr[i] = 10./(1.5^(np.log2(M[i])))    
    
    for i in range(nt):
        op, sx, mx = erov(x[i, ...])
        y = p2[i, ...]
        xx=((x[i, ...]) - mx) / sx
        for j in range(nm):
            out = sumthr(xx, M[j], thr[j], y)
            p2[i, ...]=out

    # rows  - HORIZONTAL
    # M = [1, 2, 4, 8, 64]
    M = [64]
    nm = len(M)
    thr = np.zeros(nm)
    for i in range(nm):
        thr[i] = 10./(1.5^(np.log2(M[i])))   
    
    for i in range(nf):
        op, sx, mx = erov(x[..., i])
        y = p1[..., i]
        xx=((x[..., i]) - mx) / sx
        for j in range(nm):
            out = sumthr(xx, M[j], thr[j], y)
            p1[..., i] = out
    
    p = p1 * p2
    w = np.where(p == 0)[0]
    if w:
        x[w] = med

    x = np.transpose(x)
    p = np.transpose(p)
    
    print('out:') 
    print(x.shape)
    print(p.shape)
    return p
