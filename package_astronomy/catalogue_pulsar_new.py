'''
'''
################################################################################

def catalogue_pulsar(pulsar_name):
    pulsar_name.upper()

    if   'J0006+1834' in pulsar_name: pulsar_ra = '00h06m04.8s';    pulsar_dec = '+18d34m59.0s';   pulsar_DM = 0
    elif 'B0031-07'   in pulsar_name: pulsar_ra = '00h34m08.86s';   pulsar_dec = '-07d21m53.4s';   pulsar_DM = 0
    elif 'J0051+0423' in pulsar_name: pulsar_ra = '00h51m30.1s';    pulsar_dec = '+04d22m49.0s';   pulsar_DM = 0
    elif 'B0053+47'   in pulsar_name: pulsar_ra = '00h56m25.51s';   pulsar_dec = '+47d56m10.5s';   pulsar_DM = 0
    elif 'B0114+58'   in pulsar_name: pulsar_ra = '01h17m38.661s';  pulsar_dec = '+59d14m38.39s';  pulsar_DM = 0
    elif 'J0137+1654' in pulsar_name: pulsar_ra = '01h37m23.88s';   pulsar_dec = '+16d54m42.1s';   pulsar_DM = 0
    elif 'B0148-06'   in pulsar_name: pulsar_ra = '01h51m22.701s';  pulsar_dec = '-06d35m02.8s';   pulsar_DM = 0
    elif 'J0152+0948' in pulsar_name: pulsar_ra = '01h52m23.7s';    pulsar_dec = '+09d48m10.0s';   pulsar_DM = 0
    elif 'B0301+19'   in pulsar_name: pulsar_ra = '03h04m33.115s';  pulsar_dec = '+19d32m51.4s';   pulsar_DM = 0
    elif 'B0320+39',  in pulsar_name: pulsar_ra = '03h23m26.618s';  pulsar_dec = '+39d44m52.9s';   pulsar_DM = 0
    elif 'B0329+54'   in pulsar_name: pulsar_ra = '03h32m59.37s';   pulsar_dec = '+54d34m44.9s';   pulsar_DM = 0
    elif 'B0355+54'   in pulsar_name: pulsar_ra = '03h58m53.7165s'; pulsar_dec = '+54d13m13.727s'; pulsar_DM = 0
    elif 'B0410+69'   in pulsar_name: pulsar_ra = '04h15m55.65s';   pulsar_dec = '+69d54m09.89s';  pulsar_DM = 0
    elif 'B0450+55'   in pulsar_name: pulsar_ra = '04h54m07.709s';  pulsar_dec = '+55d43m41.51s';  pulsar_DM = 0
    elif 'J0459-0210' in pulsar_name: pulsar_ra = '04h59m51.94s';   pulsar_dec = '-02d10m06.6s';   pulsar_DM = 0
    elif 'B0531+21'   in pulsar_name: pulsar_ra = '05h34m31.97s';   pulsar_dec = '+22d00m52.06s';  pulsar_DM = 0
    elif 'B0609+37'   in pulsar_name: pulsar_ra = '06h12m48.68s';   pulsar_dec = '+37d21m37.36s';  pulsar_DM = 0
    elif 'B0656+14'   in pulsar_name: pulsar_ra = '06h59m48.13s';   pulsar_dec = '+14d14m21.5s';   pulsar_DM = 0
    elif 'B0655+64'   in pulsar_name: pulsar_ra = '07h00m37.0s';    pulsar_dec = '+64d18m11.0s';   pulsar_DM = 0
    elif 'B0809+74'   in pulsar_name: pulsar_ra = '08h14m59.5s';    pulsar_dec = '+74d29m05.7s';   pulsar_DM = 0
    elif 'B0820+02'   in pulsar_name: pulsar_ra = '08h23m09.76s';   pulsar_dec = '+01d59m12.41s';  pulsar_DM = 0
    elif 'B0823+26'   in pulsar_name: pulsar_ra = '08h26m51.383s';  pulsar_dec = '+26d37m23.79s';  pulsar_DM = 0
    elif 'B0834+06'   in pulsar_name: pulsar_ra = '08h37m05.642s';  pulsar_dec = '+06d10m14.56s';  pulsar_DM = 0
    elif 'B0917+63'   in pulsar_name: pulsar_ra = '09h21m14.135s';  pulsar_dec = '+62d54m13.91s';  pulsar_DM = 0
    elif 'B0919+06'   in pulsar_name: pulsar_ra = '09h22m14.025s';  pulsar_dec = '+06d38m23.3s';   pulsar_DM = 0
    elif 'J0927+23'   in pulsar_name: pulsar_ra = '09h27m37.0s';    pulsar_dec = '+23d47m00.0s';   pulsar_DM = 0
    elif 'B0940+16'   in pulsar_name: pulsar_ra = '09h43m30.1s';    pulsar_dec = '+16d31m37.0s';   pulsar_DM = 0
    elif 'J0943+22'   in pulsar_name: pulsar_ra = '09h43m25.0s';    pulsar_dec = '+22d56m12.41s';  pulsar_DM = 0
    elif 'B0943+10'   in pulsar_name: pulsar_ra = '09h46m07.31s' ;  pulsar_dec = '+09d51m57.3s';   pulsar_DM = 0
    elif 'J0947+27'   in pulsar_name: pulsar_ra = '09h47m22.0s';    pulsar_dec = '+27d42m00.0s';   pulsar_DM = 0
    elif 'B0950+08'   in pulsar_name: pulsar_ra = '09h53m09.31s';   pulsar_dec = '+07d55m35.75s';  pulsar_DM = 0
    elif 'J1046+0304' in pulsar_name: pulsar_ra = '10h46m43.23s';   pulsar_dec = '+03d04m06.9s';   pulsar_DM = 0
    elif 'B1112+50'   in pulsar_name: pulsar_ra = '11h15m38.4s';    pulsar_dec = '+50d30m12.29s';  pulsar_DM = 0
    elif 'B1133+16'   in pulsar_name: pulsar_ra = '11h36m03.248s';  pulsar_dec = '+15d51m04.48s';  pulsar_DM = 0
    elif 'B1237+25'   in pulsar_name: pulsar_ra = '12h39m40.46s';   pulsar_dec = '+24d53m49.29s';  pulsar_DM = 0
    elif 'J1238+21'   in pulsar_name: pulsar_ra = '12h38m23.17s';   pulsar_dec = '+21d52m11.1s';   pulsar_DM = 0
    elif 'J1246+22'   in pulsar_name: pulsar_ra = '12h46m38.0s';    pulsar_dec = '+22d53m00.0s';   pulsar_DM = 0
    elif 'J1313+0931' in pulsar_name: pulsar_ra = '13h13m23.0s';    pulsar_dec = '+09d31m56.0s';   pulsar_DM = 0
    elif 'B1322+83'   in pulsar_name: pulsar_ra = '13h21m46.18s';   pulsar_dec = '+83d23m38.92s';  pulsar_DM = 0
    elif 'J1503+2111' in pulsar_name: pulsar_ra = '15h03m54.6s';    pulsar_dec = '+21d11m09.3s';   pulsar_DM = 0
    elif 'B1508+55'   in pulsar_name: pulsar_ra = '15h09m25.6211s'; pulsar_dec = '+55d31m32.331s'; pulsar_DM = 0


    'B1530+27'  '15h32m10.36s'  '+27d45m49.4s' ;
    'B1540-06'  '15h43m30.158s'  '-6d20m45.25s'
    'J1549+2113' '15h49m40.941s'   '21d13m26.9s'
    '''
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




    return pulsar_ra, pulsar_dec, pulsar_DM

################################################################################
################################################################################

if __name__ == '__main__':


    pulsar_ra, pulsar_dec, DM = catalogue_pulsar('j0006+1834')

    print(' Pulsar coordinates are:', pulsar_ra, pulsar_dec)
    print(' Pulsar dispersion measure is:', DM, ' pc*cm-3')
