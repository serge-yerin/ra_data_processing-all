'''
'''
################################################################################

def catalogue_sources(source_name):

    class Source:
        def __init__(self, unique_name, c3C_name, c4C_name, ra, dec):
            self.c3C_name = c3C_name
            self.c4C_name = c4C_name
            self.unique_name = unique_name
            self.ra = ra
            self.dec = dec

    Cas_A = Source('Cas A','3C461','4C 58.40', '23h23m24.0s',    '+58d48m54.0s')
    Syg_A = Source('Syg A','3C405','4C 40.40', '19h59m28.356s',  '+40d44m02.0967s')
    Vir_A = Source('Vir A','3C274','4C 12.45', '12h30m49.423s',  '+12d23m28.0439s')
    Crab  = Source('Crab', '3C144','4C 21.19', '05h34m31.94s',   '+22d00m52.2s')        # Tau A

    sources = [Cas_A, Syg_A, Vir_A, Crab]

    source_ra = 0
    source_dec = 0
    for source in sources:
        if source.c3C_name == source_name or source.c4C_name == source_name or source.unique_name == source_name:
            source_ra = source.ra
            source_dec = source.dec

    return source_ra, source_dec

################################################################################
################################################################################

if __name__ == '__main__':

    source_ra, source_dec = catalogue_sources('Cas A')

    print(' Source coordinates are:', pulsar_ra, pulsar_dec)
