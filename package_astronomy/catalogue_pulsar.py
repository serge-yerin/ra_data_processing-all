'''
'''
################################################################################

def catalogue_pulsar(pulsar_name):

    class Pulsar:
        def __init__(self, b_name, j_name, ra, dec, DM):
            self.b_name = b_name
            self.j_name = j_name
            self.ra = ra
            self.dec = dec
            self.DM = DM

    J0006p1834 = Pulsar('',         'J0006+1834', '00h06m04.8s',    '+18d34m59.0s',   0)
    B0031m07   = Pulsar('B0031-07', '',           '00h34m08.86s',   '-07d21m53.4s',   0)
    J0051p0423 = Pulsar('',         'J0051+0423', '00h51m30.1s',    '+04d22m49.0s',   0)
    B0053p47   = Pulsar('B0053+47', '',           '00h56m25.51s',   '+47d56m10.5s',   0)
    B0114p58   = Pulsar('B0114+58', '',           '01h17m38.661s',  '+59d14m38.39s',  0)
    J0137p1654 = Pulsar('',         'J0137+1654', '01h37m23.88s',   '+16d54m42.1s',   0)
    B0148m06   = Pulsar('B0148-06', '',           '01h51m22.701s',  '-06d35m02.8s',   0)
    J0152p0948 = Pulsar('',         'J0152+0948', '01h52m23.7s',    '+09d48m10.0s',   0)
    B0301p19   = Pulsar('B0301+19', '',           '03h04m33.115s',  '+19d32m51.4s',   0)
    B0320p39   = Pulsar('B0320+39', '',           '03h23m26.618s',  '+39d44m52.9s',   0)
    B0329p54   = Pulsar('B0329+54', '',           '03h32m59.37s',   '+54d34m44.9s',   0)
    B0355p54   = Pulsar('B0355+54', '',           '03h58m53.7165s', '+54d13m13.727s', 0)
    B0410p69   = Pulsar('B0410+69', '',           '04h15m55.65s',   '+69d54m09.89s',  0)
    B0450p55   = Pulsar('B0450+55', '',           '04h54m07.709s',  '+55d43m41.51s',  0)
    J0459m0210 = Pulsar('',         'J0459-0210', '04h59m51.94s',   '-02d10m06.6s',   0)
    B0531p21   = Pulsar('B0531+21', '',           '05h34m31.97s',   '+22d00m52.06s',  0)
    B0609p37   = Pulsar('B0609+37', '',           '06h12m48.68s',   '+37d21m37.36s',  0)
    B0656p14   = Pulsar('B0656+14', '',           '06h59m48.13s',   '+14d14m21.5s',   0)
    B0655p64   = Pulsar('B0655+64', '',           '07h00m37.0s',    '+64d18m11.0s',   0)
    B0809p74   = Pulsar('B0809+74', '',           '08h14m59.5s',    '+74d29m05.7s',   0)
    B0820p02   = Pulsar('B0820+02', '',           '08h23m09.76s',   '+01d59m12.41s',  0)
    B0823p26   = Pulsar('B0823+26', '',           '08h26m51.383s',  '+26d37m23.79s',  0)
    B0834p06   = Pulsar('B0834+06', '',           '08h37m05.642s',  '+06d10m14.56s',  0)
    B0917p63   = Pulsar('B0917+63', '',           '09h21m14.135s',  '+62d54m13.91s',  0)
    B0919p06   = Pulsar('B0919+06', '',           '09h22m14.025s',  '+06d38m23.3s',   0)
    J0927p23   = Pulsar('',         'J0927+23',   '09h27m37.0s',    '+23d47m00.0s',   0)
    B0940p16   = Pulsar('B0940+16', '',           '09h43m30.1s',    '+16d31m37.0s',   0)
    J0943p22   = Pulsar('',         'J0943+22',   '09h43m25.0s',    '+22d56m12.41s',  0)
    B0943p10   = Pulsar('B0943+10', '',           '09h46m07.31s',   '+09d51m57.3s',   0)
    J0947p27   = Pulsar('',         'J0947+27',   '09h47m22.0s',    '+27d42m00.0s',   0)
    B0950p08   = Pulsar('B0950+08', '',           '09h53m09.31s',   '+07d55m35.75s',  0)
    J1046p0304 = Pulsar('',         'J1046+0304', '10h46m43.23s',   '+03d04m06.9s',   0)
    B1112p50   = Pulsar('B1112+50', '',           '11h15m38.4s',    '+50d30m12.29s',  0)
    B1133p16   = Pulsar('B1133+16', '',           '11h36m03.248s',  '+15d51m04.48s',  0)
    B1237p25   = Pulsar('B1237+25', '',           '12h39m40.46s',   '+24d53m49.29s',  0)
    J1238p21   = Pulsar('',         'J1238+21',   '12h38m23.17s',   '+21d52m11.1s',   0)
    J1246p22   = Pulsar('',         'J1246+22',   '12h46m38.0s',    '+22d53m00.0s',   0)
    J1313p0931 = Pulsar('',         'J1313+0931', '13h13m23.0s',    '+09d31m56.0s',   0)
    B1322p83   = Pulsar('B1322+83', '',           '13h21m46.18s',   '+83d23m38.92s',  0)
    J1503p2111 = Pulsar('',         'J1503+2111', '15h03m54.6s',    '+21d11m09.3s',   0)
    B1508p55   = Pulsar('B1508+55', '',           '15h09m25.6211s', '+55d31m32.331s', 0)


    '''
    ;ra = (15+32/60.+10.36/3600.)*15/!RADEG   ; PSR B1530+27
    ;dec = (27+45/60.+49.4/3600.)/!RADEG
    ;ra = (15+43/60.+30.158/3600.)*15/!RADEG   ; PSR B1540-06
    ;dec = -(6+20/60.+45.25/3600.)/!RADEG
    ;ra = (15+49/60.+40.941/3600.)*15/!RADEG   ; PSR J1549+2113
    ;dec = (21+13/60.+26.9/3600.)/!RADEG
    ;ra = (16+7/60.+12.1/3600.)*15/!RADEG   ; PSR B1604-00
    ;dec = -(0+32/60.+40.83/3600.)/!RADEG
    ;ra = (16+14/60.+40.91/3600.)*15/!RADEG   ; PSR B1612+07
    ;dec = (7+37/60.+31./3600.)/!RADEG
    ;ra = (16+35/60.+25.781/3600.)*15/!RADEG   ; B1633+24
    ;dec = (24+18/60.+47.3/3600.)/!RADEG
    ;ra = (17+40/60.+25.95/3600.)*15/!RADEG   ; PSR J1740+1000
    ;dec = (10+0/60.+6.3/3600.)/!RADEG
    ;ra = (17+41/60.+53.51/3600.)*15/!RADEG   ; PSR J1741+2758
    ;dec = (27+58/60.+9./3600.)/!RADEG

    ;ra = (17+52/60.+58.6896/3600.)*15/!RADEG   ; PSR B1749-28
    ;dec = -(28+6/60.+37.3/3600.)/!RADEG

    ;ra = (18+17/60.+49.79/3600.)*15/!RADEG   ; PSR J1817-0743
    ;dec = -(7+43/60.+18.9/3600.)/!RADEG
    ;ra = (18+25/60.+30.554/3600.)*15/!RADEG   ; PSR B1822-09
    ;dec = -(9+35/60.+22.1/3600.)/!RADEG
    ;ra = (18+32/60.+50.7/3600.)*15/!RADEG   ; PSR J1832+0029
    ;dec = (0+29/60.+27/3600.)/!RADEG
    ;ra = (18+40/60.+44.608/3600.)*15/!RADEG   ; PSR B1839+56
    ;dec = (56+40/60.+55.47/3600.)/!RADEG
    ;ra = (18+48/60.+56.01/3600.)*15/!RADEG   ; PSR J1848+0647
    ;dec = (6+47/60.+31.7/3600.)/!RADEG
    ;ra = (18+51/60.+3.17/3600.)*15/!RADEG   ; PSR J1851-0053
    ;dec = -(0+53/60.+7.3/3600.)/!RADEG
    ;ra = (19+8/60.+17.01/3600.)*15/!RADEG   ; PSR J1908+0734
    ;dec = (7+34/60.+14.36/3600.)/!RADEG
    ;ra = (19+18/60.+23.63/3600.)*15/!RADEG   ; PSR B1916+14
    ;dec = (14+45/60.+6./3600.)/!RADEG
    ;ra = (19+17/60.+48.85/3600.)*15/!RADEG   ; PSR J1917+0834
    ;dec = (8+34/60.+54.63/3600.)/!RADEG
    ;ra = (19+18/60.+7.70/3600.)*15/!RADEG    ; PSR J1918+1541
    ;dec = (15+41/60.+15.2/3600.)/!RADEG
    ;ra = (19+20/60.+38.374/3600.)*15/!RADEG   ; PSR B1918+26
    ;dec = (26+50/60.+38.4/3600.)/!RADEG
    ;ra = (19+21/60.+44.81/3600.)*15/!RADEG  ; PSR B1919+21
    ;dec = (21+53/60.+2.25/3600.)/!RADEG
    ;ra = (19+32/60.+13.95/3600.)*15/!RADEG   ; PSR B1929+10
    ;dec = (10+59/60.+32.42/3600.)/!RADEG
    ;ra = (19+46/60.+53.044/3600.)*15/!RADEG   ; PSR B1944+17
    ;dec = (18+5/60.+41.24/3600.)/!RADEG
    ;ra = (19+54/60.+22.554/3600.)*15/!RADEG   ; PSR B1952+29
    ;dec = (29+23/60.+17.29/3600.)/!RADEG
    ;ra = (20+15/60.+12.7/3600.)*15/!RADEG   ; PSR J2015+2524
    ;dec = (25+24/60.+31.3/3600.)/!RADEG
    ;ra = (20+18/60.+3.92/3600.)*15/!RADEG   ; PSR B2016+28
    ;dec = (28+39/60.+55.2/3600.)/!RADEG
    ;ra = (20+22/60.+37.067/3600.)*15/!RADEG   ; PSR B2020+28
    ;dec = (28+54/60.+23.1/3600.)/!RADEG
    ;ra = (20+22/60.+49.873/3600.)*15/!RADEG   ; PSR B2021+51
    ;dec = (51+54/60.+50.23/3600.)/!RADEG
    ;ra = (21+13/60.+4.39/3600.)*15/!RADEG   ; PSR B2110+27
    ;dec = (27+54/60.+2.29/3600.)/!RADEG
    ;ra = (21+51/60.+10.43/3600.)*15/!RADEG   ; PSR J2151+2315
    ;dec = (23+15/60.+12.8/3600.)/!RADEG
    ;ra = (22+15/60.+39.65/3600.)*15/!RADEG  ; PSR J2215+1538
    ;dec = (15+38/60.+34.88/3600.)/!RADEG
    ;ra = (22+48/60.+26.904/3600.)*15/!RADEG   ; PSR J2248-0101
    ;dec = -(1+1/60.+48.1/3600.)/!RADEG
    ;ra = (22+53/60.+14.533/3600.)*15/!RADEG   ; PSR J2253+1516
    ;dec = (15+16/60.+37.83/3600.)/!RADEG
    ;ra = (23+7/60.+41.288/3600.)*15/!RADEG   ; PSR J2307+2225
    ;dec = (22+25/60.+50.12/3600.)/!RADEG
    ;ra = (23+13/60.+8.598/3600.)*15/!RADEG   ; PSR B2310+42
    ;dec = (42+53/60.+12.99/3600.)/!RADEG
    ;ra = (23+17/60.+57.82/3600.)*15/!RADEG   ; PSR B2315+21
    ;dec = (21+49/60.+48.03/3600.)/!RADEG
    ;ra = (23+46/60.+50.454/3600.)*15/!RADEG   ; PSR J2346-0609
    ;dec = -(6+9/60.+59.5/3600.)/!RADEG

    ;ra = (1+41/60.+39.938/3600.)*15/!RADEG    ; PSR B0138+59
    ;dec = (60+9/60.+32.30/3600.)/!RADEG
    ;ra = (15+43/60.+38.815/3600.)*15/!RADEG    ; PSR B1541+09
    ;dec = (9+29/60.+16.50/3600.)/!RADEG
    ;ra = (16+45/60.+2.041/3600.)*15/!RADEG    ; PSR B1642-03
    ;dec = -(3+17/60.+58.32/3600.)/!RADEG
    ;ra = (22+19/60.+48.139/3600.)*15/!RADEG    ; PSR B2217+47
    ;dec = (47+54/60.+53.93/3600.)/!RADEG

    ;ra = (0+7/60.+0.5819/3600.)*15/!RADEG    ; PSR J0007+7303
    ;dec = (73+3/60.+6.964/3600.)/!RADEG
    '''
    pulsars = [J0006p1834, B0031m07, J0051p0423, B0053p47, B0114p58, J0137p1654,
    B0148m06, J0152p0948, B0301p19, B0320p39, B0329p54, B0355p54, B0410p69,
    B0450p55, J0459m0210, B0531p21, B0609p37, B0656p14, B0655p64, B0809p74,
    B0820p02, B0823p26, B0834p06, B0917p63, B0919p06, J0927p23, B0940p16,
    J0943p22, B0943p10, J0947p27, B0950p08, J1046p0304, B1112p50, B1133p16,
    B1237p25, J1238p21, J1246p22, J1313p0931, B1322p83, J1503p2111, B1508p55]


    for pulsar in pulsars:
        if pulsar.b_name == pulsar_name or pulsar.j_name == pulsar_name:
            pulsar_ra = pulsar.ra
            pulsar_dec = pulsar.dec
            DM = pulsar.DM

    return pulsar_ra, pulsar_dec, DM

################################################################################
################################################################################

if __name__ == '__main__':


    pulsar_ra, pulsar_dec, DM = catalogue_pulsar('B0329+54')

    print(' Pulsar coordinates are:', pulsar_ra, pulsar_dec)
    print(' Pulsar dispersion measure is:', DM, ' pc*cm-3')