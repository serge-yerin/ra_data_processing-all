import numpy as np

def erov(op):
    count = op.size
    m_in = np.arange(count)
    m = op
    sr = np.mean(m)
    while True:
        srkv = np.std(m)
        count_pr = count
        sr_pr = sr
        m = m*(abs(m - sr) <= srkv * 3.)
        m_in = np.where(m != 0)[0]
        count = m_in.size
        if m_in.any():  # if m_in:
            m = m[m_in]
            sr = np.mean(m)
            ster = np.std(m)
        else:
            sr=0.
            ster=0.
            return op, sr, ster
        
        if (abs(sr_pr/sr-1) < 1e-5) or (count_pr == count):
            break
    
    return op, sr, ster
