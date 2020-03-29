'''
'''
################################################################################

def catalogue_pulsar(pulsar_name):
    pulsar_name = pulsar_name.upper()
    pulsar_ra = ''; pulsar_dec = ''; pulsar_DM = ''

    if   'B0000+00'   in pulsar_name: pulsar_ra = '00h00m00.0s';    pulsar_dec = '+00d00m00.0s';   pulsar_DM = 0.5;      p_bar = 1.0
    elif 'J0006+1834' in pulsar_name: pulsar_ra = '00h06m04.8s';    pulsar_dec = '+18d34m59.0s';   pulsar_DM = 0;        p_bar = 0.69374767047
    elif 'J0007+7303' in pulsar_name: pulsar_ra = '00h07m0.5819s';  pulsar_dec = '+73d3m6.964s';   pulsar_DM = 0;        p_bar = 0.31587319
    elif 'B0031-07'   in pulsar_name: pulsar_ra = '00h34m08.86s';   pulsar_dec = '-07d21m53.4s';   pulsar_DM = 10.89;    p_bar = 0.9429509945598
    elif 'J0051+0423' in pulsar_name: pulsar_ra = '00h51m30.1s';    pulsar_dec = '+04d22m49.0s';   pulsar_DM = 0;        p_bar = 0.35473179890
    elif 'B0053+47'   in pulsar_name: pulsar_ra = '00h56m25.51s';   pulsar_dec = '+47d56m10.5s';   pulsar_DM = 0;        p_bar = 0.472036662076

    elif 'B0114+58'   in pulsar_name: pulsar_ra = '01h17m38.661s';  pulsar_dec = '+59d14m38.39s';  pulsar_DM = 49.423;   p_bar = 0.1014390664824
    elif 'J0137+1654' in pulsar_name: pulsar_ra = '01h37m23.88s';   pulsar_dec = '+16d54m42.1s';   pulsar_DM = 0;        p_bar = 0.4147630265082
    elif 'B0138+59'   in pulsar_name: pulsar_ra = '01h41m39.938s';  pulsar_dec = '+60d09m32.30s';  pulsar_DM = 34.8;     p_bar = 1.2229485205457
    elif 'B0148-06'   in pulsar_name: pulsar_ra = '01h51m22.701s';  pulsar_dec = '-06d35m02.8s';   pulsar_DM = 25.66;    p_bar = 1.464664549334
    elif 'J0152+0948' in pulsar_name: pulsar_ra = '01h52m23.7s';    pulsar_dec = '+09d48m10.0s';   pulsar_DM = 0;        p_bar = 2.74664729014

    elif 'J0243+6257' in pulsar_name: pulsar_ra = '02h41m00.0s';    pulsar_dec = '+63d00m00.0s';   pulsar_DM = 0;        p_bar = 0.5917393
    elif 'J0243+5267' in pulsar_name: pulsar_ra = '           ';    pulsar_dec = '            ';   pulsar_DM = 3.8214;   p_bar = 0
    elif 'J0250+5854' in pulsar_name: pulsar_ra = '02h49m24.0s';    pulsar_dec = '+58d51m47.0s';   pulsar_DM = 45.325;   p_bar = 23.5355039

    elif 'B0301+19'   in pulsar_name: pulsar_ra = '03h04m33.115s';  pulsar_dec = '+19d32m51.4s';   pulsar_DM = 15.74;    p_bar = 1.387584446262
    elif 'B0320+39'   in pulsar_name: pulsar_ra = '03h23m26.618s';  pulsar_dec = '+39d44m52.9s';   pulsar_DM = 26.01;    p_bar = 3.032071956385
    elif 'B0329+54'   in pulsar_name: pulsar_ra = '03h32m59.37s';   pulsar_dec = '+54d34m44.9s';   pulsar_DM = 26.78;    p_bar = 0.714519699726
    elif 'B0355+54'   in pulsar_name: pulsar_ra = '03h58m53.7165s'; pulsar_dec = '+54d13m13.727s'; pulsar_DM = 57.14;    p_bar = 0.1563824177774

    elif 'J0407+1607' in pulsar_name: pulsar_ra = '           ';    pulsar_dec = '            ';   pulsar_DM = 36.0;     p_bar = 0
    elif 'B0410+69'   in pulsar_name: pulsar_ra = '04h15m55.65s';   pulsar_dec = '+69d54m09.89s';  pulsar_DM = 0;        p_bar = 0.3907150899386
    elif 'B0450+55'   in pulsar_name: pulsar_ra = '04h54m07.709s';  pulsar_dec = '+55d43m41.51s';  pulsar_DM = 14.3;     p_bar = 0.340729436235
    elif 'J0459-0210' in pulsar_name: pulsar_ra = '04h59m51.94s';   pulsar_dec = '-02d10m06.6s';   pulsar_DM = 21.02;    p_bar = 1.133076123659

    elif 'B0525+21'   in pulsar_name: pulsar_ra = '            ';   pulsar_dec = '             ';  pulsar_DM = 50.915;   p_bar = 3.7455392503
    elif 'B0531+21'   in pulsar_name: pulsar_ra = '05h34m31.97s';   pulsar_dec = '+22d00m52.06s';  pulsar_DM = 56.791;   p_bar = 0.0333924123

    elif 'B0609+37'   in pulsar_name: pulsar_ra = '06h12m48.68s';   pulsar_dec = '+37d21m37.36s';  pulsar_DM = 27.14;    p_bar = 0.29798232657184
    elif 'B0656+14'   in pulsar_name: pulsar_ra = '06h59m48.13s';   pulsar_dec = '+14d14m21.5s';   pulsar_DM = 0;        p_bar = 0.384891195054
    elif 'B0655+64'   in pulsar_name: pulsar_ra = '07h00m37.0s';    pulsar_dec = '+64d18m11.0s';   pulsar_DM = 0;        p_bar = 0.19567094516627

    elif 'B0809+74'   in pulsar_name or 'J0814+7429' in pulsar_name : pulsar_ra = '08h14m59.5s';    pulsar_dec = '+74d29m05.7s';   pulsar_DM = 5.750;    p_bar = 1.292241446862    # + (epoch_obs-2400000.5-49162.00)*1.68114E-16*86400
    elif 'B0820+02'   in pulsar_name: pulsar_ra = '08h23m09.76s';   pulsar_dec = '+01d59m12.41s';  pulsar_DM = 23.73;    p_bar = 0.8648728046988
    elif 'B0823+26'   in pulsar_name: pulsar_ra = '08h26m51.383s';  pulsar_dec = '+26d37m23.79s';  pulsar_DM = 19.4751;  p_bar = 0.53066051169
    elif 'B0834+06'   in pulsar_name: pulsar_ra = '08h37m05.642s';  pulsar_dec = '+06d10m14.56s';  pulsar_DM = 12.8579;  p_bar = 1.2737682915785

    elif 'B0917+63'   in pulsar_name: pulsar_ra = '09h21m14.135s';  pulsar_dec = '+62d54m13.91s';  pulsar_DM = 0;        p_bar = 1.567994018480
    elif 'B0919+06'   in pulsar_name: pulsar_ra = '09h22m14.025s';  pulsar_dec = '+06d38m23.3s';   pulsar_DM = 27.27;    p_bar = 0.430619453205
    elif 'J0927+23'   in pulsar_name: pulsar_ra = '09h27m37.0s';    pulsar_dec = '+23d47m00.0s';   pulsar_DM = 0;        p_bar = 0.761886
    elif 'B0940+16'   in pulsar_name: pulsar_ra = '09h43m30.1s';    pulsar_dec = '+16d31m37.0s';   pulsar_DM = 0;        p_bar = 1.087417728071
    elif 'B0943+10'   in pulsar_name: pulsar_ra = '09h46m07.31s' ;  pulsar_dec = '+09d51m57.3s';   pulsar_DM = 15.33;    p_bar = 1.09770570486
    elif 'J0943+22'   in pulsar_name: pulsar_ra = '09h43m25.0s';    pulsar_dec = '+22d56m12.41s';  pulsar_DM = 0;        p_bar = 0.532913
    elif 'J0947+27'   in pulsar_name: pulsar_ra = '09h47m22.0s';    pulsar_dec = '+27d42m00.0s';   pulsar_DM = 0;        p_bar = 0.85105
    elif 'B0950+08'   in pulsar_name or 'J0953+0755' in pulsar_name: pulsar_ra = '09h53m09.31s';   pulsar_dec = '+07d55m35.75s';  pulsar_DM = 2.9730;    p_bar = 0.2530651649482  #+ (julday(11,30,2013,4,45,0)-2400000.5-46375.00)*2.29758E-16*86400

    elif 'J1046+0304' in pulsar_name: pulsar_ra = '10h46m43.23s';   pulsar_dec = '+03d04m06.9s';   pulsar_DM = 0;        p_bar = 0.326271446035

    elif 'B1112+50'   in pulsar_name: pulsar_ra = '11h15m38.4s';    pulsar_dec = '+50d30m12.29s';  pulsar_DM = 9.195;    p_bar = 1.656439759937
    elif 'B1133+16'   in pulsar_name or 'J1136+1551' in pulsar_name: pulsar_ra = '11h36m03.248s';  pulsar_dec = '+15d51m04.48s';  pulsar_DM = 4.8471;    p_bar = 1.18791153608

    elif 'B1237+25'   in pulsar_name: pulsar_ra = '12h39m40.46s';   pulsar_dec = '+24d53m49.29s';  pulsar_DM = 9.2755;   p_bar = 1.11859068945
    elif 'J1238+21'   in pulsar_name: pulsar_ra = '12h38m23.17s';   pulsar_dec = '+21d52m11.1s';   pulsar_DM = 0;        p_bar = 1.3824491030388
    elif 'J1246+22'   in pulsar_name: pulsar_ra = '12h46m38.0s';    pulsar_dec = '+22d53m00.0s';   pulsar_DM = 0;        p_bar = 0.473830

    elif 'J1313+0931' in pulsar_name: pulsar_ra = '13h13m23.0s';    pulsar_dec = '+09d31m56.0s';   pulsar_DM = 0;        p_bar = 0.84893275073
    elif 'B1322+83'   in pulsar_name: pulsar_ra = '13h21m46.18s';   pulsar_dec = '+83d23m38.92s';  pulsar_DM = 0;        p_bar = 0.670037418386

    elif 'J1503+2111' in pulsar_name: pulsar_ra = '15h03m54.6s';    pulsar_dec = '+21d11m09.3s';   pulsar_DM = 0;        p_bar = 3.31400150122
    elif 'B1508+55'   in pulsar_name: pulsar_ra = '15h09m25.6211s'; pulsar_dec = '+55d31m32.331s'; pulsar_DM = 19.623;   p_bar = 0.73967789896
    elif 'B1530+27'   in pulsar_name: pulsar_ra = '15h32m10.36s';   pulsar_dec = '+27d45m49.4s';   pulsar_DM = 14.6100;  p_bar = 1.124835742767
    elif 'B1540-06'   in pulsar_name: pulsar_ra = '15h43m30.158s';  pulsar_dec = '-6d20m45.25s';   pulsar_DM = 0;        p_bar = 0.709064069786
    elif 'B1541+09'   in pulsar_name: pulsar_ra = '15h43m38.815s';  pulsar_dec = '+09d29m16.50s';  pulsar_DM = 0;        p_bar = 0.748448416229
    elif 'J1549+2113' in pulsar_name: pulsar_ra = '15h49m40.941s';  pulsar_dec = '+21d13m26.9s';   pulsar_DM = 0;        p_bar = 1.262471311613

    elif 'B1604-00'   in pulsar_name: pulsar_ra = '16h07m12.1s';    pulsar_dec = '-00d32m40.83';   pulsar_DM = 10.68;    p_bar = 0.42181623358258
    elif 'B1612+07'   in pulsar_name: pulsar_ra = '16h14m40.91s';   pulsar_dec = '+07d37m31s';     pulsar_DM = 0;        p_bar = 1.206801436397
    elif 'B1633+24'   in pulsar_name: pulsar_ra = '16h35m25.781s';  pulsar_dec = '+24d18m47.3s';   pulsar_DM = 0;        p_bar = 0.4905065128003
    elif 'B1642-03'   in pulsar_name: pulsar_ra = '16h45m02.041s';  pulsar_dec = '-03d17m58.32s';  pulsar_DM = 35.727;   p_bar = 0.387689698034

    elif 'J1740+1000' in pulsar_name: pulsar_ra = '17h40m25.95s';   pulsar_dec = '+10d00m6.3s';    pulsar_DM = 0;        p_bar = 0.154087174313
    elif 'J1741+2758' in pulsar_name: pulsar_ra = '17h41m53.51s';   pulsar_dec = '+27d58m9.0s';    pulsar_DM = 0;        p_bar = 1.3607376877
    elif 'B1749-28'   in pulsar_name: pulsar_ra = '17h52m58.6896s'; pulsar_dec = '-28d06m+37.3s';  pulsar_DM = 0;        p_bar = 0.56255763553

    elif 'J1817-0743' in pulsar_name: pulsar_ra = '18h17m49.79s';   pulsar_dec = '-07d43m18.9s';   pulsar_DM = 0;        p_bar = 0.438095346909
    elif 'B1822-09'   in pulsar_name: pulsar_ra = '18h25m30.554s';  pulsar_dec = '-9d35m22.1s';    pulsar_DM = 0;        p_bar = 0.769005855083
    elif 'J1832+0029' in pulsar_name: pulsar_ra = '18h32m50.7s';    pulsar_dec = '+00d29m27s';     pulsar_DM = 0;        p_bar = 0.533917296
    elif 'B1839+56'   in pulsar_name: pulsar_ra = '18h40m44.608s';  pulsar_dec = '+56d40m55.47s';  pulsar_DM = 0;        p_bar = 1.6528618528869
    elif 'J1848+0647' in pulsar_name: pulsar_ra = '18h48m56.01s';   pulsar_dec = '+06d47m31.7s';   pulsar_DM = 0;        p_bar = 0.5059567391
    elif 'J1851-0053' in pulsar_name: pulsar_ra = '18h51m3.17s';    pulsar_dec = '-00d53m7.3s';    pulsar_DM = 0;        p_bar = 1.40906524128

    elif 'J1908+0734' in pulsar_name: pulsar_ra = '19h08m17.01s';   pulsar_dec = '+07d34m14.36s';  pulsar_DM = 0;        p_bar = 0.212352673319
    elif 'B1916+14'   in pulsar_name: pulsar_ra = '19h18m23.63s';   pulsar_dec = '+14d45m6.0s';    pulsar_DM = 0;        p_bar = 2.129665364024
    elif 'J1917+0834' in pulsar_name: pulsar_ra = '19h17m48.85s';   pulsar_dec = '+08d+34m54.63s'; pulsar_DM = 0;        p_bar = 1.18102329730
    elif 'J1918+1541' in pulsar_name: pulsar_ra = '19h18m7.70s';    pulsar_dec = '+15d41m15.2s';   pulsar_DM = 0;        p_bar = 0.37088299877
    elif 'B1918+26'   in pulsar_name: pulsar_ra = '19h20m38.374s';  pulsar_dec = '+26d50m38.4s';   pulsar_DM = 0;        p_bar = 0.785521849527
    elif 'B1919+21'   in pulsar_name: pulsar_ra = '19h21m44.81s';   pulsar_dec = '+21d53m2.25s';   pulsar_DM = 12.440;   p_bar = 1.3373021601895
    elif 'B1929+10'   in pulsar_name: pulsar_ra = '19h32m13.95s';   pulsar_dec = '+10d59m32.42s';  pulsar_DM = 3.176;    p_bar = 0.226517635038
    elif 'B1944+17'   in pulsar_name: pulsar_ra = '19h46m53.044s';  pulsar_dec = '+18d5m41.24s';   pulsar_DM = 0;        p_bar = 0.4406184769108
    elif 'B1952+29'   in pulsar_name: pulsar_ra = '19h54m22.554s';  pulsar_dec = '+29d23m17.29s';  pulsar_DM = 0;        p_bar = 0.4266767865302

    elif 'J2015+2524' in pulsar_name: pulsar_ra = '20h15m12.7s';    pulsar_dec = '+25d24m31.3s';   pulsar_DM = 0;        p_bar = 2.3032990816
    elif 'B2016+28'   in pulsar_name: pulsar_ra = '20h18m3.92s';    pulsar_dec = '+28d39m55.2s';   pulsar_DM = 0;        p_bar = 0.5579534804225
    elif 'B2020+28'   in pulsar_name: pulsar_ra = '20h22m37.067s';  pulsar_dec = '+28d54m23.1s';   pulsar_DM = 24.640;   p_bar = 0.3434021577860
    elif 'B2021+51'   in pulsar_name: pulsar_ra = '20h22m49.873s';  pulsar_dec = '+51d54m50.23s';  pulsar_DM = 0;        p_bar = 0.529196917808

    elif 'B2110+27'   in pulsar_name: pulsar_ra = '21h13m4.39s';    pulsar_dec = '+27d54m2.29s';   pulsar_DM = 24.7;     p_bar = 1.2028517540847
    elif 'J2151+2315' in pulsar_name: pulsar_ra = '21h51m10.43s';   pulsar_dec = '+23d15m12.8s';   pulsar_DM = 0;        p_bar = 0.593533613

    elif 'J2215+1538' in pulsar_name: pulsar_ra = '22h15m39.65s';   pulsar_dec = '+15d38m34.88s';  pulsar_DM = 0;        p_bar = 0.3741958930416
    elif 'B2217+47'   in pulsar_name: pulsar_ra = '22h19m48.139s';  pulsar_dec = '+47d54m53.93s';  pulsar_DM = 0;        p_bar = 0.5384688219194
    elif 'J2248-0101' in pulsar_name: pulsar_ra = '22h48m26.904s';  pulsar_dec = '-01d01m48.1s';   pulsar_DM = 0;        p_bar = 0.477233119123
    elif 'J2253+1516' in pulsar_name: pulsar_ra = '22h53m14.533s';  pulsar_dec = '+15d16m37.83s';  pulsar_DM = 0;        p_bar = 0.792235920118

    elif 'J2307+2225' in pulsar_name: pulsar_ra = '23h07m41.288s';  pulsar_dec = '+22d25m50.12s';  pulsar_DM = 0;        p_bar = 0.535828895432
    elif 'B2310+42'   in pulsar_name: pulsar_ra = '23h13m8.598s';   pulsar_dec = '+42d53m12.99s';  pulsar_DM = 0;        p_bar = 0.3494336821331
    elif 'B2315+21'   in pulsar_name: pulsar_ra = '23h17m57.82s';   pulsar_dec = '+21d49m48.03s';  pulsar_DM = 0;        p_bar = 1.444653102317
    elif 'J2346-0609' in pulsar_name: pulsar_ra = '23h46m50.454s';  pulsar_dec = '-06d09m59.5s';   pulsar_DM = 0;        p_bar = 1.181463382967

    else: print('   !!! Source not found !!!')

    return pulsar_ra, pulsar_dec, pulsar_DM, p_bar

################################################################################
################################################################################

if __name__ == '__main__':


    pulsar_ra, pulsar_dec, DM, p_bar = catalogue_pulsar('j0006+1834')

    print(' Pulsar coordinates are:       ', pulsar_ra, pulsar_dec)
    print(' Pulsar dispersion measure is: ', DM, ' pc*cm-3')
    print(' Pulsar period is:             ', p_bar, ' s.')
