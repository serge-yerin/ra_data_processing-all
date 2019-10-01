'''
'''
################################################################################

def catalogue_sources(name):
    name = name.upper()
    if   '3C461' in name or 'CAS A' in name or '4C 58.40' in name: ra = '23h23m24.0s';   dec = '+58d48m54.0s'
    elif '3C405' in name or 'SYG A' in name or '4C 40.40' in name: ra = '19h59m28.356s'; dec = '+40d44m02.0967s'
    elif '3C274' in name or 'VIR A' in name or '4C 12.45' in name: ra = '12h30m49.423s'; dec = '+12d23m28.0439s'
    elif '3C144' in name or 'CRAB'  in name or '4C 21.19' in name: ra = '05h34m31.94s';  dec = '+22d00m52.2s'

    else: print('   !!! Source not found !!!')
    return ra, dec

################################################################################
################################################################################

if __name__ == '__main__':

    source_ra, source_dec = catalogue_sources('3C405')

    print(' Source coordinates are:', source_ra, source_dec)
