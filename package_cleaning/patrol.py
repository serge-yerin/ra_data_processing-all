from package_cleaning.erov import erov
#from erov import erov
import numpy as np


def patrol(imdat, med, p, s_sk, m_sk):
    
#    wofsg = len(imdat)
#    nofs = len(imdat[0])
    
    wofsg, nofs = imdat.shape
    
    l1 = 3.5
    l2 = 4.
    l3 = 2.

#    !P.COLOR=0
#    
#    
#    !P.COLOR=0
#    !P.BACKGROUND=16777215
#    !P.FONT=-1
#    
    
    op = np.divide(s_sk, m_sk)

    op, st, mt = erov(op)
    ispr = mt * (abs(op-mt) > st*l2)
    cle = op * (abs(op-mt) <= st*l2)
    op = ispr + cle
    op = op > (mt - st*l3)
    op = op < (mt + st*l1)
#    testarr = [ispr.index(x) for x in ispr if x > 0]
    testarr = np.where(ispr > 0.)[0]
    
    if testarr:
        pass
        imdat[np.where(ispr > 0.), ...] = med
        p[testarr, ...] = 0
    
    
    op = np.sum(imdat, axis=0) / float(wofsg)
    op, st, mt = erov(op)
    ispr = mt*(abs(op-mt) > st*l2)
    cle = op*(abs(op-mt) <= st*l2)
    op = ispr + cle
    op = op > (mt-st*l3)
    op = op < (mt+st*l1) 
#    testarr = [ispr.index(x) for x in ispr if x > 0]
    testarr = np.where(ispr > 0.)[0]

    if testarr:
        imdat[..., np.where(ispr > 0.)] = med
        p[..., testarr] = 0
    
    return imdat, med, p, s_sk, m_sk
