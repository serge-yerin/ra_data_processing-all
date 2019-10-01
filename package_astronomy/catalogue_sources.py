'''
'''
################################################################################

def catalogue_sources(source_name):
    source_name = source_name.upper()
    if   ('CAS A' or '3C461' or '4C 58.40') in source_name: source_ra = '23h23m24.0s';   source_dec = '+58d48m54.0s'
    elif ('SYG A' or '3C405' or '4C 40.40') in source_name: source_ra = '19h59m28.356s'; source_dec = '+40d44m02.0967s'
    elif ('VIR A' or '3C274' or '4C 12.45') in source_name: source_ra = '12h30m49.423s'; source_dec = '+12d23m28.0439s'
    elif ('CRAB'  or '3C144' or '4C 21.19') in source_name: source_ra = '05h34m31.94s';  source_dec = '+22d00m52.2s'
    return source_ra, source_dec

################################################################################
################################################################################

if __name__ == '__main__':

    source_ra, source_dec = catalogue_sources('Cas A')

    print(' Source coordinates are:', source_ra, source_dec)
