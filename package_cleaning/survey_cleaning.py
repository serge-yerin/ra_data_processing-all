import numpy as np
from package_cleaning.erov import erov
from package_cleaning.launch_sumthr import launch_sumthr
from package_cleaning.patrol import patrol
#from erov import erov
#from launch_sumthr import launch_sumthr
#from patrol import patrol


def survey_cleaning(imdat):
    
    plotarr = np.copy(imdat)
    wofsg, nofs = imdat.shape

    s_sk = np.zeros(wofsg)
    m_sk = np.zeros(wofsg)
    for j in range(wofsg):
        op = imdat[j, ...]
        op, st, mt = erov(op)
        s_sk[j] = st
        m_sk[j] = mt
        plotarr[j, ...] = (op - mt) / mt

    
    op = s_sk / m_sk
    op, st, mt = erov(op)
    w = np.where(abs(op - mt) < st*4.)[0]
    if w.any():   # if w:
        med=np.median(imdat[w, ...])
    else:
        med = 0
        
    p = np.ones((wofsg, nofs), dtype=int)
    
    p = launch_sumthr(plotarr, p, med)
    
    imdat=plotarr
    
    imdat, med, p, s_sk, m_sk = patrol(imdat, med, p, s_sk, m_sk)
    
    return imdat