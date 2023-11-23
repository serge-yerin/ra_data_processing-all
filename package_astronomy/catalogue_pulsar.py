from astropy.time import Time
import numpy as np


def catalogue_pulsar(pulsar_name, epoch_obs='2020-01-01 00:00:00.000000'):

    # Calculate epoch of observations in julian days
    t = Time([epoch_obs], scale='utc')
    epoch_obs = np.float64(t.jd)

    pulsar_name = pulsar_name.upper()
    pulsar_ra = ''; pulsar_dec = ''; pulsar_DM = 0; p_bar = 0

    if   'B0000+00'   in pulsar_name: pulsar_ra = '00h00m00.0s';    pulsar_dec = '+00d00m00.0s';   pulsar_DM = 7.96179;     p_bar = 1.0

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

    elif 'J0242+6256' in pulsar_name: pulsar_ra = '02h42m35.0s';    pulsar_dec = '+62d56m50.0s';   pulsar_DM = 3.8214;   p_bar = 0.592
    # elif 'J0243+6257' in pulsar_name: pulsar_ra = '02h41m00.0s';    pulsar_dec = '+63d00m00.0s';   pulsar_DM = 0;        p_bar = 0.5917393
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

    elif 'J0740+6620' in pulsar_name: pulsar_ra = '07h40m45.7927s'; pulsar_dec = '+66d20m33.520s'; pulsar_DM = 14.96179; p_bar = 0.002885736411412693

    # elif 'B0809+74'   in pulsar_name or 'J0814+7429' in pulsar_name : pulsar_ra = '08h14m59.5s';    pulsar_dec = '+74d29m05.7s';   pulsar_DM = 5.75066;    p_bar = 1.292241446862    # + (epoch_obs-2400000.5-49162.00)*1.68114E-16*86400
    # elif 'B0809+74'   in pulsar_name or 'J0814+7429' in pulsar_name : pulsar_ra = '08h14m59.5s';    pulsar_dec = '+74d29m05.7s';   pulsar_DM = 5.752;    p_bar = 1.292241446862    # + (epoch_obs-2400000.5-49162.00)*1.68114E-16*86400
    elif 'B0809+74'   in pulsar_name or 'J0814+7429' in pulsar_name: pulsar_ra = '08h14m59.5s';    pulsar_dec = '+74d29m05.7s'; pulsar_DM = 5.755; p_bar = 1.292241446862 + (epoch_obs - 2400000.5 - 49162.00) * 1.68114E-16 * 86400
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
    # elif 'B0950+08'   in pulsar_name or 'J0953+0755' in pulsar_name: pulsar_ra = '09h53m09.31s';   pulsar_dec = '+07d55m35.75s';  pulsar_DM = 2.96927;    p_bar = 0.2530651649482  #+ (julday(11,30,2013,4,45,0)-2400000.5-46375.00)*2.29758E-16*86400
    elif 'B0950+08'   in pulsar_name or 'J0953+0755' in pulsar_name: pulsar_ra = '09h53m09.31s';   pulsar_dec = '+07d55m35.75s';  pulsar_DM = 2.972;    p_bar = 0.2530651649482 + (epoch_obs - 2400000.5 - 46375.00) * 2.29758E-16 * 86400

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

    elif 'B1604-00'   in pulsar_name: pulsar_ra = '16h07m12.1s';    pulsar_dec = '-00d32m40.83';   pulsar_DM = 10.6823;  p_bar = 0.42181623358258
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
    # elif 'B1919+21'   in pulsar_name: pulsar_ra = '19h21m44.81s';   pulsar_dec = '+21d53m2.25s';   pulsar_DM = 12.440;   p_bar = 1.3373021601895
    elif 'B1919+21'   in pulsar_name: pulsar_ra = '19h21m44.81s';   pulsar_dec = '+21d53m2.25s';   pulsar_DM = 12.4449;   p_bar = 1.3373021601895
    elif 'B1929+10'   in pulsar_name: pulsar_ra = '19h32m13.95s';   pulsar_dec = '+10d59m32.42s';  pulsar_DM = 3.176;    p_bar = 0.226517635038
    elif 'B1944+17'   in pulsar_name: pulsar_ra = '19h46m53.044s';  pulsar_dec = '+18d5m41.24s';   pulsar_DM = 0;        p_bar = 0.4406184769108
    elif 'B1952+29'   in pulsar_name: pulsar_ra = '19h54m22.554s';  pulsar_dec = '+29d23m17.29s';  pulsar_DM = 0;        p_bar = 0.4266767865302

    elif 'J2015+2524' in pulsar_name: pulsar_ra = '20h15m12.7s';    pulsar_dec = '+25d24m31.3s';   pulsar_DM = 0;        p_bar = 2.3032990816
    elif 'B2016+28'   in pulsar_name: pulsar_ra = '20h18m3.92s';    pulsar_dec = '+28d39m55.2s';   pulsar_DM = 0;        p_bar = 0.5579534804225
    elif 'B2020+28'   in pulsar_name: pulsar_ra = '20h22m37.067s';  pulsar_dec = '+28d54m23.1s';   pulsar_DM = 24.640;   p_bar = 0.3434021577860
    elif 'B2021+51'   in pulsar_name: pulsar_ra = '20h22m49.873s';  pulsar_dec = '+51d54m50.23s';  pulsar_DM = 0;        p_bar = 0.529196917808

    elif 'B2045-16'   in pulsar_name or 'J2048-1616' in pulsar_name : pulsar_ra = '20h48m35.640637s';    pulsar_dec = '-16d16m44.55350s';   pulsar_DM = 11.456;    p_bar = 1.961572303613


    elif 'B2110+27'   in pulsar_name: pulsar_ra = '21h13m4.39s';    pulsar_dec = '+27d54m2.29s';   pulsar_DM = 24.7;     p_bar = 1.2028517540847
    elif 'J2151+2315' in pulsar_name: pulsar_ra = '21h51m10.43s';   pulsar_dec = '+23d15m12.8s';   pulsar_DM = 0;        p_bar = 0.593533613

    elif 'J2215+1538' in pulsar_name: pulsar_ra = '22h15m39.65s';   pulsar_dec = '+15d38m34.88s';  pulsar_DM = 0;        p_bar = 0.3741958930416
    elif 'B2217+47'   in pulsar_name: pulsar_ra = '22h19m48.139s';  pulsar_dec = '+47d54m53.93s';  pulsar_DM = 0;        p_bar = 0.5384688219194
    elif 'B2224+65'   in pulsar_name: pulsar_ra = '22h25m52.8627s';  pulsar_dec = '+65d35m36.371s';  pulsar_DM = 36.44362;        p_bar = 0.682542497406
    elif 'J2248-0101' in pulsar_name: pulsar_ra = '22h48m26.904s';  pulsar_dec = '-01d01m48.1s';   pulsar_DM = 0;        p_bar = 0.477233119123
    elif 'J2253+1516' in pulsar_name: pulsar_ra = '22h53m14.533s';  pulsar_dec = '+15d16m37.83s';  pulsar_DM = 0;        p_bar = 0.792235920118

    elif 'J2307+2225' in pulsar_name: pulsar_ra = '23h07m41.288s';  pulsar_dec = '+22d25m50.12s';  pulsar_DM = 0;        p_bar = 0.535828895432
    elif 'B2310+42'   in pulsar_name: pulsar_ra = '23h13m8.598s';   pulsar_dec = '+42d53m12.99s';  pulsar_DM = 0;        p_bar = 0.3494336821331
    elif 'B2315+21'   in pulsar_name: pulsar_ra = '23h17m57.82s';   pulsar_dec = '+21d49m48.03s';  pulsar_DM = 0;        p_bar = 1.444653102317
    elif 'J2325-0530' in pulsar_name: pulsar_ra = '23h25m15.3s';    pulsar_dec = '-05d30m39s';     pulsar_DM = 14.966;   p_bar = 0.868735115025
    elif 'J2336-01'   in pulsar_name: pulsar_ra = '23h36m36s';      pulsar_dec = '-01d51m00s';     pulsar_DM = 19.60;    p_bar = 1.0298
    elif 'J2346-0609' in pulsar_name: pulsar_ra = '23h46m50.454s';  pulsar_dec = '-06d09m59.5s';   pulsar_DM = 0;        p_bar = 1.181463382967
    elif 'J2347+02'   in pulsar_name: pulsar_ra = '23h47m00s';      pulsar_dec = '+02d00m00s';     pulsar_DM = 15.0;     p_bar = 1.38347

    ################## From Igor Kravtsov ########################V
    # RRATs
    elif 'J0013+29' in pulsar_name:
        pulsar_ra = '00h13m16s';      pulsar_dec = '+29d49m18s';     pulsar_DM = 36.2;     p_bar = 1.5
    elif 'J0027+84' in pulsar_name:
        pulsar_ra = '00h27m16s';      pulsar_dec = '+84d17m23s';     pulsar_DM = 9.65;     p_bar = 1.5
    elif 'J0034+27' in pulsar_name:
        pulsar_ra = '00h34m57s';      pulsar_dec = '+27d47m00s';     pulsar_DM = 16.0;     p_bar = 1.5
    elif 'J0053+6938' in pulsar_name:
        pulsar_ra = '00h53m13s';      pulsar_dec = '+69d39m03s';     pulsar_DM = 90.3;     p_bar = 1.16
    elif 'J0054+6650' in pulsar_name:
        pulsar_ra = '00h54m55s';      pulsar_dec = '+66d50m24s';     pulsar_DM = 14.550974; p_bar = 1.39017001799
    elif 'J0103+54' in pulsar_name:
        pulsar_ra = '01h03m37s';      pulsar_dec = '+54d02m00s';     pulsar_DM = 55.605;   p_bar = 0.354304
    elif 'J0121+5329' in pulsar_name:
        pulsar_ra = '01h21m19s';      pulsar_dec = '+53d29m24s';     pulsar_DM = 87.35;    p_bar = 2.7255
    elif 'J0156+04' in pulsar_name:
        pulsar_ra = '01h56m01s';      pulsar_dec = '+04d02m00s';     pulsar_DM = 27.5;     p_bar = 1.5
    elif 'J0201+7005' in pulsar_name:
        pulsar_ra = '02h01m41s';      pulsar_dec = '+70d05m18s';     pulsar_DM = 21.029;   p_bar = 1.349184471846
    elif 'J0203+7022' in pulsar_name:
        pulsar_ra = '02h03m28s';      pulsar_dec = '+70d22m44s';     pulsar_DM = 21.0;     p_bar = 1.35
    elif 'J0209+58' in pulsar_name:
        pulsar_ra = '02h09m12s';      pulsar_dec = '+58d12m01s';     pulsar_DM = 56.0;     p_bar = 1.0637
    elif 'J0226+3356' in pulsar_name:
        pulsar_ra = '02h27m08s';      pulsar_dec = '+33d55m44s';     pulsar_DM = 27.397;   p_bar = 1.2401
    elif 'J0253+52' in pulsar_name:
        pulsar_ra = '02h53m35s';      pulsar_dec = '+52d43m18s';     pulsar_DM = 28.5757810804579;     p_bar = 1.5
    elif 'J0301+20' in pulsar_name:
        pulsar_ra = '03h01m04s';      pulsar_dec = '+20d52m33s';     pulsar_DM = 19.0;     p_bar = 1.207
    elif 'J0305+4001' in pulsar_name:
        pulsar_ra = '03h05m26s';      pulsar_dec = '+40d01m00s';     pulsar_DM = 24;       p_bar = 1.5
    elif 'J0317+1328' in pulsar_name:
        pulsar_ra = '03h17m54s';      pulsar_dec = '+13d29m00s';     pulsar_DM = 12.7452;  p_bar = 1.9742
    elif 'J0327+09' in pulsar_name:
        pulsar_ra = '03h27m58s';      pulsar_dec = '+09d35m06s';     pulsar_DM = 93.68;    p_bar = 1.5
    elif 'J0332+7910' in pulsar_name:
        pulsar_ra = '03h32m45s';      pulsar_dec = '+79d10m00s';     pulsar_DM = 16.589;   p_bar = 2.0562
    elif 'J0348+79' in pulsar_name:
        pulsar_ra = '03h48m18s';      pulsar_dec = '+79d18m26s';     pulsar_DM = 26.09;    p_bar = 1.5
    elif 'J0357-05' in pulsar_name:
        pulsar_ra = '03h57m56s';      pulsar_dec = '-05d09m44s';     pulsar_DM = 56.4;     p_bar = 2.0
    elif 'J0441-04' in pulsar_name:
        pulsar_ra = '04h41m00s';      pulsar_dec = '-04d18m00s';     pulsar_DM = 20.0;     p_bar = 1.5
    elif 'J0447-04' in pulsar_name:
        pulsar_ra = '04h47m00s';      pulsar_dec = '-04d35m00s';     pulsar_DM = 29.83;    p_bar = 2.18819
    elif 'J0452+1651' in pulsar_name:
        pulsar_ra = '04h52m00s';      pulsar_dec = '+16d51m00s';     pulsar_DM = 18.5;     p_bar = 1.5
    elif 'J0503+22' in pulsar_name:
        pulsar_ra = '05h03m00s';      pulsar_dec = '+22d20m00s';     pulsar_DM = 92;       p_bar = 1.5
    elif 'J0513-04' in pulsar_name:
        pulsar_ra = '05h13m00s';      pulsar_dec = '-04d18m00s';     pulsar_DM = 18.5;     p_bar = 1.5
    elif 'J0517+24' in pulsar_name:
        pulsar_ra = '05h17m55s';      pulsar_dec = '+24d30m38s';     pulsar_DM = 74.3;     p_bar = 1.5
    elif 'J0534+3407' in pulsar_name:
        pulsar_ra = '05h34m30s';      pulsar_dec = '+34d07m00s';     pulsar_DM = 24.5;     p_bar = 1.5
    elif 'J0544+20' in pulsar_name:
        pulsar_ra = '05h44m12s';      pulsar_dec = '-20d50m00s';     pulsar_DM = 56.9;     p_bar = 1.5
    elif 'J0545-03' in pulsar_name:
        pulsar_ra = '05h45m00s';      pulsar_dec = '-03d10m00s';     pulsar_DM = 67.2;     p_bar = 1.5
    elif 'J0550+09' in pulsar_name:
        pulsar_ra = '05h50m28s';      pulsar_dec = '+09d51m00s';     pulsar_DM = 86.6;     p_bar = 1.745
    elif 'J0609+1635' in pulsar_name:
        pulsar_ra = '06h09m13s';      pulsar_dec = '+16d34m00s';     pulsar_DM = 85;       p_bar = 1.5
    elif 'J0614-03' in pulsar_name:
        pulsar_ra = '06h15m00s';      pulsar_dec = '-03d29m00s';     pulsar_DM = 17.9;     p_bar = 0.136
    elif 'J0625+1730' in pulsar_name:
        pulsar_ra = '06h25m19s';      pulsar_dec = '+17d30m00s';     pulsar_DM = 58;       p_bar = 1.5
    elif 'J0627+16' in pulsar_name:
        pulsar_ra = '06h27m13s';      pulsar_dec = '+16d12m00s';     pulsar_DM = 113;      p_bar = 2.180
    elif 'J0628+09' in pulsar_name:
        pulsar_ra = '06h28m36s';      pulsar_dec = '+09d09m14s';     pulsar_DM = 88.3;     p_bar = 1.241
    elif 'J0630+19' in pulsar_name:
        pulsar_ra = '06h30m04s';      pulsar_dec = '+19d37m30s';     pulsar_DM = 48.3;     p_bar = 1.24855
    elif 'J0630+25' in pulsar_name:
        pulsar_ra = '06h31m00s';      pulsar_dec = '+25d23m14s';     pulsar_DM = 22.3;     p_bar = 1.5
    elif 'J0653-06' in pulsar_name:
        pulsar_ra = '06h53m00s';      pulsar_dec = '-06d16m00s';     pulsar_DM = 83.7;     p_bar = 0.79
    elif 'J0658+29' in pulsar_name:
        pulsar_ra = '06h58m06s';      pulsar_dec = '+29d32m08s';     pulsar_DM = 40.05;    p_bar = 0.82
    elif 'J0658-15' in pulsar_name:
        pulsar_ra = '06h58m55s';      pulsar_dec = '-15d16m50s';     pulsar_DM = 57.6;     p_bar = 1.5
    elif 'J0741+17' in pulsar_name:
        pulsar_ra = '07h41m00s';      pulsar_dec = '+17d03m00s';     pulsar_DM = 44.3;     p_bar = 1.73
    elif 'J0746+55' in pulsar_name:
        pulsar_ra = '07h46m48s';      pulsar_dec = '+55d14m33s';     pulsar_DM = 10.326333; p_bar = 2.89378549447
    elif 'J0803+3410' in pulsar_name:
        pulsar_ra = '08h03m05s';      pulsar_dec = '+34d19m00s';     pulsar_DM = 34;       p_bar = 1.5
    elif 'J0812+8626' in pulsar_name:
        pulsar_ra = '08h12m30s';      pulsar_dec = '+86d26m00s';     pulsar_DM = 40.25;    p_bar = 1.5
    elif 'J0845-03' in pulsar_name:
        pulsar_ra = '08h45m00s';      pulsar_dec = '-03d34m48s';     pulsar_DM = 14.15;    p_bar = 1.5
    elif 'J0854+54' in pulsar_name:
        pulsar_ra = '08h54m24s';      pulsar_dec = '+54d48m00s';     pulsar_DM = 17.8;     p_bar = 1.2329

    #     elif 'J0854+54_1' in pulsar_name: pulsar_ra = '08h54m24s';      pulsar_dec = '+54d48m00s';       pulsar_DM = 18.843;   p_bar = 1.2330

    elif 'J0939+45' in pulsar_name:
        pulsar_ra = '09h39m31s';      pulsar_dec = '+45d15m00s';     pulsar_DM = 17.45;    p_bar = 1.5
    elif 'J0941+1621' in pulsar_name:
        pulsar_ra = '09h43m30s';      pulsar_dec = '+16d31m00s';     pulsar_DM = 23.5;     p_bar = 1.5
    elif 'J0957-06' in pulsar_name:
        pulsar_ra = '09h57m00s';      pulsar_dec = '-06d17m00s';     pulsar_DM = 26.95;    p_bar = 1.72370
    elif 'J1010+15' in pulsar_name:
        pulsar_ra = '10h10m00s';      pulsar_dec = '+15d00m00s';     pulsar_DM = 42.15;    p_bar = 1.5
    elif 'J1048+53' in pulsar_name:
        pulsar_ra = '10h48m28s';      pulsar_dec = '+53d41m49s';     pulsar_DM = 30.85;    p_bar = 1.5
    elif 'J1059-01' in pulsar_name:
        pulsar_ra = '10h59m00s';      pulsar_dec = '-01d02m00s';     pulsar_DM = 18.7;     p_bar = 1.5
    elif 'J1105+02' in pulsar_name:
        pulsar_ra = '11h05m32s';      pulsar_dec = '+02d28m50s';     pulsar_DM = 16.5;     p_bar = 6.403055372
    elif 'J1130+09' in pulsar_name:
        pulsar_ra = '11h30m55s';      pulsar_dec = '+09d20m00s';     pulsar_DM = 21.9;     p_bar = 4.796636974

    #    elif 'J1130+09_1' in pulsar_name: pulsar_ra = '11h30m55s';      pulsar_dec = '+09d20m00s';       pulsar_DM = 21.0;    p_bar = 4.796636974

    elif 'J1132+0921' in pulsar_name:
        pulsar_ra = '11h32m00s';      pulsar_dec = '+09d21m00s';     pulsar_DM = 22.0;     p_bar = 1.5
    elif 'J1156-1318' in pulsar_name:
        pulsar_ra = '11h56m42s';      pulsar_dec = '-13d18m22s';     pulsar_DM = 28.0;     p_bar = 1.5
    elif 'J1246+53' in pulsar_name:
        pulsar_ra = '12h51m48s';      pulsar_dec = '+53d41m24s';     pulsar_DM = 21.03;    p_bar = 1.5
    elif 'J1326+33' in pulsar_name:
        pulsar_ra = '13h26m42s';      pulsar_dec = '+33d46m00s';     pulsar_DM = 4.19;     p_bar = 0.0415
    elif 'J1332-03' in pulsar_name:
        pulsar_ra = '13h32m00s';      pulsar_dec = '-03d26m00s';     pulsar_DM = 27.1;     p_bar = 1.10640
    elif 'J1336-20' in pulsar_name:
        pulsar_ra = '13h36m00s';      pulsar_dec = '-20d34m00s';     pulsar_DM = 19.3;     p_bar = 0.184
    elif 'J1336+3346' in pulsar_name:
        pulsar_ra = '13h36m34s';      pulsar_dec = '+34d14m38s';     pulsar_DM = 8.4688;   p_bar = 1.50660326546

    #    elif 'J1336+3346_1' in pulsar_name: pulsar_ra = '13h36m34s';    pulsar_dec = '+34d14m38s';       pulsar_DM = 8.4688;  p_bar = 3.013

    elif 'J1346+06' in pulsar_name:
        pulsar_ra = '13h46m11s';      pulsar_dec = '+06d10m00s';     pulsar_DM = 9.0;      p_bar = 1.5
    elif 'J1354+2454' in pulsar_name:
        pulsar_ra = '13h54m00s';      pulsar_dec = '+24d54m00s';     pulsar_DM = 20.1;     p_bar = 0.85106

    #    elif 'J1354+2454_1' in pulsar_name: pulsar_ra = '13h54m00s';    pulsar_dec = '+24d54m00s';       pulsar_DM = 20.1;    p_bar = 6.27

    elif 'J1404+1210' in pulsar_name:
        pulsar_ra = '14h04m36s';      pulsar_dec = '+11d59m00s';     pulsar_DM = 18.53;    p_bar = 2.6504
    elif 'J1430+22' in pulsar_name:
        pulsar_ra = '14h30m01s';      pulsar_dec = '+22d24m24s';     pulsar_DM = 23.32;    p_bar = 1.5
    elif 'J1432+09' in pulsar_name:
        pulsar_ra = '14h32m30s';      pulsar_dec = '+09d08m00s';     pulsar_DM = 14.0;     p_bar = 1.5
    elif 'J1433+00' in pulsar_name:
        pulsar_ra = '14h33m30s';      pulsar_dec = '+00d28m00s';     pulsar_DM = 23.5;     p_bar = 1.5
    elif 'J1439+7655' in pulsar_name:
        pulsar_ra = '14h39m00s';      pulsar_dec = '+76d55m00s';     pulsar_DM = 22.29;    p_bar = 0.948
    elif 'J1502+2813' in pulsar_name:
        pulsar_ra = '15h02m09s';      pulsar_dec = '+28d13m00s';     pulsar_DM = 14.0;     p_bar = 3.784
    elif 'J1524-20' in pulsar_name:
        pulsar_ra = '15h24m44s';      pulsar_dec = '-20d59m21s';     pulsar_DM = 40.1;     p_bar = 1.5
    elif 'J1532+00' in pulsar_name:
        pulsar_ra = '15h32m40s';      pulsar_dec = '+00d42m00s';     pulsar_DM = 12.3;     p_bar = 1.5
    elif 'J1538+2345' in pulsar_name:
        pulsar_ra = '15h38m06s';      pulsar_dec = '+23d45m04s';     pulsar_DM = 6.9;      p_bar = 3.44938495332
    elif 'J1541+47' in pulsar_name:
        pulsar_ra = '15h41m00s';      pulsar_dec = '+47d03m00s';     pulsar_DM = 19.4;     p_bar = 0.277700692893
    elif 'J1550+0943' in pulsar_name:
        pulsar_ra = '15h50m47s';      pulsar_dec = '+09d43m00s';     pulsar_DM = 21.0;     p_bar = 0.28
    elif 'J1554+18' in pulsar_name:
        pulsar_ra = '15h54m17s';      pulsar_dec = '+18d04m00s';     pulsar_DM = 23.94;    p_bar = 1.5
    elif 'J1555+0108' in pulsar_name:
        pulsar_ra = '15h55m58s';      pulsar_dec = '+01d08m00s';     pulsar_DM = 18.0;     p_bar = 1.5
    elif 'J1603+18' in pulsar_name:
        pulsar_ra = '16h03m34s';      pulsar_dec = '+18d51m00s';     pulsar_DM = 29.7;     p_bar = 0.503
    elif 'J1603-1655' in pulsar_name:
        pulsar_ra = '16h03m09s';      pulsar_dec = '-16d55m28s';     pulsar_DM = 63.22;    p_bar = 0.7147
    elif 'J1611-01' in pulsar_name:
        pulsar_ra = '16h11m00s';      pulsar_dec = '-01d28m00s';     pulsar_DM = 27.21;    p_bar = 1.29687
    elif 'J1610-17' in pulsar_name:
        pulsar_ra = '16h10m11s';      pulsar_dec = '-17d50m00s';     pulsar_DM = 52.5;     p_bar = 1.3
    elif 'J1623-0841' in pulsar_name:
        pulsar_ra = '16h23m43s';      pulsar_dec = '-08d41m37s';     pulsar_DM = 59.79;    p_bar = 0.503045281599
    elif 'J1639+21' in pulsar_name:
        pulsar_ra = '16h39m40s';      pulsar_dec = '+21d59m30s';     pulsar_DM = 14.4;     p_bar = 0.79073276630
    elif 'J1640-09' in pulsar_name:
        pulsar_ra = '16h40m17s';      pulsar_dec = '-09d15m49s';     pulsar_DM = 50.2;     p_bar = 1.5
    elif 'J1705-04' in pulsar_name:
        pulsar_ra = '17h05m00s';      pulsar_dec = '-04d41m00s';     pulsar_DM = 42.951;   p_bar = 0.23748
    elif 'J1717+03' in pulsar_name:
        pulsar_ra = '17h17m56s';      pulsar_dec = '+03d11m00s';     pulsar_DM = 25.6;     p_bar = 3.901
    elif 'J1720+00' in pulsar_name:
        pulsar_ra = '17h20m55s';      pulsar_dec = '+00d40m00s';     pulsar_DM = 46.2;     p_bar = 3.353
    elif 'J1722+31' in pulsar_name:
        pulsar_ra = '17h22m00s';      pulsar_dec = '+31d00m00s';     pulsar_DM = 109.88;   p_bar = 1.5
    elif 'J1732+2700' in pulsar_name:
        pulsar_ra = '17h32m24s';      pulsar_dec = '+27d00m00s';     pulsar_DM = 36.0;     p_bar = 1.5
    elif 'J1737+24' in pulsar_name:
        pulsar_ra = '17h37m00s';      pulsar_dec = '+24d00m00s';     pulsar_DM = 59.80;    p_bar = 2.449
    elif 'J1753-12' in pulsar_name:
        pulsar_ra = '17h52m53s';      pulsar_dec = '-12d59m00s';     pulsar_DM = 73.2;     p_bar = 0.405454
    elif 'J1835-15' in pulsar_name:
        pulsar_ra = '18h35m54s';      pulsar_dec = '-15d35m25s';     pulsar_DM = 22.9;     p_bar = 1.5
    elif 'J1838+5051' in pulsar_name:
        pulsar_ra = '18h38m01s';      pulsar_dec = '+50d54m00s';     pulsar_DM = 21.8;     p_bar = 2.5772
    elif 'J1840-1419' in pulsar_name:
        pulsar_ra = '18h40m33s';      pulsar_dec = '-14d19m07s';     pulsar_DM = 19.4;     p_bar = 6.59756252242
    elif 'J1841-0448' in pulsar_name:
        pulsar_ra = '18h41m10s';      pulsar_dec = '+04d48m00s';     pulsar_DM = 29.0;     p_bar = 1.5
    elif 'J1848-12' in pulsar_name:
        pulsar_ra = '18h48m18s';      pulsar_dec = '-12d43m30s';     pulsar_DM = 91.96;    p_bar = 0.414
    elif 'J1848+1516' in pulsar_name:
        pulsar_ra = '18h49m21s';      pulsar_dec = '+15d17m07s';     pulsar_DM = 77.436;   p_bar = 2.23376977466
    elif 'J1850+15' in pulsar_name:
        pulsar_ra = '18h50m09s';      pulsar_dec = '+15d32m00s';     pulsar_DM = 24.7;     p_bar = 1.383965
    elif 'J1907+34' in pulsar_name:
        pulsar_ra = '19h07m00s';      pulsar_dec = '+34d00m00s';     pulsar_DM = 64.85;    p_bar = 1.5
    elif 'J1911+00' in pulsar_name:
        pulsar_ra = '19h11m48s';      pulsar_dec = '+00d37m00s';     pulsar_DM = 100.0;    p_bar = 6.94
    elif 'J1912+08' in pulsar_name:
        pulsar_ra = '19h12m00s';      pulsar_dec = '+08d00m00s';     pulsar_DM = 96.0;     p_bar = 1.5
    elif 'J1915-11' in pulsar_name:
        pulsar_ra = '19h15m00s';      pulsar_dec = '-11d30m00s';     pulsar_DM = 91.06;    p_bar = 2.1770
    elif 'J1917+1723' in pulsar_name:
        pulsar_ra = '19h17m30s';      pulsar_dec = '+17d23m00s';     pulsar_DM = 38.0;     p_bar = 1.5
    elif 'J1925-16' in pulsar_name:
        pulsar_ra = '19h25m06s';      pulsar_dec = '-16d01m00s';     pulsar_DM = 88.0;     p_bar = 3.8858
    elif 'J1929+11' in pulsar_name:
        pulsar_ra = '19h29m00s';      pulsar_dec = '+11d00m00s';     pulsar_DM = 80.0;     p_bar = 3.218
    elif 'J1929+42' in pulsar_name:
        pulsar_ra = '19h29m11s';      pulsar_dec = '+42d40m00s';     pulsar_DM = 51.25;    p_bar = 3.6375
    elif 'J1930+0104' in pulsar_name:
        pulsar_ra = '19h30m30s';      pulsar_dec = '+01d04m00s';     pulsar_DM = 42.0;     p_bar = 1.5
    elif 'J1941-0746' in pulsar_name:
        pulsar_ra = '19h41m05s';      pulsar_dec = '-07d46m19s';     pulsar_DM = 43.6;     p_bar = 1.5
    elif 'J1943+58' in pulsar_name:
        pulsar_ra = '19h43m00s';      pulsar_dec = '+58d13m00s';     pulsar_DM = 71.2;     p_bar = 1.27085
    elif 'J1944-10' in pulsar_name:
        pulsar_ra = '19h44m00s';      pulsar_dec = '-10d17m00s';     pulsar_DM = 31.009999;    p_bar = 0.409115991961
    elif 'J1945+61' in pulsar_name:
        pulsar_ra = '19h45m40s';      pulsar_dec = '+61d46m12s';     pulsar_DM = 83.3;     p_bar = 1.5
    elif 'J1946+24' in pulsar_name:
        pulsar_ra = '19h46m00s';      pulsar_dec = '+23d58m00s';     pulsar_DM = 96.0;     p_bar = 4.729
    elif 'J1955-0907' in pulsar_name:
        pulsar_ra = '19h55m57s';      pulsar_dec = '-09d07m14s';     pulsar_DM = 72.0;     p_bar = 0.484
    elif 'J2002+13' in pulsar_name:
        pulsar_ra = '20h02m07s';      pulsar_dec = '+13d03m00s';     pulsar_DM = 5.0;      p_bar = 1.5
    elif 'J2007+20' in pulsar_name:
        pulsar_ra = '20h07m00s';      pulsar_dec = '+20d21m00s';     pulsar_DM = 67.0;     p_bar = 4.634
    elif 'J2018-07' in pulsar_name:
        pulsar_ra = '20h18m00s';      pulsar_dec = '-07d45m00s';     pulsar_DM = 15.0;     p_bar = 1.5
    elif 'J2033+00' in pulsar_name:
        pulsar_ra = '20h33m31s';      pulsar_dec = '+00d42m23s';     pulsar_DM = 37.84;    p_bar = 5.013
    elif 'J2047+1259' in pulsar_name:
        pulsar_ra = '20h47m45s';      pulsar_dec = '+12d59m00s';     pulsar_DM = 36.00;    p_bar = 1.5
    elif 'J2052+1308' in pulsar_name:
        pulsar_ra = '20h52m47s';      pulsar_dec = '+12d19m00s';     pulsar_DM = 42.00;    p_bar = 1.5
    elif 'J2100+50' in pulsar_name:
        pulsar_ra = '21h01m00s';      pulsar_dec = '+50d55m43s';     pulsar_DM = 18.462;   p_bar = 1.5
    elif 'J2105+1917' in pulsar_name:
        pulsar_ra = '21h05m20s';      pulsar_dec = '+19d21m00s';     pulsar_DM = 34.47;    p_bar = 3.5298
    elif 'J2105+6223' in pulsar_name:
        pulsar_ra = '21h05m13s';      pulsar_dec = '+62d23m05s';     pulsar_DM = 50.75;    p_bar = 2.30487883766
    elif 'J2107+2606' in pulsar_name:
        pulsar_ra = '21h07m30s';      pulsar_dec = '+26d06m00s';     pulsar_DM = 11.12;    p_bar = 5.458
    elif 'J2108+45' in pulsar_name:
        pulsar_ra = '21h08m01s';      pulsar_dec = '+45d18m00s';     pulsar_DM = 84.0;     p_bar = 0.577369
    elif 'J2111+34' in pulsar_name:
        pulsar_ra = '21h11m26s';      pulsar_dec = '+34d43m23s';     pulsar_DM = 79.8;     p_bar = 1.5
    elif 'J2116+37' in pulsar_name:
        pulsar_ra = '21h16m20s';      pulsar_dec = '+37d07m45s';     pulsar_DM = 44.0;     p_bar = 0.145
    elif 'J2135+3032' in pulsar_name:
        pulsar_ra = '21h35m00s';      pulsar_dec = '+30d32m00s';     pulsar_DM = 63.0;     p_bar = 1.5
    elif 'J2138+69' in pulsar_name:
        pulsar_ra = '21h38m00s';      pulsar_dec = '+69d50m00s';     pulsar_DM = 46.6;     p_bar = 0.22
    elif 'J2146+2148' in pulsar_name:
        pulsar_ra = '21h46m00s';      pulsar_dec = '+21d48m00s';     pulsar_DM = 43.0;     p_bar = 1.5
    elif 'J2202+2134' in pulsar_name:
        pulsar_ra = '21h02m21s';      pulsar_dec = '+21d47m00s';     pulsar_DM = 17.7473;  p_bar = 1.3573
    elif 'J2205+2244' in pulsar_name:
        pulsar_ra = '22h05m30s';      pulsar_dec = '+22d44m00s';     pulsar_DM = 22.0;     p_bar = 1.5
    elif 'J2208+46' in pulsar_name:
        pulsar_ra = '22h08m31s';      pulsar_dec = '+46d06m50s';     pulsar_DM = 63.0;     p_bar = 0.6425
    elif 'J2210+2118' in pulsar_name:
        pulsar_ra = '22h09m54s';      pulsar_dec = '+21d17m00s';     pulsar_DM = 45.0;     p_bar = 1.5
    elif 'J2215+4524' in pulsar_name:
        pulsar_ra = '22h14m01s';      pulsar_dec = '+45d25m00s';     pulsar_DM = 18.5917;  p_bar = 2.7230498235
    elif 'J2221+81' in pulsar_name:
        pulsar_ra = '22h21m00s';      pulsar_dec = '+81d32m00s';     pulsar_DM = 39.0;     p_bar = 1.5
    elif 'J2225+35' in pulsar_name:
        pulsar_ra = '22h24m48s';      pulsar_dec = '+35d30m00s';     pulsar_DM = 51.8;     p_bar = 0.94
    elif 'J2237+2828' in pulsar_name:
        pulsar_ra = '22h37m29s';      pulsar_dec = '+28d28m40s';     pulsar_DM = 38.1;     p_bar = 1.0773950914
    elif 'J2239+42' in pulsar_name:
        pulsar_ra = '22h39m01s';      pulsar_dec = '+42d35m28s';     pulsar_DM = 28.306;   p_bar = 1.5
    elif 'J2252+2451' in pulsar_name:
        pulsar_ra = '22h52m23s';      pulsar_dec = '+24d51m23s';     pulsar_DM = 34.4;     p_bar = 1.7979
    elif 'J2311+6656' in pulsar_name:
        pulsar_ra = '23h11m39s';      pulsar_dec = '+66d55m26s';     pulsar_DM = 97.1;     p_bar = 1.945
    elif 'J2316+75' in pulsar_name:
        pulsar_ra = '23h15m00s';      pulsar_dec = '+75d44m00s';     pulsar_DM = 53.4;     p_bar = 1.5
    elif 'J2329+04' in pulsar_name:
        pulsar_ra = '23h29m48s';      pulsar_dec = '+04d00m00s';     pulsar_DM = 12.5126;  p_bar = 1.5
    elif 'J2334+20' in pulsar_name:
        pulsar_ra = '23h34m00s';      pulsar_dec = '+20d00m00s';     pulsar_DM = 13.22;    p_bar = 1.5
    elif 'J2355+1523' in pulsar_name:
        pulsar_ra = '23h55m48s';      pulsar_dec = '+15d23m18s';     pulsar_DM = 26.924;   p_bar = 1.09439626467

    #    elif 'J2355+1523_1' in pulsar_name: pulsar_ra = '23h55m48s';     pulsar_dec = '15d23m18s';      pulsar_DM = 26.0;   p_bar = 1.09439626467

    elif 'J2357+24' in pulsar_name:
        pulsar_ra = '23h57m48s';      pulsar_dec = '24d00m00s';      pulsar_DM = 8.6;      p_bar = 1.5

    # Additional RRATs

    elif 'J0139+3336' in pulsar_name:
        pulsar_ra = '01h39m57s';      pulsar_dec = '+33d37m03s';     pulsar_DM = 21.229;   p_bar = 1.2479609557
    elif 'J0640+0744' in pulsar_name:
        pulsar_ra = '06h40m30s';      pulsar_dec = '+07d44m30s';     pulsar_DM = 55.529;   p_bar = 1.00002925341
    elif 'J0746+5514' in pulsar_name:
        pulsar_ra = '07h46m48s';      pulsar_dec = '+55d14m33s';     pulsar_DM = 10.318;   p_bar = 2.8936673467
    elif 'J1005+3015' in pulsar_name:
        pulsar_ra = '10h06m35s';      pulsar_dec = '+30d15m46s';     pulsar_DM = 18.0815;  p_bar = 3.06624955248
    elif 'J1132+2515' in pulsar_name:
        pulsar_ra = '11h32m50s';      pulsar_dec = '+25d15m00s';     pulsar_DM = 23.716;   p_bar = 1.0021
    elif 'J1218+47' in pulsar_name:
        pulsar_ra = '12h18m56s';      pulsar_dec = '+47d14m00s';     pulsar_DM = 20.144;   p_bar = 1.5
    elif 'J1329+1349' in pulsar_name:
        pulsar_ra = '13h29m00s';      pulsar_dec = '+13d44m00s';     pulsar_DM = 12.367;   p_bar = 1.5
    elif 'J1400+2127' in pulsar_name:
        pulsar_ra = '14h00m14s';      pulsar_dec = '+21d25m40s';     pulsar_DM = 11.2072;  p_bar = 1.8555953418
    elif 'J1931+4229' in pulsar_name:
        pulsar_ra = '19h31m11s';      pulsar_dec = '+42d29m18s';     pulsar_DM = 50.987;   p_bar = 3.9209748695

    #  PC2

    elif 'J1049+5822' in pulsar_name:
        pulsar_ra = '10h49m38s';      pulsar_dec = '+58d22m20s';     pulsar_DM = 12.364;   p_bar = 0.72761787288
    elif 'J1226+00' in pulsar_name:
        pulsar_ra = '12h26m12s';      pulsar_dec = '+00d03m00s';     pulsar_DM = 18.564;   p_bar = 2.2851

    #  DPC

    # elif ''   in pulsar_name: pulsar_ra = '';      pulsar_dec = '';     pulsar_DM = ;     p_bar =

    elif 'J0957-06' in pulsar_name:
        pulsar_ra = '09h57m00s';      pulsar_dec = '-06d17m00s';     pulsar_DM = 26.95;    p_bar = 1.724
    elif 'J1005+3015' in pulsar_name:
        pulsar_ra = '10h06m35s';      pulsar_dec = '+30d15m46s';     pulsar_DM = 18.081567;     p_bar = 3.06624955248
    elif 'J1059-01' in pulsar_name:
        pulsar_ra = '10h59m00s';      pulsar_dec = '-01d02m00s';     pulsar_DM = 18.7;     p_bar = 1.5

    elif 'J1332-03' in pulsar_name:
        pulsar_ra = '13h32m00s';      pulsar_dec = '-03d26m00s';     pulsar_DM = 27.1;     p_bar = 1.106
    elif 'J1336-20' in pulsar_name:
        pulsar_ra = '13h36m00s';      pulsar_dec = '-20d34m00s';     pulsar_DM = 19.3;     p_bar = 0.184
    elif 'J1354+24' in pulsar_name:
        pulsar_ra = '13h54m00s';      pulsar_dec = '+24d54m00s';     pulsar_DM = 20.0;     p_bar = 1.5
    elif 'J1400+2127' in pulsar_name:
        pulsar_ra = '14h00m14s';      pulsar_dec = '+21d25m40s';     pulsar_DM = 11.207249;     p_bar = 1.8555953418
    elif 'J1433+00' in pulsar_name:
        pulsar_ra = '14h33m00s';      pulsar_dec = '+00d28m00s';     pulsar_DM = 23.5;     p_bar = 1.5

    elif 'J1538+2345' in pulsar_name:
        pulsar_ra = '15h38m06s';      pulsar_dec = '+23d45m04s';     pulsar_DM = 14.9;     p_bar = 3.449

    # Distant pulsars' census замінити періоди!!!! + скрізь по дві цифри в координатах!

    elif 'B0011+47' in pulsar_name:
        pulsar_ra = '00h14m18s';      pulsar_dec = '+47d46m33s';     pulsar_DM = 30.405;   p_bar = 1.240699039
    elif 'J0033+57' in pulsar_name:
        pulsar_ra = '00h33m00s';      pulsar_dec = '+57d00m00s';     pulsar_DM = 75.65;    p_bar = 0.315
    elif 'J0033+61' in pulsar_name:
        pulsar_ra = '00h33m00s';      pulsar_dec = '+61d00m00s';     pulsar_DM = 37.7;     p_bar = 0.912
    elif 'J0039+35' in pulsar_name:
        pulsar_ra = '00h39m06s';      pulsar_dec = '+35d45m00s';     pulsar_DM = 53.04;    p_bar = 0.5367
    elif 'B0037+56' in pulsar_name:
        pulsar_ra = '00h40m32s';      pulsar_dec = '+57d16m25s';     pulsar_DM = 92.5146;  p_bar = 1.118225345

    elif 'B0045+33' in pulsar_name:
        pulsar_ra = '00h48m34s';      pulsar_dec = '+34d12m08s';     pulsar_DM = 39.922;   p_bar = 1.217094296
    elif 'J0054+6946' in pulsar_name:
        pulsar_ra = '00h54m59s';      pulsar_dec = '+69d46m17s';     pulsar_DM = 116.52;   p_bar = 0.832911329
    elif 'B0052+51' in pulsar_name:
        pulsar_ra = '00h55m45s';      pulsar_dec = '+51d17m24s';     pulsar_DM = 44.0127;  p_bar = 2.115171149
    elif 'J0058+4950' in pulsar_name:
        pulsar_ra = '00h58m10s';      pulsar_dec = '+49d50m26s';     pulsar_DM = 66.953;   p_bar = 0.996023452
    elif 'J0059+69' in pulsar_name:
        pulsar_ra = '00h59m30s';      pulsar_dec = '+69d55m00s';     pulsar_DM = 63.53;    p_bar = 1.1459

    elif 'J0100+8023' in pulsar_name:
        pulsar_ra = '01h00m16s';      pulsar_dec = '+80d23m41s';     pulsar_DM = 56.0062;  p_bar = 1.493600919
    elif 'B0059+65' in pulsar_name:
        pulsar_ra = '01h02m33s';      pulsar_dec = '+65d37m13s';     pulsar_DM = 65.853;   p_bar = 1.679164229
    elif 'J0103+54' in pulsar_name:
        pulsar_ra = '01h03m37s';      pulsar_dec = '+54d02m00s';     pulsar_DM = 55.605;   p_bar = 0.354304
    elif 'B0105+65' in pulsar_name:
        pulsar_ra = '01h08m23s';      pulsar_dec = '+66d08m34s';     pulsar_DM = 30.5482;  p_bar = 1.283659843
    elif 'B0105+68' in pulsar_name:
        pulsar_ra = '01h08m29s';      pulsar_dec = '+69d05m53s';     pulsar_DM = 61.0617;  p_bar = 1.07111811

    elif 'J0111+6624' in pulsar_name:
        pulsar_ra = '01h11m22s';      pulsar_dec = '+66d24m11s';     pulsar_DM = 111.20;   p_bar = 4.301872101
    elif 'J0115+6325' in pulsar_name:
        pulsar_ra = '01h15m46s';      pulsar_dec = '+63d25m51s';     pulsar_DM = 65.069;   p_bar = 0.521455427
    elif 'B0114+58' in pulsar_name:
        pulsar_ra = '01h17m39s';      pulsar_dec = '+59d14m38s';     pulsar_DM = 49.42068; p_bar = 0.101439066
    elif 'J0121+53' in pulsar_name:
        pulsar_ra = '01h21m00s';      pulsar_dec = '+53d29m00s';     pulsar_DM = 91.38;    p_bar = 2.7247846
    elif 'J0125+62' in pulsar_name:
        pulsar_ra = '01h26m00s';      pulsar_dec = '+62d35m00s';     pulsar_DM = 118.0;    p_bar = 1.708233

    elif 'J0139+5621' in pulsar_name:
        pulsar_ra = '01h39m39s';      pulsar_dec = '+56d21m37s';     pulsar_DM = 101.842;  p_bar = 1.775343826
    elif 'B0136+57' in pulsar_name:
        pulsar_ra = '01h39m20s';      pulsar_dec = '+58d14m32s';     pulsar_DM = 73.81141; p_bar = 0.272450631
    elif 'B0138+59' in pulsar_name:
        pulsar_ra = '01h41m40s';      pulsar_dec = '+60d09m32s';     pulsar_DM = 34.926;   p_bar = 1.222948521
    elif 'B0144+59' in pulsar_name:
        pulsar_ra = '01h47m45s';      pulsar_dec = '+59d22m03s';     pulsar_DM = 40.111;   p_bar = 0.196321375
    elif 'B0153+39' in pulsar_name:
        pulsar_ra = '01h56m55s';      pulsar_dec = '+39d49m29s';     pulsar_DM = 59.833;   p_bar = 1.811560611

    elif 'B0154+61' in pulsar_name:
        pulsar_ra = '01h57m50s';      pulsar_dec = '+62d12m27s';     pulsar_DM = 30.21;    p_bar = 2.351744936
    elif 'J0209+5759' in pulsar_name:
        pulsar_ra = '02h09m37s';      pulsar_dec = '+57d59m45s';     pulsar_DM = 55.855;   p_bar = 1.063906283
    elif 'J0210+5845' in pulsar_name:
        pulsar_ra = '02h10m55s';      pulsar_dec = '+58d45m04s';     pulsar_DM = 76.772;   p_bar = 1.766208099
    elif 'J0212+5222' in pulsar_name:
        pulsar_ra = '02h12m52s';      pulsar_dec = '+52d22m50s';     pulsar_DM = 38.21;    p_bar = 0.376386364
    elif 'J0215+6218' in pulsar_name:
        pulsar_ra = '02h15m57s';      pulsar_dec = '+62d18m33s';     pulsar_DM = 84.00;    p_bar = 0.548879819

    elif 'J0220+36' in pulsar_name:
        pulsar_ra = '02h20m50s';      pulsar_dec = '+36d22m00s';     pulsar_DM = 40.00;    p_bar = 1.0297
    elif 'B0226+70' in pulsar_name:
        pulsar_ra = '02h31m14s';      pulsar_dec = '+70d26m34s';     pulsar_DM = 46.6794;  p_bar = 1.466820306
    elif 'J0244+14' in pulsar_name:
        pulsar_ra = '02h44m51s';      pulsar_dec = '+14d27m00s';     pulsar_DM = 31.00;    p_bar = 2.1281
    elif 'J0250+5854' in pulsar_name:
        pulsar_ra = '02h50m18s';      pulsar_dec = '+58d54m01s';     pulsar_DM = 45.281;   p_bar = 23.53537848
    elif 'J0324+5239' in pulsar_name:
        pulsar_ra = '03h24m55s';      pulsar_dec = '+52d39m31s';     pulsar_DM = 115.4636; p_bar = 0.33662023

    elif 'J0325+6744' in pulsar_name:
        pulsar_ra = '03h25m05s';      pulsar_dec = '+67d44m59s';     pulsar_DM = 65.28;    p_bar = 1.364678767
    elif 'J0329+1654' in pulsar_name:
        pulsar_ra = '03h29m09s';      pulsar_dec = '+16d54m02s';     pulsar_DM = 40.821;   p_bar = 0.893319661
    elif 'B0331+45' in pulsar_name:
        pulsar_ra = '03h35m17s';      pulsar_dec = '+45d55m53s';     pulsar_DM = 47.14571; p_bar = 0.269200541
    elif 'J0335+6623' in pulsar_name:
        pulsar_ra = '03h35m57s';      pulsar_dec = '+66d23m24s';     pulsar_DM = 66.726;   p_bar = 1.761934247
    elif 'J0341+5711' in pulsar_name:
        pulsar_ra = '03h41m00s';      pulsar_dec = '+57d11m00s';     pulsar_DM = 101.0;    p_bar = 1.888

    elif 'B0339+53' in pulsar_name:
        pulsar_ra = '03h43m13s';      pulsar_dec = '+53d12m53s';     pulsar_DM = 67.30;    p_bar = 1.934478067
    elif 'J0344-0901' in pulsar_name:
        pulsar_ra = '03h44m38s';      pulsar_dec = '-09d01m03s';     pulsar_DM = 30.9;     p_bar = 1.226005573
    elif 'J0349+2340' in pulsar_name:
        pulsar_ra = '03h49m57s';      pulsar_dec = '+23d40m53s';     pulsar_DM = 62.962;   p_bar = 2.420770978
    elif 'B0353+52' in pulsar_name:
        pulsar_ra = '03h57m45s';      pulsar_dec = '+52d36m57s';     pulsar_DM = 103.706;  p_bar = 0.197030098
    elif 'J0358+4155' in pulsar_name:
        pulsar_ra = '03h58m03s';      pulsar_dec = '+41d55m19s';     pulsar_DM = 46.325;   p_bar = 0.226484332

    elif 'B0355+54' in pulsar_name:
        pulsar_ra = '03h58m54s';      pulsar_dec = '+54d13m14s';     pulsar_DM = 57.1420;  p_bar = 0.156384122
    elif 'B0402+61' in pulsar_name:
        pulsar_ra = '04h06m30s';      pulsar_dec = '+61d38m41s';     pulsar_DM = 65.4053;  p_bar = 0.594576165
    elif 'J0408+55A' in pulsar_name:
        pulsar_ra = '04h08m00s';      pulsar_dec = '+55d00m00s';     pulsar_DM = 55.0;     p_bar = 1.837
    elif 'J0408+55B' in pulsar_name:
        pulsar_ra = '04h08m00s';      pulsar_dec = '+55d00m00s';     pulsar_DM = 63.8;     p_bar = 0.754
    elif 'J0413+58' in pulsar_name:
        pulsar_ra = '04h13m00s';      pulsar_dec = '+58d00m00s';     pulsar_DM = 57.0;     p_bar = 0.687

    elif 'J0417+35' in pulsar_name:
        pulsar_ra = '04h17m43s';      pulsar_dec = '+35d45m00s';     pulsar_DM = 48.5336;  p_bar = 0.65440
    elif 'J0417+61' in pulsar_name:
        pulsar_ra = '04h17m00s';      pulsar_dec = '+61d08m00s';     pulsar_DM = 70.14;    p_bar = 0.440283
    elif 'J0419+44' in pulsar_name:
        pulsar_ra = '04h19m00s';      pulsar_dec = '+44d00m00s';     pulsar_DM = 71.0;     p_bar = 1.241
    elif 'J0421-0345' in pulsar_name:
        pulsar_ra = '04h21m34s';      pulsar_dec = '-03d45m07s';     pulsar_DM = 44.61;    p_bar = 2.161308495
    elif 'J0421+3255' in pulsar_name:
        pulsar_ra = '04h21m33s';      pulsar_dec = '+32d55m50s';     pulsar_DM = 77.02;    p_bar = 0.900105016

    elif 'J0426+4933' in pulsar_name:
        pulsar_ra = '04h26m07s';      pulsar_dec = '+49d33m38s';     pulsar_DM = 84.3;     p_bar = 0.92247473
    elif 'J0435+2749' in pulsar_name:
        pulsar_ra = '04h35m52s';      pulsar_dec = '+27d49m02s';     pulsar_DM = 53.19;    p_bar = 0.326279453
    elif 'B0447-12' in pulsar_name:
        pulsar_ra = '04h50m09s';      pulsar_dec = '-12d48m07s';     pulsar_DM = 37.041;   p_bar = 0.438014149
    elif 'B0450-18' in pulsar_name:
        pulsar_ra = '04h52m34s';      pulsar_dec = '-17d59m23s';     pulsar_DM = 39.903;   p_bar = 0.548939223294
    elif 'J0457+23' in pulsar_name:
        pulsar_ra = '04h57m06s';      pulsar_dec = '+23d34m00s';     pulsar_DM = 59.0;     p_bar = 0.5049

    elif 'J0458-0505' in pulsar_name:
        pulsar_ra = '04h58m37s';      pulsar_dec = '-05d05m05s';     pulsar_DM = 47.806;   p_bar = 1.883479658
    elif 'B0458+46' in pulsar_name:
        pulsar_ra = '05h02m05s';      pulsar_dec = '+46d54m06s';     pulsar_DM = 41.834;   p_bar = 0.638565482
    elif 'J0518+5125' in pulsar_name:
        pulsar_ra = '05h18m26s';      pulsar_dec = '+51d25m59s';     pulsar_DM = 39.244;   p_bar = 0.912511685
    elif 'J0518+5416' in pulsar_name:
        pulsar_ra = '05h18m53s';      pulsar_dec = '+54d16m50s';     pulsar_DM = 42.330;   p_bar = 0.340202652
    elif 'J0519+44' in pulsar_name:
        pulsar_ra = '05h19m00s';      pulsar_dec = '+44d00m00s';     pulsar_DM = 52.0;     p_bar = 0.515

    elif 'B0523+11' in pulsar_name:
        pulsar_ra = '05h25m56s';      pulsar_dec = '+11d15m19s';     pulsar_DM = 79.418;   p_bar = 0.354437595
    elif 'B0525+21' in pulsar_name:
        pulsar_ra = '05h28m52s';      pulsar_dec = '+22d00m04s';     pulsar_DM = 50.8695;  p_bar = 3.74553925
    elif 'J0529-0715' in pulsar_name:
        pulsar_ra = '05h29m09s';      pulsar_dec = '-07d15m26s';     pulsar_DM = 87.3;     p_bar = 0.689223601
    elif 'J0533+0402' in pulsar_name:
        pulsar_ra = '05h33m26s';      pulsar_dec = '+04d02m00s';     pulsar_DM = 83.7;     p_bar = 0.963017825
    elif 'J0538+2817' in pulsar_name:
        pulsar_ra = '05h38m25s';      pulsar_dec = '+28d17m09s';     pulsar_DM = 39.570;   p_bar = 0.143158259

    elif 'J0540+3207' in pulsar_name:
        pulsar_ra = '05h40m37s';      pulsar_dec = '+32d07m37s';     pulsar_DM = 61.97;    p_bar = 0.524270863
    elif 'B0540+23' in pulsar_name:
        pulsar_ra = '05h43m11s';      pulsar_dec = '+23d16m40s';     pulsar_DM = 77.7026;  p_bar = 0.245983683
    elif 'J0545-03' in pulsar_name:
        pulsar_ra = '05h45m00s';      pulsar_dec = '-03d10m00s';     pulsar_DM = 67.2;     p_bar = 1.07393
    elif 'J0546+2441' in pulsar_name:
        pulsar_ra = '05h46m29s';      pulsar_dec = '+24d41m21s';     pulsar_DM = 73.81;    p_bar = 2.843850385
    elif 'J0550+09' in pulsar_name:
        pulsar_ra = '05h50m28s';      pulsar_dec = '+09d51m00s';     pulsar_DM = 86.6;     p_bar = 1.745

    elif 'J0555+3948' in pulsar_name:
        pulsar_ra = '05h55m00s';      pulsar_dec = '+39d48m00s';     pulsar_DM = 36.1;     p_bar = 1.1469058
    elif 'B0559-05' in pulsar_name:
        pulsar_ra = '06h01m59s';      pulsar_dec = '-05d27m51s';     pulsar_DM = 80.538;   p_bar = 0.39596917
    elif 'J0608+00' in pulsar_name:
        pulsar_ra = '06h08m49s';      pulsar_dec = '+00d39m00s';     pulsar_DM = 48.5;     p_bar = 1.0762
    elif 'J0609+16' in pulsar_name:
        pulsar_ra = '06h09m13s';      pulsar_dec = '+16d34m00s';     pulsar_DM = 84.0;     p_bar = 0.9458
    elif 'J0611+04' in pulsar_name:
        pulsar_ra = '06h11m18s';      pulsar_dec = '+04d06m00s';     pulsar_DM = 69.9;     p_bar = 1.67443

    elif 'J0611+1436' in pulsar_name:
        pulsar_ra = '06h11m19s';      pulsar_dec = '+14d36m52s';     pulsar_DM = 43.99;    p_bar = 0.270329463
    elif 'J0611+30' in pulsar_name:
        pulsar_ra = '06h11m16s';      pulsar_dec = '+30d16m00s';     pulsar_DM = 45.2551;  p_bar = 1.412090
    elif 'J0612+37216' in pulsar_name:
        pulsar_ra = '06h12m44s';      pulsar_dec = '+37d21m40s';     pulsar_DM = 39.270;  p_bar = 0.443871368
    elif 'B0611+22' in pulsar_name:
        pulsar_ra = '06h14m17s';      pulsar_dec = '+22d29m57s';     pulsar_DM = 96.91;    p_bar = 0.334959966
    elif 'J0614+83' in pulsar_name:
        pulsar_ra = '06h14m00s';      pulsar_dec = '+83d14m00s';     pulsar_DM = 44.2;     p_bar = 1.039203

    elif 'J0621+0336' in pulsar_name:
        pulsar_ra = '06h21m11s';      pulsar_dec = '+03d36m46s';     pulsar_DM = 72.53;    p_bar = 0.269954068
    elif 'J0623+0340' in pulsar_name:
        pulsar_ra = '06h23m47s';      pulsar_dec = '+03d40m07s';     pulsar_DM = 54.0;     p_bar = 0.6137596
    elif 'B0621-04' in pulsar_name:
        pulsar_ra = '06h24m20s';      pulsar_dec = '-04d24m50s';     pulsar_DM = 70.835;   p_bar = 1.039076476
    elif 'J0625+10' in pulsar_name:
        pulsar_ra = '06h25m45s';      pulsar_dec = '+10d16m00s';     pulsar_DM = 78.0;     p_bar = 0.498397
    elif 'J0627+0649' in pulsar_name:
        pulsar_ra = '06h27m54s';      pulsar_dec = '+06d49m54s';     pulsar_DM = 86.60;    p_bar = 0.346522567

    elif 'J0627+16' in pulsar_name:
        pulsar_ra = '06h27m13s';      pulsar_dec = '+16d12m00s';     pulsar_DM = 113.0;    p_bar = 2.180
    elif 'J0628+0909' in pulsar_name:
        pulsar_ra = '06h28m36s';      pulsar_dec = '+09d09m14s';     pulsar_DM = 88.3;     p_bar = 1.241421391
    elif 'B0626+24' in pulsar_name:
        pulsar_ra = '06h29m06s';      pulsar_dec = '+24d15m42s';     pulsar_DM = 84.1762;  p_bar = 0.476622836
    elif 'J0630-0046' in pulsar_name:
        pulsar_ra = '06h30m27s';      pulsar_dec = '-00d46m06s';     pulsar_DM = 97.9;     p_bar = 0.680574832
    elif 'J0630+19' in pulsar_name:
        pulsar_ra = '06h30m04s';      pulsar_dec = '+19d37m00s';     pulsar_DM = 48.1;     p_bar = 1.24855

    elif 'J0645+80' in pulsar_name:
        pulsar_ra = '06h46m00s';      pulsar_dec = '+80d09m00s';     pulsar_DM = 49.7;     p_bar = 0.657873
    elif 'J0652-0142' in pulsar_name:
        pulsar_ra = '06h52m11s';      pulsar_dec = '-01d42m30s';     pulsar_DM = 116.3;    p_bar = 0.924053918
    elif 'B0643+80' in pulsar_name:
        pulsar_ra = '06h53m15s';      pulsar_dec = '+80d52m00s';     pulsar_DM = 33.31882; p_bar = 1.214440512
    elif 'J0658+0022' in pulsar_name:
        pulsar_ra = '06h58m15s';      pulsar_dec = '+00d22m35s';     pulsar_DM = 115.6;    p_bar = 0.563294925
    elif 'J0711+0931' in pulsar_name:
        pulsar_ra = '07h11m36s';      pulsar_dec = '+09d31m25s';     pulsar_DM = 46.238;   p_bar = 1.214090492

    elif 'J0725-1635' in pulsar_name:
        pulsar_ra = '07h25m00s';      pulsar_dec = '-16d35m46s';     pulsar_DM = 98.98;    p_bar = 0.424311403
    elif 'J0729-1448' in pulsar_name:
        pulsar_ra = '07h29m16s';      pulsar_dec = '-14d48m37s';     pulsar_DM = 91.89;    p_bar = 0.251658714
    elif 'B0727-18' in pulsar_name:
        pulsar_ra = '07h29m32s';      pulsar_dec = '-18d36m42s';     pulsar_DM = 61.293;   p_bar = 0.510160345
    elif 'J0742+4334' in pulsar_name:
        pulsar_ra = '07h42m42s';      pulsar_dec = '+43d34m02s';     pulsar_DM = 36.255;   p_bar = 0.60619068
    elif 'J0753-0816' in pulsar_name:
        pulsar_ra = '07h53m33s';      pulsar_dec = '-08d19m35s';     pulsar_DM = 38.0;     p_bar = 2.09362

    elif 'B0751+32' in pulsar_name:
        pulsar_ra = '07h54m41s';      pulsar_dec = '+32d31m56s';     pulsar_DM = 39.9863;  p_bar = 1.442349479
    elif 'B0756-15' in pulsar_name:
        pulsar_ra = '07h58m29s';      pulsar_dec = '-15d28m09s';     pulsar_DM = 63.327;   p_bar = 0.682265176
    elif 'J0806+08' in pulsar_name:
        pulsar_ra = '08h06m05s';      pulsar_dec = '+08d17m00s';     pulsar_DM = 46.0;     p_bar = 2.0631
    elif 'J0813+22' in pulsar_name:
        pulsar_ra = '08h13m54s';      pulsar_dec = '+22d01m00s';     pulsar_DM = 52.29;    p_bar = 0.5314
    elif 'J0815+0939' in pulsar_name:
        pulsar_ra = '08h15m09s';      pulsar_dec = '+09d39m51s';     pulsar_DM = 52.6589;  p_bar = 0.645161191

    elif 'B0818-13' in pulsar_name:
        pulsar_ra = '08h20m26s';      pulsar_dec = '-13d50m56s';     pulsar_DM = 40.938;   p_bar = 1.238129544
    elif 'J0843+0719' in pulsar_name:
        pulsar_ra = '08h43m34s';      pulsar_dec = '+07d18m48s';     pulsar_DM = 36.6;     p_bar = 1.36586
    elif 'J0848+16' in pulsar_name:
        pulsar_ra = '08h48m53s';      pulsar_dec = '+16d43m00s';     pulsar_DM = 38.0;     p_bar = 0.4524
    elif 'B0841+80' in pulsar_name:
        pulsar_ra = '08h49m01s';      pulsar_dec = '+80d28m59s';     pulsar_DM = 34.8121;  p_bar = 1.602227974
    elif 'J0928+06' in pulsar_name:
        pulsar_ra = '09h28m44s';      pulsar_dec = '+06d14m00s';     pulsar_DM = 49.8;     p_bar = 2.0604

    elif 'B1016-16' in pulsar_name:
        pulsar_ra = '10h18m40s';      pulsar_dec = '-16d42m10s';     pulsar_DM = 48.82;    p_bar = 1.804694946
    elif 'B1039-19' in pulsar_name:
        pulsar_ra = '10h41m36s';      pulsar_dec = '-19d42m14s';     pulsar_DM = 33.777;   p_bar = 1.386368075
    elif 'B1309-12' in pulsar_name:
        pulsar_ra = '13h11m53s';      pulsar_dec = '-12d28m02s';     pulsar_DM = 36.214;   p_bar = 0.447517711
    elif 'J1343+6634' in pulsar_name:
        pulsar_ra = '13h43m59s';      pulsar_dec = '+66d34m25s';     pulsar_DM = 30.031;   p_bar = 1.394103786
    elif 'J1403-0314' in pulsar_name:
        pulsar_ra = '14h03m41s';      pulsar_dec = '-03d15m28s';     pulsar_DM = 31.0;     p_bar = 0.362634

    elif 'B1541+09' in pulsar_name:
        pulsar_ra = '15h43m39s';      pulsar_dec = '+09d29m16s';     pulsar_DM = 34.9758;  p_bar = 0.748448416
    elif 'J1544-0713' in pulsar_name:
        pulsar_ra = '15h44m24s';      pulsar_dec = '-07d13m59s';     pulsar_DM = 30.73;    p_bar = 0.484129803
    elif 'J1547-0944' in pulsar_name:
        pulsar_ra = '15h47m46s';      pulsar_dec = '-09d44m08s';     pulsar_DM = 37.416;   p_bar = 1.576924633
    elif 'J1609-1930' in pulsar_name:
        pulsar_ra = '16h09m05s';      pulsar_dec = '-19d30m08s';     pulsar_DM = 37.0;     p_bar = 1.557917248
    elif 'B1607-13' in pulsar_name:
        pulsar_ra = '16h10m43s';      pulsar_dec = '-13d22m22s';     pulsar_DM = 49.13;    p_bar = 1.018392746

    elif 'J1623-0841' in pulsar_name:
        pulsar_ra = '16h23m43s';      pulsar_dec = '-08d41m37s';     pulsar_DM = 59.79;    p_bar = 0.503015006
    elif 'B1620-09' in pulsar_name:
        pulsar_ra = '16h23m18s';      pulsar_dec = '-09d08m49s';     pulsar_DM = 68.183;   p_bar = 1.27644582
    elif 'J1624+8643' in pulsar_name:
        pulsar_ra = '16h24m33s';      pulsar_dec = '+86d43m13s';     pulsar_DM = 46.55;    p_bar = 0.395763022
    elif 'J1627+1419' in pulsar_name:
        pulsar_ra = '16h27m19s';      pulsar_dec = '+14d19m21s';     pulsar_DM = 32.16696; p_bar = 0.49085673
    elif 'J1631-1612' in pulsar_name:
        pulsar_ra = '16h31m52s';      pulsar_dec = '-16d12m52s';     pulsar_DM = 33.77;    p_bar = 0.677683912

    elif 'J1632-1013' in pulsar_name:
        pulsar_ra = '16h32m54s';      pulsar_dec = '-10d13m18s';     pulsar_DM = 89.9;     p_bar = 0.717637328
    elif 'J1635-1511' in pulsar_name:
        pulsar_ra = '16h35m47s';      pulsar_dec = '-15d11m52s';     pulsar_DM = 54.0;     p_bar = 1.179387039
    elif 'J1635+2332' in pulsar_name:
        pulsar_ra = '16h35m05s';      pulsar_dec = '+23d32m23s';     pulsar_DM = 37.568;   p_bar = 1.208694246
    elif 'J1638+4005' in pulsar_name:
        pulsar_ra = '16h38m16s';      pulsar_dec = '+40d05m56s';     pulsar_DM = 33.417;   p_bar = 0.767720392
    elif 'J1643+1338' in pulsar_name:
        pulsar_ra = '16h43m54s';      pulsar_dec = '+13d38m44s';     pulsar_DM = 35.821;   p_bar = 1.099047163

    elif 'B1642-03' in pulsar_name:
        pulsar_ra = '16h45m02s';      pulsar_dec = '-03d17m58s';     pulsar_DM = 35.7555;  p_bar = 0.387689698
    elif 'J1645+1012' in pulsar_name:
        pulsar_ra = '16h45m34s';      pulsar_dec = '+10d12m16s';     pulsar_DM = 36.17129; p_bar = 0.410860719
    elif 'J1646-1910' in pulsar_name:
        pulsar_ra = '16h46m19s';      pulsar_dec = '-19d10m14s';     pulsar_DM = 55.0;     p_bar = 4.81773583
    elif 'J1649+2533' in pulsar_name:
        pulsar_ra = '16h49m44s';      pulsar_dec = '+25d33m07s';     pulsar_DM = 34.4622;  p_bar = 1.015257392
    elif 'J1650-1654' in pulsar_name:
        pulsar_ra = '16h50m27s';      pulsar_dec = '-16d54m42s';     pulsar_DM = 43.25;    p_bar = 1.749551746

    elif 'J1651+14' in pulsar_name:
        pulsar_ra = '16h51m00s';      pulsar_dec = '+14d22m00s';     pulsar_DM = 48.0;     p_bar = 0.8280
    elif 'B1648-17' in pulsar_name:
        pulsar_ra = '16h51m32s';      pulsar_dec = '-17d09m22s';     pulsar_DM = 33.46;    p_bar = 0.973393692
    elif 'J1652-1400' in pulsar_name:
        pulsar_ra = '16h52m17s';      pulsar_dec = '-14d00m27s';     pulsar_DM = 49.5;     p_bar = 0.305447058
    elif 'J1652+2651' in pulsar_name:
        pulsar_ra = '16h52m03s';      pulsar_dec = '+26d51m40s';     pulsar_DM = 40.80244; p_bar = 0.915803497
    elif 'J1656+00' in pulsar_name:
        pulsar_ra = '16h56m41s';      pulsar_dec = '+00d26m00s';     pulsar_DM = 46.9;     p_bar = 1.49785

    elif 'J1656+6203' in pulsar_name:
        pulsar_ra = '16h56m10s';      pulsar_dec = '+62d03m50s';     pulsar_DM = 35.262;   p_bar = 0.776155311
    elif 'B1657-13' in pulsar_name:
        pulsar_ra = '16h59m53s';      pulsar_dec = '-13d05m09s';     pulsar_DM = 60.37;    p_bar = 0.6409582
    elif 'J1700-0954' in pulsar_name:
        pulsar_ra = '17h00m03s';      pulsar_dec = '-09d54m43s';     pulsar_DM = 64.1;     p_bar = 0.817311602
    elif 'J1703-18' in pulsar_name:
        pulsar_ra = '17h03m26s';      pulsar_dec = '-18d48m54s';     pulsar_DM = 46.0;     p_bar = 1.27024
    elif 'B1700-18' in pulsar_name:
        pulsar_ra = '17h03m51s';      pulsar_dec = '-18d46m15s';     pulsar_DM = 49.551;   p_bar = 0.804341079

    elif 'J1705-04' in pulsar_name:
        pulsar_ra = '17h05m00s';      pulsar_dec = '-04d41m00s';     pulsar_DM = 42.951;   p_bar = 0.23748
    elif 'J1706+59' in pulsar_name:
        pulsar_ra = '17h07m00s';      pulsar_dec = '+59d10m00s';     pulsar_DM = 30.8;     p_bar = 1.476687
    elif 'B1709-15' in pulsar_name:
        pulsar_ra = '17h11m55s';      pulsar_dec = '-15d09m40s';     pulsar_DM = 59.88;    p_bar = 0.868804249
    elif 'J1713+7810' in pulsar_name:
        pulsar_ra = '17h13m27s';      pulsar_dec = '+78d10m34s';     pulsar_DM = 36.977;   p_bar = 0.432525935
    elif 'J1714-1054' in pulsar_name:
        pulsar_ra = '17h14m40s';      pulsar_dec = '-10d54m11s';     pulsar_DM = 51.0;     p_bar = 0.696278743

    elif 'J1720+00' in pulsar_name:
        pulsar_ra = '17h20m55s';      pulsar_dec = '+00d40m00s';     pulsar_DM = 46.2;     p_bar = 3.357
    elif 'B1718-02' in pulsar_name:
        pulsar_ra = '17h20m57s';      pulsar_dec = '-02d12m24s';     pulsar_DM = 66.98;    p_bar = 0.477715344
    elif 'B1717-16' in pulsar_name:
        pulsar_ra = '17h20m25s';      pulsar_dec = '-16d33m34s';     pulsar_DM = 44.83;    p_bar = 1.565601148
    elif 'J1720+2150' in pulsar_name:
        pulsar_ra = '17h20m01s';      pulsar_dec = '+21d50m13s';     pulsar_DM = 40.719;   p_bar = 1.61566378
    elif 'B1718-19' in pulsar_name:
        pulsar_ra = '17h21m01s';      pulsar_dec = '-19d36m51s';     pulsar_DM = 75.7;     p_bar = 1.004037457

    elif 'J1721-1939' in pulsar_name:
        pulsar_ra = '17h21m47s';      pulsar_dec = '-19d39m49s';     pulsar_DM = 103.0;    p_bar = 0.404039751
    elif 'J1725-0732' in pulsar_name:
        pulsar_ra = '17h25m12s';      pulsar_dec = '-07d32m59s';     pulsar_DM = 58.72;    p_bar = 0.239919487
    elif 'J1726-00' in pulsar_name:
        pulsar_ra = '17h26m23s';      pulsar_dec = '-00d15m00s';     pulsar_DM = 57.0;     p_bar = 1.3086
    elif 'B1726-00' in pulsar_name:
        pulsar_ra = '17h28m35s';      pulsar_dec = '-00d07m45s';     pulsar_DM = 41.09;    p_bar = 0.386003724
    elif 'J1732-1930' in pulsar_name:
        pulsar_ra = '17h32m20s';      pulsar_dec = '-19d30m09s';     pulsar_DM = 72.43;    p_bar = 0.483769998

    elif 'B1732-02' in pulsar_name:
        pulsar_ra = '17h34m46s';      pulsar_dec = '-02d12m39s';     pulsar_DM = 65.05;    p_bar = 0.839394325
    elif 'J1735-0243' in pulsar_name:
        pulsar_ra = '17h35m48s';      pulsar_dec = '-02d43m48s';     pulsar_DM = 54.9;     p_bar = 0.782886977
    elif 'B1732-07' in pulsar_name:
        pulsar_ra = '17h35m05s';      pulsar_dec = '-07d24m52s';     pulsar_DM = 73.512;   p_bar = 0.419334966
    elif 'J1735+6320' in pulsar_name:
        pulsar_ra = '17h35m07s';      pulsar_dec = '+63d20m00s';     pulsar_DM = 41.853;   p_bar = 0.510718135
    elif 'J1736+05' in pulsar_name:
        pulsar_ra = '17h36m54s';      pulsar_dec = '+05d48m00s';     pulsar_DM = 42.0;     p_bar = 0.999245

    elif 'J1739+0612' in pulsar_name:
        pulsar_ra = '17h39m18s';      pulsar_dec = '+06d12m28s';     pulsar_DM = 95.52;    p_bar = 0.234169036
    elif 'J1739-1313' in pulsar_name:
        pulsar_ra = '17h39m58s';      pulsar_dec = '-13d13m19s';     pulsar_DM = 58.2;     p_bar = 1.215697614
    elif 'B1737+13' in pulsar_name:
        pulsar_ra = '17h40m07s';      pulsar_dec = '+13d11m57s';     pulsar_DM = 48.66823; p_bar = 0.803050265
    elif 'J1740+27' in pulsar_name:
        pulsar_ra = '17h40m30s';      pulsar_dec = '+27d13m00s';     pulsar_DM = 35.46;    p_bar = 1.0582
    elif 'B1738-08' in pulsar_name:
        pulsar_ra = '17h41m23s';      pulsar_dec = '-08d40m32s';     pulsar_DM = 74.90;    p_bar = 2.043082458

    elif 'J1741+3855' in pulsar_name:
        pulsar_ra = '17h41m12s';      pulsar_dec = '+38d55m10s';     pulsar_DM = 47.224;   p_bar = 0.82886089
    elif 'B1740-03' in pulsar_name:
        pulsar_ra = '17h43m08s';      pulsar_dec = '-03d39m12s';     pulsar_DM = 30.26;    p_bar = 0.444645107
    elif 'J1743+05' in pulsar_name:
        pulsar_ra = '17h43m16s';      pulsar_dec = '+05d29m00s';     pulsar_DM = 56.1;     p_bar = 1.47363
    elif 'B1740-13' in pulsar_name:
        pulsar_ra = '17h43m38s';      pulsar_dec = '-13d51m38s';     pulsar_DM = 116.30;   p_bar = 0.405336949
    elif 'J1744-1610' in pulsar_name:
        pulsar_ra = '17h44m17s';      pulsar_dec = '-16d10m36s';     pulsar_DM = 66.67;    p_bar = 1.757205869

    elif 'J1745-0129' in pulsar_name:
        pulsar_ra = '17h45m02s';      pulsar_dec = '-01d29m18s';     pulsar_DM = 89.3;     p_bar = 1.045406856
    elif 'J1745+1252' in pulsar_name:
        pulsar_ra = '17h45m44s';      pulsar_dec = '+12d52m38s';     pulsar_DM = 66.141;   p_bar = 1.059848758
    elif 'J1745+42' in pulsar_name:
        pulsar_ra = '17h45m48s';      pulsar_dec = '+42d53m00s';     pulsar_DM = 38.00;    p_bar = 0.3051
    elif 'J1746+2245' in pulsar_name:
        pulsar_ra = '17h46m01s';      pulsar_dec = '+22d45m29s';     pulsar_DM = 49.8543;  p_bar = 3.465037783
    elif 'J1746+2540' in pulsar_name:
        pulsar_ra = '17h46m07s';      pulsar_dec = '+25d40m38s';     pulsar_DM = 51.2044;  p_bar = 1.05814817

    elif 'B1745-12' in pulsar_name:
        pulsar_ra = '17h48m17s';      pulsar_dec = '-13d00m52s';     pulsar_DM = 99.364;   p_bar = 0.394133347
    elif 'J1749+16' in pulsar_name:
        pulsar_ra = '17h49m29s';      pulsar_dec = '+16d24m00s';     pulsar_DM = 59.6;     p_bar = 2.31165
    elif 'J1749+5952' in pulsar_name:
        pulsar_ra = '17h49m33s';      pulsar_dec = '+59d52m36s';     pulsar_DM = 45.0694;  p_bar = 0.436040951
    elif 'J1750+07' in pulsar_name:
        pulsar_ra = '17h50m40s';      pulsar_dec = '+07d33m00s';     pulsar_DM = 55.4;     p_bar = 1.90881
    elif 'J1752+2359' in pulsar_name:
        pulsar_ra = '17h52m35s';      pulsar_dec = '+23d59m48s';     pulsar_DM = 36.19635; p_bar = 0.409050865

    elif 'J1753-12' in pulsar_name:
        pulsar_ra = '17h52m53s';      pulsar_dec = '-12d59m00s';     pulsar_DM = 73.2;     p_bar = 0.405454
    elif 'B1753+52' in pulsar_name:
        pulsar_ra = '17h54m23s';      pulsar_dec = '+52d01m12s';     pulsar_DM = 35.0096;  p_bar = 2.391396795
    elif 'J1755-0903' in pulsar_name:
        pulsar_ra = '17h55m10s';      pulsar_dec = '-09d03m52s';     pulsar_DM = 63.67;    p_bar = 0.190709643
    elif 'J1756+1822' in pulsar_name:
        pulsar_ra = '17h56m18s';      pulsar_dec = '+18d22m55s';     pulsar_DM = 70.80;    p_bar = 0.74400094
    elif 'J1758+3030' in pulsar_name:
        pulsar_ra = '17h58m26s';      pulsar_dec = '+30d30m24s';     pulsar_DM = 35.0674;  p_bar = 0.947255811

    elif 'J1759-1029' in pulsar_name:
        pulsar_ra = '17h59m34s';      pulsar_dec = '-10d29m57s';     pulsar_DM = 115.4;    p_bar = 2.512262812
    elif 'J1800-0125' in pulsar_name:
        pulsar_ra = '18h00m22s';      pulsar_dec = '-01d25m31s';     pulsar_DM = 51.0;     p_bar = 0.78318549
    elif 'J1802+0128' in pulsar_name:
        pulsar_ra = '18h02m27s';      pulsar_dec = '+01d28m24s';     pulsar_DM = 97.97;    p_bar = 0.554261604
    elif 'J1802+03' in pulsar_name:
        pulsar_ra = '18h02m44s';      pulsar_dec = '+03d38m00s';     pulsar_DM = 77.0;     p_bar = 0.6643

    elif 'J1806+1023' in pulsar_name:
        pulsar_ra = '18h06m52s';      pulsar_dec = '+10d23m18s';     pulsar_DM = 52.03;    p_bar = 0.48428646
    elif 'J1807+04' in pulsar_name:
        pulsar_ra = '18h07m25s';      pulsar_dec = '+04d05m00s';     pulsar_DM = 53.0;     p_bar = 0.7989
    elif 'J1807+0756' in pulsar_name:
        pulsar_ra = '18h07m51s';      pulsar_dec = '+07d56m43s';     pulsar_DM = 89.29;    p_bar = 0.464300493
    elif 'B1804-08' in pulsar_name:
        pulsar_ra = '18h07m38s';      pulsar_dec = '-08d47m43s';     pulsar_DM = 112.3802; p_bar = 0.163727372
    elif 'J1809+17' in pulsar_name:
        pulsar_ra = '18h09m06s';      pulsar_dec = '+17d04m00s';     pulsar_DM = 47.32;    p_bar = 2.0667

    elif 'J1810+0705' in pulsar_name:
        pulsar_ra = '18h10m47s';      pulsar_dec = '+07d05m36s';     pulsar_DM = 79.425;   p_bar = 0.307682834
    elif 'J1811+0702' in pulsar_name:
        pulsar_ra = '18h11m20s';      pulsar_dec = '+07d02m30s';     pulsar_DM = 57.8;     p_bar = 0.461712677
    elif 'B1810+02' in pulsar_name:
        pulsar_ra = '18h12m53s';      pulsar_dec = '+02d26m57s';     pulsar_DM = 104.14;   p_bar = 0.793902802
    elif 'J1813+1822' in pulsar_name:
        pulsar_ra = '18h13m39s';      pulsar_dec = '+18d22m15s';     pulsar_DM = 60.8;     p_bar = 0.336424676
    elif 'B1811+40' in pulsar_name:
        pulsar_ra = '18h13m13s';      pulsar_dec = '+40d13m39s';     pulsar_DM = 41.55656; p_bar = 0.931089085

    elif 'J1814+1130' in pulsar_name:
        pulsar_ra = '18h14m43s';      pulsar_dec = '+11d30m44s';     pulsar_DM = 65.0;     p_bar = 0.751261115
    elif 'J1814+22' in pulsar_name:
        pulsar_ra = '18h14m36s';      pulsar_dec = '+22d23m00s';     pulsar_DM = 62.313;   p_bar = 0.2537
    elif 'J1815+5546' in pulsar_name:
        pulsar_ra = '18h15m06s';      pulsar_dec = '+55d46m23s';     pulsar_DM = 58.999;   p_bar = 0.426843827
    elif 'J1816-0755' in pulsar_name:
        pulsar_ra = '18h16m25s';      pulsar_dec = '-07d55m23s';     pulsar_DM = 117.90;   p_bar = 0.217642691
    elif 'J1819+1305' in pulsar_name:
        pulsar_ra = '18h19m56s';      pulsar_dec = '+13d05m15s';     pulsar_DM = 64.808;   p_bar = 1.060363544

    elif 'J1819-1318' in pulsar_name:
        pulsar_ra = '18h19m44s';      pulsar_dec = '-13d18m42s';     pulsar_DM = 35.1;     p_bar = 1.515695993
    elif 'J1819-17' in pulsar_name:
        pulsar_ra = '18h19m30s';      pulsar_dec = '-17d05m00s';     pulsar_DM = 67.0;     p_bar = 2.352135
    elif 'B1818-04' in pulsar_name:
        pulsar_ra = '18h20m53s';      pulsar_dec = '-04d27m38s';     pulsar_DM = 84.435;   p_bar = 0.598081935
    elif 'J1820-0509' in pulsar_name:
        pulsar_ra = '18h20m23s';      pulsar_dec = '-05d09m39s';     pulsar_DM = 102.40;   p_bar = 0.337320796
    elif 'J1821-0256' in pulsar_name:
        pulsar_ra = '18h21m10s';      pulsar_dec = '-02d56m39s';     pulsar_DM = 84.0;     p_bar = 0.41411105

    elif 'J1821+1715' in pulsar_name:
        pulsar_ra = '18h21m14s';      pulsar_dec = '+17d15m47s';     pulsar_DM = 60.2844;  p_bar = 1.366682059
    elif 'J1821+4147' in pulsar_name:
        pulsar_ra = '18h21m52s';      pulsar_dec = '+41d47m03s';     pulsar_DM = 40.673;   p_bar = 1.261857209
    elif 'J1822+02' in pulsar_name:
        pulsar_ra = '18h22m00s';      pulsar_dec = '+02d00m00s';     pulsar_DM = 103.8;    p_bar = 1.508
    elif 'J1822+0705' in pulsar_name:
        pulsar_ra = '18h22m18s';      pulsar_dec = '+07d05m19s';     pulsar_DM = 62.2;     p_bar = 1.362817392
    elif 'J1822+1120' in pulsar_name:
        pulsar_ra = '18h22m15s';      pulsar_dec = '+11d20m56s';     pulsar_DM = 95.2;     p_bar = 1.787036805

    elif 'B1821+05' in pulsar_name:
        pulsar_ra = '18h23m31s';      pulsar_dec = '+05d50m24s';     pulsar_DM = 66.775;   p_bar = 0.752906543
    elif 'J1824-0127' in pulsar_name:
        pulsar_ra = '18h24m53s';      pulsar_dec = '-01d27m51s';     pulsar_DM = 63.00;    p_bar = 2.499469846
    elif 'J1824-0132' in pulsar_name:
        pulsar_ra = '18h24m56s';      pulsar_dec = '-01d32m24s';     pulsar_DM = 79.0;     p_bar = 0.22372852
    elif 'B1822+00' in pulsar_name:
        pulsar_ra = '18h25m15s';      pulsar_dec = '+00d04m20s';     pulsar_DM = 56.618;   p_bar = 0.7789494
    elif 'J1828+1221' in pulsar_name:
        pulsar_ra = '18h28m22s';      pulsar_dec = '+12d21m21s';     pulsar_DM = 69.1;     p_bar = 1.528295081

    elif 'J1828+1359' in pulsar_name:
        pulsar_ra = '18h28m53s';      pulsar_dec = '+13d59m35s';     pulsar_DM = 56.0;     p_bar = 0.74163952
    elif 'J1829+0000' in pulsar_name:
        pulsar_ra = '18h29m47s';      pulsar_dec = '+00d00m09s';     pulsar_DM = 116.8;    p_bar = 0.199147397
    elif 'J1830-0131' in pulsar_name:
        pulsar_ra = '18h30m20s';      pulsar_dec = '-01d31m48s';     pulsar_DM = 95.7;     p_bar = 0.152511958
    elif 'J1832+0029' in pulsar_name:
        pulsar_ra = '18h32m51s';      pulsar_dec = '+00d29m27s';     pulsar_DM = 32.7;     p_bar = 0.533917733
    elif 'J1832+27' in pulsar_name:
        pulsar_ra = '18h32m10s';      pulsar_dec = '+27d58m00s';     pulsar_DM = 46.0;     p_bar = 0.6318

    elif 'B1831-00' in pulsar_name:
        pulsar_ra = '18h34m17s';      pulsar_dec = '-00d10m53s';     pulsar_DM = 88.65;    p_bar = 0.520954311
    elif 'B1831-04' in pulsar_name:
        pulsar_ra = '18h34m26s';      pulsar_dec = '-04d26m16s';     pulsar_DM = 79.308;   p_bar = 0.290108193
    elif 'J1834+10' in pulsar_name:
        pulsar_ra = '18h34m27s';      pulsar_dec = '+10d44m00s';     pulsar_DM = 78.479;   p_bar = 1.172719
    elif 'J1835-1020' in pulsar_name:
        pulsar_ra = '18h35m58s';      pulsar_dec = '-10d20m05s';     pulsar_DM = 115.90;   p_bar = 0.302449584
    elif 'J1837-0045' in pulsar_name:
        pulsar_ra = '18h37m32s';      pulsar_dec = '-00d45m11s';     pulsar_DM = 86.98;    p_bar = 0.617036696

    elif 'J1837+1221' in pulsar_name:
        pulsar_ra = '18h37m07s';      pulsar_dec = '+12d21m54s';     pulsar_DM = 100.6;    p_bar = 1.963531984
    elif 'J1837-1837' in pulsar_name:
        pulsar_ra = '18h37m54s';      pulsar_dec = '-18d37m08s';     pulsar_DM = 100.74;   p_bar = 0.618357697
    elif 'J1838+1523' in pulsar_name:
        pulsar_ra = '18h38m47s';      pulsar_dec = '+15d23m25s';     pulsar_DM = 68.26;    p_bar = 0.549160602
    elif 'J1838+1650' in pulsar_name:
        pulsar_ra = '18h38m43s';      pulsar_dec = '+16d50m16s';     pulsar_DM = 32.95162; p_bar = 1.901967399
    elif 'J1839-0627' in pulsar_name:
        pulsar_ra = '18h39m20s';      pulsar_dec = '-06d27m34s';     pulsar_DM = 92.49;    p_bar = 0.484913679

    elif 'B1839+09' in pulsar_name:
        pulsar_ra = '18h41m56s';      pulsar_dec = '+09d12m07s';     pulsar_DM = 49.1579;  p_bar = 0.381319294
    elif 'J1842+0358' in pulsar_name:
        pulsar_ra = '18h42m17s';      pulsar_dec = '+03d58m35s';     pulsar_DM = 109.9;    p_bar = 0.233326207
    elif 'J1842+1332' in pulsar_name:
        pulsar_ra = '18h42m30s';      pulsar_dec = '+13d32m02s';     pulsar_DM = 102.5;    p_bar = 0.471603579
    elif 'J1843-0000' in pulsar_name:
        pulsar_ra = '18h43m28s';      pulsar_dec = '-00d00m42s';     pulsar_DM = 101.8;    p_bar = 0.880334322
    elif 'J1843+2024' in pulsar_name:
        pulsar_ra = '18h43m26s';      pulsar_dec = '+20d24m55s';     pulsar_DM = 85.3;     p_bar = 3.406538671

    elif 'B1842+14' in pulsar_name:
        pulsar_ra = '18h44m55s';      pulsar_dec = '+14d54m14s';     pulsar_DM = 41.48555; p_bar = 0.375463379
    elif 'J1844+41' in pulsar_name:
        pulsar_ra = '18h44m45s';      pulsar_dec = '+41d17m00s';     pulsar_DM = 50.0;     p_bar = 0.9157
    elif 'J1845+0623' in pulsar_name:
        pulsar_ra = '18h45m09s';      pulsar_dec = '+06d23m58s';     pulsar_DM = 113.0;    p_bar = 1.421653784
    elif 'J1848-0023' in pulsar_name:
        pulsar_ra = '18h48m38s';      pulsar_dec = '-00d23m17s';     pulsar_DM = 34.9;     p_bar = 0.537623733
    elif 'J1848+0127g' in pulsar_name:
        pulsar_ra = '18h48m19s';     pulsar_dec = '+01d27m00s';     pulsar_DM = 77.0;     p_bar = 0.53402

    elif 'J1848+0826' in pulsar_name:
        pulsar_ra = '18h48m44s';      pulsar_dec = '+08d26m36s';     pulsar_DM = 90.677;   p_bar = 0.328664727
    elif 'J1848-1243' in pulsar_name:
        pulsar_ra = '18h48m18s';      pulsar_dec = '-12d43m30s';     pulsar_DM = 91.96;    p_bar = 0.414383354
    elif 'J1848+1516' in pulsar_name:
        pulsar_ra = '18h48m56s';      pulsar_dec = '+15d16m44s';     pulsar_DM = 77.436;   p_bar = 2.233769775
    elif 'J1849-0317' in pulsar_name:
        pulsar_ra = '18h49m58s';      pulsar_dec = '-03d17m31s';     pulsar_DM = 40.0;     p_bar = 0.668407829
    elif 'J1849+0409' in pulsar_name:
        pulsar_ra = '18h49m03s';      pulsar_dec = '+04d09m42s';     pulsar_DM = 63.97;    p_bar = 0.761194082

    elif 'J1849-0614' in pulsar_name:
        pulsar_ra = '18h49m45s';      pulsar_dec = '-06d14m32s';     pulsar_DM = 118.2;    p_bar = 0.953384188
    elif 'J1849+2423' in pulsar_name:
        pulsar_ra = '18h49m35s';      pulsar_dec = '+24d23m46s';     pulsar_DM = 62.2677;  p_bar = 0.275641499
    elif 'J1849+2559' in pulsar_name:
        pulsar_ra = '18h49m48s';      pulsar_dec = '+25d59m58s';     pulsar_DM = 75.0016;  p_bar = 0.519263406
    elif 'B1848+13' in pulsar_name:
        pulsar_ra = '18h50m35s';      pulsar_dec = '+13d35m58s';     pulsar_DM = 60.1396;  p_bar = 0.345581898
    elif 'B1848+04' in pulsar_name:
        pulsar_ra = '18h51m03s';      pulsar_dec = '+04d18m12s';     pulsar_DM = 115.54;   p_bar = 0.284697472

    elif 'B1848+12' in pulsar_name:
        pulsar_ra = '18h51m13s';      pulsar_dec = '+12d59m35s';     pulsar_DM = 70.6333;  p_bar = 1.205303285
    elif 'J1852+0857g' in pulsar_name:
        pulsar_ra = '18h52m37s';     pulsar_dec = '+08d57m00s';     pulsar_DM = 85.9;     p_bar = 3.77214
    elif 'J1853-0649' in pulsar_name:
        pulsar_ra = '18h53m25s';      pulsar_dec = '-06d49m26s';     pulsar_DM = 44.541;   p_bar = 1.048132105
    elif 'J1855+0235g' in pulsar_name:
        pulsar_ra = '18h55m49s';     pulsar_dec = '+02d35m00s';     pulsar_DM = 103.3;    p_bar = 0.98303
    elif 'B1853+01' in pulsar_name:
        pulsar_ra = '18h56m11s';      pulsar_dec = '+01d13m21s';     pulsar_DM = 96.1;     p_bar = 0.26743961

    elif 'J1856+0211g' in pulsar_name:
        pulsar_ra = '18h56m53s';     pulsar_dec = '+02d11m00s';     pulsar_DM = 113.9;    p_bar = 9.89012
    elif 'B1854+00' in pulsar_name:
        pulsar_ra = '18h57m01s';      pulsar_dec = '+00d57m17s';     pulsar_DM = 82.39;    p_bar = 0.356928998
    elif 'J1857-1027' in pulsar_name:
        pulsar_ra = '18h57m27s';      pulsar_dec = '-10d27m01s';     pulsar_DM = 108.9;    p_bar = 3.687219048
    elif 'J1859+1526' in pulsar_name:
        pulsar_ra = '18h59m44s';      pulsar_dec = '+15d26m11s';     pulsar_DM = 97.45;    p_bar = 0.933971582
    elif 'J1859+7654' in pulsar_name:
        pulsar_ra = '18h59m36s';      pulsar_dec = '+76d54m56s';     pulsar_DM = 47.25;    p_bar = 1.393729135

    elif 'J1900+30' in pulsar_name:
        pulsar_ra = '19h00m18s';      pulsar_dec = '+30d53m00s';     pulsar_DM = 71.8352;  p_bar = 0.602227
    elif 'B1859+01' in pulsar_name:
        pulsar_ra = '19h01m34s';      pulsar_dec = '+01d56m38s';     pulsar_DM = 105.394;  p_bar = 0.288219159
    elif 'J1901-0312' in pulsar_name:
        pulsar_ra = '19h01m16s';      pulsar_dec = '-03d12m30s';     pulsar_DM = 106.6;    p_bar = 0.355725187
    elif 'J1901+0621' in pulsar_name:
        pulsar_ra = '19h01m06s';      pulsar_dec = '+06d21m19s';     pulsar_DM = 94.0;     p_bar = 0.832001949
    elif 'J1901-0906' in pulsar_name:
        pulsar_ra = '19h01m53s';      pulsar_dec = '-09d06m11s';     pulsar_DM = 72.677;   p_bar = 1.781927762

    elif 'J1901+1306' in pulsar_name:
        pulsar_ra = '19h01m49s';      pulsar_dec = '+13d06m48s';     pulsar_DM = 75.0988;  p_bar = 1.830857453
    elif 'J1902-0340' in pulsar_name:
        pulsar_ra = '19h02m51s';      pulsar_dec = '-03d40m18s';     pulsar_DM = 114.0;    p_bar = 1.524672106
    elif 'J1902+0723' in pulsar_name:
        pulsar_ra = '19h02m14s';      pulsar_dec = '+07d23m51s';     pulsar_DM = 105.0;    p_bar = 0.4878126283
    elif 'J1902-1036' in pulsar_name:
        pulsar_ra = '19h02m42s';      pulsar_dec = '-10d36m13s';     pulsar_DM = 96.3;     p_bar = 0.786813538431
    elif 'J1903-0258' in pulsar_name:
        pulsar_ra = '19h03m30s';      pulsar_dec = '-02d58m16s';     pulsar_DM = 114.10;   p_bar = 0.301458774079

    elif 'J1903-0848' in pulsar_name:
        pulsar_ra = '19h03m11s';      pulsar_dec = '-08d48m57s';     pulsar_DM = 66.99;    p_bar = 0.88732464056
    elif 'J1903+0851g' in pulsar_name:
        pulsar_ra = '19h03m04s';     pulsar_dec = '+08d51m00s';     pulsar_DM = 78.9;     p_bar = 1.23197
    elif 'J1903+2225' in pulsar_name:
        pulsar_ra = '19h03m53s';      pulsar_dec = '+22d25m12s';     pulsar_DM = 109.20;   p_bar = 0.65118538418
    elif 'J1904+0519g' in pulsar_name:
        pulsar_ra = '19h04m08s';     pulsar_dec = '+05d19m00s';     pulsar_DM = 80.8;     p_bar = 1.68053
    elif 'J1904+0535g' in pulsar_name:
        pulsar_ra = '19h04m52s';     pulsar_dec = '+05d35m00s';     pulsar_DM = 78.4;     p_bar = 0.60376

    elif 'J1904+0823g' in pulsar_name:
        pulsar_ra = '19h04m44s';     pulsar_dec = '+08d23m00s';     pulsar_DM = 60.4;     p_bar = 1.50773
    elif 'J1904-1224' in pulsar_name:
        pulsar_ra = '19h04m33s';      pulsar_dec = '-12d24m01s';     pulsar_DM = 118.23;   p_bar = 0.75080812238
    elif 'J1906+0509' in pulsar_name:
        pulsar_ra = '19h06m56s';      pulsar_dec = '+05d09m36s';     pulsar_DM = 99.5;     p_bar = 0.39758968304
    elif 'J1907+0602' in pulsar_name:
        pulsar_ra = '19h07m55s';      pulsar_dec = '+06d02m17s';     pulsar_DM = 82.1;     p_bar = 0.106632746266
    elif 'J1907-1532' in pulsar_name:
        pulsar_ra = '19h07m07s';      pulsar_dec = '-15d32m15s';     pulsar_DM = 72.6;     p_bar = 0.63223532885

    elif 'B1905+39' in pulsar_name:
        pulsar_ra = '19h07m35s';      pulsar_dec = '+40d02m06s';     pulsar_DM = 30.966;   p_bar = 1.235757452781
    elif 'J1907+57' in pulsar_name:
        pulsar_ra = '19h07m00s';      pulsar_dec = '+57d00m00s';     pulsar_DM = 54.63;    p_bar = 0.424
    elif 'J1908+2351' in pulsar_name:
        pulsar_ra = '19h08m32s';      pulsar_dec = '+23d51m42s';     pulsar_DM = 101.695;  p_bar = 0.377578026
    elif 'B1907+00' in pulsar_name:
        pulsar_ra = '19h09m35s';      pulsar_dec = '+00d07m58s';     pulsar_DM = 112.787;  p_bar = 1.01694836198
    elif 'J1909+0641' in pulsar_name:
        pulsar_ra = '19h09m29s';      pulsar_dec = '+06d41m26s';     pulsar_DM = 36.7;     p_bar = 0.741761952452

    elif 'J1909+0657g' in pulsar_name:
        pulsar_ra = '19h09m14s';     pulsar_dec = '+06d57m00s';     pulsar_DM = 59.9;     p_bar = 1.24589
    elif 'J1909+1450' in pulsar_name:
        pulsar_ra = '19h09m27s';      pulsar_dec = '+14d50m58s';     pulsar_DM = 119.5;    p_bar = 0.9961077952
    elif 'J1909+1859' in pulsar_name:
        pulsar_ra = '19h09m19s';      pulsar_dec = '+18d59m11s';     pulsar_DM = 64.517;   p_bar = 0.54245109601
    elif 'B1907+03' in pulsar_name:
        pulsar_ra = '19h10m09s';      pulsar_dec = '+03d58m28s';     pulsar_DM = 82.93;    p_bar = 2.33026282052
    elif 'J1910-0556' in pulsar_name:
        pulsar_ra = '19h10m17s';      pulsar_dec = '-05d56m30s';     pulsar_DM = 88.3;     p_bar = 0.557609248

    elif 'J1911+00' in pulsar_name:
        pulsar_ra = '19h11m48s';      pulsar_dec = '+00d37m00s';     pulsar_DM = 100.0;    p_bar = 6.94
    elif 'J1911+1758' in pulsar_name:
        pulsar_ra = '19h11m55s';      pulsar_dec = '+17d58m46s';     pulsar_DM = 48.98;    p_bar = 0.46040581878
    elif 'B1910+20' in pulsar_name:
        pulsar_ra = '19h12m43s';      pulsar_dec = '+21d04m34s';     pulsar_DM = 88.5961;  p_bar = 2.232969028273
    elif 'J1912+2525' in pulsar_name:
        pulsar_ra = '19h12m19s';      pulsar_dec = '+25d25m02s';     pulsar_DM = 37.8474;  p_bar = 0.62197624506
    elif 'B1911-04' in pulsar_name:
        pulsar_ra = '19h13m54s';      pulsar_dec = '-04d40m48s';     pulsar_DM = 89.385;   p_bar = 0.825935803096

    elif 'J1913+0446' in pulsar_name:
        pulsar_ra = '19h13m51s';      pulsar_dec = '+04d46m06s';     pulsar_DM = 75.65;    p_bar = 0.315
    elif 'J1913+0904' in pulsar_name:
        pulsar_ra = '19h13m21s';      pulsar_dec = '+09d04m45s';     pulsar_DM = 95.3;     p_bar = 0.163245785775
    elif 'J1913+3732' in pulsar_name:
        pulsar_ra = '19h13m28s';      pulsar_dec = '+37d32m12s';     pulsar_DM = 72.3263;  p_bar = 0.851078948902
    elif 'J1914+0631' in pulsar_name:
        pulsar_ra = '19h14m17s';      pulsar_dec = '+06d31m56s';     pulsar_DM = 58.0;     p_bar = 0.69381120574
    elif 'J1914+1029g' in pulsar_name:
        pulsar_ra = '19h14m23s';     pulsar_dec = '+10d29m00s';     pulsar_DM = 59.7;     p_bar = 2.48499

    elif 'B1911+11' in pulsar_name:
        pulsar_ra = '19h14m10s';      pulsar_dec = '+11d22m04s';     pulsar_DM = 100.0;    p_bar = 0.60099749634
    elif 'J1915+0738' in pulsar_name:
        pulsar_ra = '19h15m25s';      pulsar_dec = '+07d38m31s';     pulsar_DM = 39.00;    p_bar = 1.54270444942
    elif 'J1915+0752' in pulsar_name:
        pulsar_ra = '19h15m02s';      pulsar_dec = '+07d52m09s';     pulsar_DM = 105.3;    p_bar = 2.05831378861
    elif 'J1915+0832g' in pulsar_name:
        pulsar_ra = '19h15m06s';     pulsar_dec = '+08d32m00s';     pulsar_DM = 36.2;     p_bar = 2.71009
    elif 'J1915-11' in pulsar_name:
        pulsar_ra = '19h15m00s';      pulsar_dec = '-11d30m00s';     pulsar_DM = 91.06;    p_bar = 2.1770

    elif 'B1913+167' in pulsar_name:
        pulsar_ra = '19h15m19s';      pulsar_dec = '+16d47m09s';     pulsar_DM = 62.57;    p_bar = 1.616231495126
    elif 'B1914+09' in pulsar_name:
        pulsar_ra = '19h16m32s';      pulsar_dec = '+09d51m26s';     pulsar_DM = 60.953;   p_bar = 0.2702544395645
    elif 'J1916+3224' in pulsar_name:
        pulsar_ra = '19h16m03s';      pulsar_dec = '+32d24m40s';     pulsar_DM = 84.105;   p_bar = 1.13744972551
    elif 'B1915+13' in pulsar_name:
        pulsar_ra = '19h17m40s';      pulsar_dec = '+13d53m57s';     pulsar_DM = 94.538;   p_bar = 0.194630982798
    elif 'J1918-1052' in pulsar_name:
        pulsar_ra = '19h18m48s';      pulsar_dec = '-10d52m46s';     pulsar_DM = 62.73;    p_bar = 0.798692542358

    elif 'B1917+00' in pulsar_name:
        pulsar_ra = '19h19m51s';      pulsar_dec = '+00d21m40s';     pulsar_DM = 90.315;   p_bar = 1.27226037471
    elif 'J1919+2621' in pulsar_name:
        pulsar_ra = '19h19m41s';      pulsar_dec = '+26d21m29s';     pulsar_DM = 96.5;     p_bar = 0.65151209407
    elif 'J1920-0950' in pulsar_name:
        pulsar_ra = '19h20m56s';      pulsar_dec = '-09d50m01s';     pulsar_DM = 93.0;     p_bar = 1.037824001161
    elif 'J1921-05' in pulsar_name:
        pulsar_ra = '19h21m04s';      pulsar_dec = '-05d23m08s';     pulsar_DM = 80.7;     p_bar = 2.22759

    elif 'J1921-0510' in pulsar_name:
        pulsar_ra = '19h21m29s';      pulsar_dec = '-05d10m11s';     pulsar_DM = 96.6;     p_bar = 0.79425387952
    elif 'J1921+0812' in pulsar_name:
        pulsar_ra = '19h21m48s';      pulsar_dec = '+08d12m52s';     pulsar_DM = 84.0;     p_bar = 0.210648412102
    elif 'B1919+14' in pulsar_name:
        pulsar_ra = '19h21m24s';      pulsar_dec = '+14d19m17s';     pulsar_DM = 91.64;    p_bar = 0.618182590832
    elif 'B1919+20' in pulsar_name:
        pulsar_ra = '19h21m52s';      pulsar_dec = '+20d03m21s';     pulsar_DM = 101.0;    p_bar = 0.76068138902
    elif 'J1922+58' in pulsar_name:
        pulsar_ra = '19h22m00s';      pulsar_dec = '+58d28m00s';     pulsar_DM = 53.74;    p_bar = 0.529623

    elif 'J1923-0408' in pulsar_name:
        pulsar_ra = '19h23m11s';      pulsar_dec = '-04d08m19s';     pulsar_DM = 35.0;     p_bar = 1.14926937103
    elif 'J1923+4243' in pulsar_name:
        pulsar_ra = '19h23m15s';      pulsar_dec = '+42d43m19s';     pulsar_DM = 52.99;    p_bar = 0.595192858512
    elif 'J1924+1510g' in pulsar_name:
        pulsar_ra = '19h24m02s';     pulsar_dec = '+15d10m00s';     pulsar_DM = 115.6;    p_bar = 0.49863
    elif 'J1924+2037g' in pulsar_name:
        pulsar_ra = '19h24m34s';     pulsar_dec = '+20d37m00s';     pulsar_DM = 82.3;     p_bar = 0.68480
    elif 'J1925-16' in pulsar_name:
        pulsar_ra = '19h25m06s';      pulsar_dec = '-16d01m00s';     pulsar_DM = 88.0;     p_bar = 3.8858

    elif 'B1923+04' in pulsar_name:
        pulsar_ra = '19h26m24s';      pulsar_dec = '+04d31m32s';     pulsar_DM = 102.243;  p_bar = 1.074080076347
    elif 'J1926-0652' in pulsar_name:
        pulsar_ra = '19h26m37s';      pulsar_dec = '-06d52m43s';     pulsar_DM = 85.3;     p_bar = 1.608816302697
    elif 'J1926-1314' in pulsar_name:
        pulsar_ra = '19h26m54s';      pulsar_dec = '-13d14m04s';     pulsar_DM = 40.83;    p_bar = 4.86428379983
    elif 'B1925+188' in pulsar_name:
        pulsar_ra = '19h27m25s';      pulsar_dec = '+18d56m37s';     pulsar_DM = 99.0;     p_bar = 0.298313497249
    elif 'J1928+1443' in pulsar_name:
        pulsar_ra = '19h28m07s';      pulsar_dec = '+14d43m11s';     pulsar_DM = 101.0;    p_bar = 1.01073895346

    elif 'J1928+1839g' in pulsar_name:
        pulsar_ra = '19h28m38s';     pulsar_dec = '+18d39m00s';     pulsar_DM = 70.0;     p_bar = 2.26091
    elif 'J1929+00' in pulsar_name:
        pulsar_ra = '19h29m28s';      pulsar_dec = '+00d26m00s';     pulsar_DM = 42.95;    p_bar = 1.166900
    elif 'B1926+18' in pulsar_name:
        pulsar_ra = '19h29m17s';      pulsar_dec = '+18d45m00s';     pulsar_DM = 112.0;    p_bar = 1.22047000453
    elif 'J1929+2121' in pulsar_name:
        pulsar_ra = '19h29m04s';      pulsar_dec = '+21d21m23s';     pulsar_DM = 66.0;     p_bar = 0.723598503258
    elif 'J1929+3817' in pulsar_name:
        pulsar_ra = '19h29m07s';      pulsar_dec = '+38d17m58s';     pulsar_DM = 93.4;     p_bar = 0.81421524225

    elif 'J1929+62' in pulsar_name:
        pulsar_ra = '19h29m00s';      pulsar_dec = '+62d16m00s';     pulsar_DM = 67.7;     p_bar = 1.456004
    elif 'J1930-1852' in pulsar_name:
        pulsar_ra = '19h30m30s';      pulsar_dec = '-18d51m46s';     pulsar_DM = 42.8526;  p_bar = 0.18552016047926
    elif 'J1931-0144' in pulsar_name:
        pulsar_ra = '19h31m32s';      pulsar_dec = '-01d44m23s';     pulsar_DM = 38.3;     p_bar = 0.593661359781
    elif 'J1931+30' in pulsar_name:
        pulsar_ra = '19h31m28s';      pulsar_dec = '+30d35m00s';     pulsar_DM = 53.0;     p_bar = 0.582126
    elif 'J1932+1500' in pulsar_name:
        pulsar_ra = '19h32m46s';      pulsar_dec = '+15d00m22s';     pulsar_DM = 90.5;     p_bar = 1.86433186749

    elif 'J1933+1923g' in pulsar_name:
        pulsar_ra = '19h33m58s';     pulsar_dec = '+19d23m00s';     pulsar_DM = 97.7;     p_bar = 0.37173
    elif 'B1931+24' in pulsar_name:
        pulsar_ra = '19h33m38s';      pulsar_dec = '+24d36m40s';     pulsar_DM = 106.03;   p_bar = 0.81369030283
    elif 'J1933+5335' in pulsar_name:
        pulsar_ra = '19h33m01s';      pulsar_dec = '+53d35m43s';     pulsar_DM = 33.54;    p_bar = 2.052574490
    elif 'J1934+19' in pulsar_name:
        pulsar_ra = '19h34m18s';      pulsar_dec = '+19d26m00s';     pulsar_DM = 98.4;     p_bar = 0.23098462
    elif 'J1934+5219' in pulsar_name:
        pulsar_ra = '19h34m24s';      pulsar_dec = '+52d19m58s';     pulsar_DM = 71.26;    p_bar = 0.56844228297

    elif 'J1937-00' in pulsar_name:
        pulsar_ra = '19h37m09s';      pulsar_dec = '-00d17m00s';     pulsar_DM = 68.6;     p_bar = 0.2401
    elif 'B1935+25' in pulsar_name:
        pulsar_ra = '19h37m01s';      pulsar_dec = '+25d44m13s';     pulsar_DM = 53.221;   p_bar = 0.20098020244218
    elif 'J1937+2950' in pulsar_name:
        pulsar_ra = '19h37m48s';      pulsar_dec = '+29d50m02s';     pulsar_DM = 113.99;   p_bar = 1.65742878336
    elif 'J1938+0650' in pulsar_name:
        pulsar_ra = '19h37m53s';      pulsar_dec = '+06d50m06s';     pulsar_DM = 70.8;     p_bar = 1.121561892
    elif 'J1938+14' in pulsar_name:
        pulsar_ra = '19h38m07s';      pulsar_dec = '+15d06m00s';     pulsar_DM = 75.4;     p_bar = 2.902504

    elif 'J1938+2213' in pulsar_name:
        pulsar_ra = '19h38m14s';      pulsar_dec = '+22d13m13s';     pulsar_DM = 93.0;     p_bar = 0.1661155731566
    elif 'J1939+10' in pulsar_name:
        pulsar_ra = '19h39m11s';      pulsar_dec = '+10d45m00s';     pulsar_DM = 90.0;     p_bar = 2.31
    elif 'J1939+26' in pulsar_name:
        pulsar_ra = '19h39m42s';      pulsar_dec = '+26d09m00s';     pulsar_DM = 47.5;     p_bar = 0.4669615
    elif 'J1940+0239' in pulsar_name:
        pulsar_ra = '19h40m33s';      pulsar_dec = '+02d36m41s';     pulsar_DM = 87.2;     p_bar = 1.23224
    elif 'J1940-0902' in pulsar_name:
        pulsar_ra = '19h40m55s';      pulsar_dec = '-09d02m18s';     pulsar_DM = 42.3;     p_bar = 0.97846813844

    elif 'J1941+0121' in pulsar_name:
        pulsar_ra = '19h41m16s';      pulsar_dec = '+01d21m40s';     pulsar_DM = 51.87;    p_bar = 0.217317451828
    elif 'J1941+4320' in pulsar_name:
        pulsar_ra = '19h41m59s';      pulsar_dec = '+43d20m06s';     pulsar_DM = 79.361;   p_bar = 0.840906468392
    elif 'J1942+8106' in pulsar_name:
        pulsar_ra = '19h42m55s';      pulsar_dec = '+81d06m17s';     pulsar_DM = 40.24;    p_bar = 0.2035584528675
    elif 'J1943+0609' in pulsar_name:
        pulsar_ra = '19h43m29s';      pulsar_dec = '+06d09m58s';     pulsar_DM = 70.76;    p_bar = 0.446226281658
    elif 'J1944-10' in pulsar_name:
        pulsar_ra = '19h44m00s';      pulsar_dec = '-10d17m00s';     pulsar_DM = 31.01;    p_bar = 0.409135

    elif 'B1941-17' in pulsar_name:
        pulsar_ra = '19h44m05s';      pulsar_dec = '-17d50m11s';     pulsar_DM = 56.32;    p_bar = 0.841157774341
    elif 'B1942-00' in pulsar_name:
        pulsar_ra = '19h45m28s';      pulsar_dec = '-00d40m58s';     pulsar_DM = 59.71;    p_bar = 1.045632444772
    elif 'J1945+07' in pulsar_name:
        pulsar_ra = '19h45m55s';      pulsar_dec = '+07d17m00s';     pulsar_DM = 62.0;     p_bar = 1.0739
    elif 'J1945+1211' in pulsar_name:
        pulsar_ra = '19h45m12s';      pulsar_dec = '+12d11m46s';     pulsar_DM = 92.7;     p_bar = 4.7567963794
    elif 'J1946-1312' in pulsar_name:
        pulsar_ra = '19h46m58s';      pulsar_dec = '-13d12m36s';     pulsar_DM = 63.04;    p_bar = 0.491865489484

    elif 'J1946+14' in pulsar_name:
        pulsar_ra = '19h46m52s';      pulsar_dec = '+14d42m00s';     pulsar_DM = 50.3;     p_bar = 2.28244
    elif 'J1946+24' in pulsar_name:
        pulsar_ra = '19h46m00s';      pulsar_dec = '+23d58m00s';     pulsar_DM = 96.0;     p_bar = 4.729
    elif 'J1947+0915' in pulsar_name:
        pulsar_ra = '19h47m46s';      pulsar_dec = '+09d15m08s';     pulsar_DM = 94.0;     p_bar = 1.48074382424
    elif 'J1950+05' in pulsar_name:
        pulsar_ra = '19h50m58s';      pulsar_dec = '+05d35m00s';     pulsar_DM = 71.0;     p_bar = 0.455934
    elif 'J1951+1123' in pulsar_name:
        pulsar_ra = '19h51m08s';      pulsar_dec = '+11d23m25s';     pulsar_DM = 31.29;    p_bar = 5.0940830275

    elif 'B1949+14' in pulsar_name:
        pulsar_ra = '19h52m06s';      pulsar_dec = '+14d07m29s';     pulsar_DM = 31.5051;  p_bar = 0.27502568252
    elif 'J1953+30' in pulsar_name:
        pulsar_ra = '19h53m48s';      pulsar_dec = '+30d13m00s';     pulsar_DM = 43.61;    p_bar = 1.2712
    elif 'J1954+1021' in pulsar_name:
        pulsar_ra = '19h54m37s';      pulsar_dec = '+10d21m11s';     pulsar_DM = 80.87;    p_bar = 2.09944017034
    elif 'J1954+2407' in pulsar_name:
        pulsar_ra = '19h54m00s';      pulsar_dec = '+24d07m14s';     pulsar_DM = 80.5;     p_bar = 0.1934045707829
    elif 'J1954+3852' in pulsar_name:
        pulsar_ra = '19h54m01s';      pulsar_dec = '+38d52m16s';     pulsar_DM = 65.36;    p_bar = 0.352933478726

    elif 'B1953+50' in pulsar_name:
        pulsar_ra = '19h55m19s';      pulsar_dec = '+50d59m55s';     pulsar_DM = 31.98266; p_bar = 0.5189379874091
    elif 'J1956+07' in pulsar_name:
        pulsar_ra = '19h56m35s';      pulsar_dec = '+07d16m00s';     pulsar_DM = 61.3;     p_bar = 5.01248
    elif 'J1956+0838' in pulsar_name:
        pulsar_ra = '19h56m52s';      pulsar_dec = '+08d38m17s';     pulsar_DM = 67.087;   p_bar = 0.303910924347
    elif 'J1957-0002' in pulsar_name:
        pulsar_ra = '19h57m43s';      pulsar_dec = '-00d02m07s';     pulsar_DM = 38.443;   p_bar = 0.96509596606
    elif 'J1958+56' in pulsar_name:
        pulsar_ra = '19h58m00s';      pulsar_dec = '+56d49m00s';     pulsar_DM = 58.10;    p_bar = 0.3118

    elif 'J2001-0349' in pulsar_name:
        pulsar_ra = '20h01m53s';      pulsar_dec = '-03d49m44s';     pulsar_DM = 67.0;     p_bar = 1.34472401604
    elif 'J2001+4258' in pulsar_name:
        pulsar_ra = '20h01m11s';      pulsar_dec = '+42d58m06s';     pulsar_DM = 54.93;    p_bar = 0.719166137852
    elif 'J2002+1637' in pulsar_name:
        pulsar_ra = '20h02m48s';      pulsar_dec = '+16d37m17s';     pulsar_DM = 94.581;   p_bar = 0.27649748362
    elif 'J2005-0020' in pulsar_name:
        pulsar_ra = '20h05m44s';      pulsar_dec = '-00d20m22s';     pulsar_DM = 35.93;    p_bar = 2.27966105858
    elif 'B2003-08' in pulsar_name:
        pulsar_ra = '20h06m16s';      pulsar_dec = '-08d07m02s';     pulsar_DM = 32.39;    p_bar = 0.580871337031

    elif 'J2006+3102' in pulsar_name:
        pulsar_ra = '20h06m11s';      pulsar_dec = '+31d02m03s';     pulsar_DM = 107.16;   p_bar = 0.16369523645
    elif 'J2007+0809' in pulsar_name:
        pulsar_ra = '20h07m13s';      pulsar_dec = '+08d09m33s';     pulsar_DM = 53.394;   p_bar = 0.32572436605
    elif 'J2007+0910' in pulsar_name:
        pulsar_ra = '20h07m58s';      pulsar_dec = '+09d10m13s';     pulsar_DM = 48.72934; p_bar = 0.4587348258074
    elif 'J2007+20' in pulsar_name:
        pulsar_ra = '20h07m00s';      pulsar_dec = '+20d21m00s';     pulsar_DM = 67.0;     p_bar = 4.634
    elif 'J2008+2513' in pulsar_name:
        pulsar_ra = '20h08m35s';      pulsar_dec = '+25d13m30s';     pulsar_DM = 60.5555;  p_bar = 0.58919550332

    elif 'J2010+2845' in pulsar_name:
        pulsar_ra = '20h10m05s';      pulsar_dec = '+28d45m29s';     pulsar_DM = 112.47;   p_bar = 0.5653693451984
    elif 'J2013-0649' in pulsar_name:
        pulsar_ra = '20h13m18s';      pulsar_dec = '-06d49m05s';     pulsar_DM = 63.36;    p_bar = 0.580187269001
    elif 'J2017+2043' in pulsar_name:
        pulsar_ra = '20h17m29s';      pulsar_dec = '+20d43m32s';     pulsar_DM = 60.4906;  p_bar = 0.537143086032
    elif 'J2017+2819g' in pulsar_name:
        pulsar_ra = '20h17m20s';     pulsar_dec = '+28d19m00s';     pulsar_DM = 66.0;     p_bar = 1.83246
    elif 'J2017+5906' in pulsar_name:
        pulsar_ra = '20h17m45s';      pulsar_dec = '+59d06m47s';     pulsar_DM = 60.28;    p_bar = 0.403478334902

    elif 'J2022+21' in pulsar_name:
        pulsar_ra = '20h22m24s';      pulsar_dec = '+21d11m00s';     pulsar_DM = 73.52;    p_bar = 0.8035
    elif 'B2022+50' in pulsar_name:
        pulsar_ra = '20h23m42s';      pulsar_dec = '+50d37m35s';     pulsar_DM = 32.98817; p_bar = 0.372619054536
    elif 'J2024+48' in pulsar_name:
        pulsar_ra = '20h24m00s';      pulsar_dec = '+48d00m00s';     pulsar_DM = 99.0;     p_bar = 1.262
    elif 'B2025+21' in pulsar_name:
        pulsar_ra = '20h27m17s';      pulsar_dec = '+21d46m04s';     pulsar_DM = 97.0915;  p_bar = 0.398173021652
    elif 'B2028+22' in pulsar_name:
        pulsar_ra = '20h30m40s';      pulsar_dec = '+22d28m22s';     pulsar_DM = 71.8627;  p_bar = 0.630512646679

    elif 'J2030+55' in pulsar_name:
        pulsar_ra = '20h30m00s';      pulsar_dec = '+55d00m00s';     pulsar_DM = 59.43;    p_bar = 0.579
    elif 'J2032+4127' in pulsar_name:
        pulsar_ra = '20h32m13s';      pulsar_dec = '+41d27m24s';     pulsar_DM = 114.67;   p_bar = 0.14324647
    elif 'J2033+0042' in pulsar_name:
        pulsar_ra = '20h33m31s';      pulsar_dec = '+00d42m24s';     pulsar_DM = 37.84;    p_bar = 5.01340011141
    elif 'J2036+2835' in pulsar_name:
        pulsar_ra = '20h36m46s';      pulsar_dec = '+28d35m10s';     pulsar_DM = 84.2174;  p_bar = 1.35872676315
    elif 'J2036+6646' in pulsar_name:
        pulsar_ra = '20h36m52s';      pulsar_dec = '+66d46m21s';     pulsar_DM = 50.763;   p_bar = 0.5019271782

    elif 'B2034+19' in pulsar_name:
        pulsar_ra = '20h37m15s';      pulsar_dec = '+19d42m54s';     pulsar_DM = 36.891647; p_bar = 2.0743770781
    elif 'B2035+36' in pulsar_name:
        pulsar_ra = '20h37m27s';      pulsar_dec = '+36d21m24s';     pulsar_DM = 93.56;    p_bar = 0.61871508419
    elif 'J2038+35' in pulsar_name:
        pulsar_ra = '20h38m00s';      pulsar_dec = '+35d00m00s';     pulsar_DM = 57.91;    p_bar = 0.16
    elif 'J2040+1657' in pulsar_name:
        pulsar_ra = '20h40m18s';      pulsar_dec = '+16d57m30s';     pulsar_DM = 50.6919;  p_bar = 0.865606225032
    elif 'J2043+7045' in pulsar_name:
        pulsar_ra = '20h43m00s';      pulsar_dec = '+70d45m00s';     pulsar_DM = 57.64;    p_bar = 0.588

    elif 'J2044+28' in pulsar_name:
        pulsar_ra = '20h44m00s';      pulsar_dec = '+28d00m00s';     pulsar_DM = 90.3;     p_bar = 1.618
    elif 'J2045+0912' in pulsar_name:
        pulsar_ra = '20h45m47s';      pulsar_dec = '+09d12m29s';     pulsar_DM = 31.776;   p_bar = 0.3955551117394
    elif 'B2043-04' in pulsar_name:
        pulsar_ra = '20h46m00s';      pulsar_dec = '-04d21m26s';     pulsar_DM = 35.799;   p_bar = 1.5469381168652
    elif 'B2044+15' in pulsar_name:
        pulsar_ra = '20h46m39s';      pulsar_dec = '+15d40m34s';     pulsar_DM = 39.81796; p_bar = 1.1382856833155
    elif 'B2045+56' in pulsar_name:
        pulsar_ra = '20h46m47s';      pulsar_dec = '+57d08m37s';     pulsar_DM = 101.790291; p_bar = 0.476734842147

    elif 'J2047+5029' in pulsar_name:
        pulsar_ra = '20h47m55s';      pulsar_dec = '+50d29m38s';     pulsar_DM = 107.676;  p_bar = 0.445944557385
    elif 'J2048+2255' in pulsar_name:
        pulsar_ra = '20h48m46s';      pulsar_dec = '+22d55m05s';     pulsar_DM = 70.6847;  p_bar = 0.2839009641977
    elif 'J2050+1259' in pulsar_name:
        pulsar_ra = '20h50m57s';      pulsar_dec = '+12d59m09s';     pulsar_DM = 52.40;    p_bar = 1.2210199818
    elif 'J2051+1248' in pulsar_name:
        pulsar_ra = '20h51m30s';      pulsar_dec = '+12d48m22s';     pulsar_DM = 43.45;    p_bar = 0.55316745256
    elif 'B2053+21' in pulsar_name:
        pulsar_ra = '20h55m39s';      pulsar_dec = '+22d09m27s';     pulsar_DM = 36.34963; p_bar = 0.8151811027646

    elif 'B2053+36' in pulsar_name:
        pulsar_ra = '20h55m31s';      pulsar_dec = '+36d30m21s';     pulsar_DM = 97.4155;  p_bar = 0.221507638277
    elif 'J2057+21' in pulsar_name:
        pulsar_ra = '20h57m48s';      pulsar_dec = '+21d26m00s';     pulsar_DM = 73.31;    p_bar = 1.1667
    elif 'J2102+38' in pulsar_name:
        pulsar_ra = '21h02m00s';      pulsar_dec = '+38d00m00s';     pulsar_DM = 86.3;     p_bar = 1.19
    elif 'J2105+07' in pulsar_name:
        pulsar_ra = '21h05m27s';      pulsar_dec = '+07d57m00s';     pulsar_DM = 52.6;     p_bar = 3.74663
    elif 'J2105+28' in pulsar_name:
        pulsar_ra = '21h06m00s';      pulsar_dec = '+28d29m00s';     pulsar_DM = 62.48;    p_bar = 0.405737

    elif 'J2105+6223' in pulsar_name:
        pulsar_ra = '21h05m13s';      pulsar_dec = '+62d23m06s';     pulsar_DM = 50.75;    p_bar = 2.30487883766
    elif 'J2108+4516' in pulsar_name:
        pulsar_ra = '21h08m00s';      pulsar_dec = '+45d16m00s';     pulsar_DM = 83.54;    p_bar = 0.5772309434487
    #   elif 'J2108+4516_1' in pulsar_name: pulsar_ra = '21h08m00s';     pulsar_dec = '+45d16m00s';     pulsar_DM = 82.520;   p_bar = 0.5772309434487
    elif 'J2111+2106' in pulsar_name:
        pulsar_ra = '21h11m33s';      pulsar_dec = '+21d06m07s';     pulsar_DM = 59.2964;  p_bar = 3.9538529596
    elif 'J2113+67' in pulsar_name:
        pulsar_ra = '21h14m00s';      pulsar_dec = '+67d02m00s';     pulsar_DM = 54.98;    p_bar = 0.5521697
    elif 'B2113+14' in pulsar_name:
        pulsar_ra = '21h16m14s';      pulsar_dec = '+14d14m21s';     pulsar_DM = 56.2044;  p_bar = 0.4401530669475

    elif 'J2123+36' in pulsar_name:
        pulsar_ra = '21h23m48s';      pulsar_dec = '+36d24m00s';     pulsar_DM = 108.7;    p_bar = 1.2940
    elif 'J2123+5434' in pulsar_name:
        pulsar_ra = '21h23m22s';      pulsar_dec = '+54d34m08s';     pulsar_DM = 31.760;   p_bar = 0.13886807258911
    elif 'B2122+13' in pulsar_name:
        pulsar_ra = '21h24m47s';      pulsar_dec = '+14d07m19s';     pulsar_DM = 30.2473;  p_bar = 0.694053479086
    elif 'B2127+11A' in pulsar_name:
        pulsar_ra = '21h29m58s';      pulsar_dec = '+12d10m01s';     pulsar_DM = 67.31;    p_bar = 0.11066470446904
    elif 'J2137+6428' in pulsar_name:
        pulsar_ra = '21h37m20s';      pulsar_dec = '+64d28m42s';     pulsar_DM = 106.0;    p_bar = 1.75098916325

    elif 'J2139+00' in pulsar_name:
        pulsar_ra = '21h39m42s';      pulsar_dec = '+00d36m00s';     pulsar_DM = 31.18;    p_bar = 0.312470
    elif 'J2139+2242' in pulsar_name:
        pulsar_ra = '21h39m27s';      pulsar_dec = '+22d42m42s';     pulsar_DM = 44.15971; p_bar = 1.08351351364
    elif 'J2155+2813' in pulsar_name:
        pulsar_ra = '21h55m16s';      pulsar_dec = '+28d13m12s';     pulsar_DM = 77.1309;  p_bar = 1.6090199964
    elif 'J2156+2618' in pulsar_name:
        pulsar_ra = '21h56m24s';      pulsar_dec = '+26d18m30s';     pulsar_DM = 48.4433;  p_bar = 0.49814907254
    elif 'B2154+40' in pulsar_name:
        pulsar_ra = '21h57m02s';      pulsar_dec = '+40d17m46s';     pulsar_DM = 71.1239;  p_bar = 1.525265633965

    elif 'J2203+50' in pulsar_name:
        pulsar_ra = '22h03m00s';      pulsar_dec = '+50d00m00s';     pulsar_DM = 77.0;     p_bar = 0.745
    elif 'J2205+1444' in pulsar_name:
        pulsar_ra = '22h05m17s';      pulsar_dec = '+14d44m31s';     pulsar_DM = 36.717;   p_bar = 0.93801422813
    elif 'J2208+5500' in pulsar_name:
        pulsar_ra = '22h08m24s';      pulsar_dec = '+55d00m08s';     pulsar_DM = 105.21;   p_bar = 0.93316251394
    elif 'J2209+22' in pulsar_name:
        pulsar_ra = '22h09m54s';      pulsar_dec = '+21d17m00s';     pulsar_DM = 46.30;    p_bar = 1.7769
    elif 'B2210+29' in pulsar_name:
        pulsar_ra = '22h12m23s';      pulsar_dec = '+29d33m05s';     pulsar_DM = 74.5213;  p_bar = 1.004592528853

    elif 'B2217+47' in pulsar_name:
        pulsar_ra = '22h19m48s';      pulsar_dec = '+47d54m54s';     pulsar_DM = 43.4975;  p_bar = 0.5384688219194
    elif 'J2222+2923' in pulsar_name:
        pulsar_ra = '22h23m03s';      pulsar_dec = '+29d23m59s';     pulsar_DM = 49.4128;  p_bar = 0.2813991427542
    elif 'J2225+35' in pulsar_name:
        pulsar_ra = '22h24m48s';      pulsar_dec = '+35d30m00s';     pulsar_DM = 51.8;     p_bar = 0.94
    elif 'B2224+65' in pulsar_name:
        pulsar_ra = '22h25m53s';      pulsar_dec = '+65d35m36s';     pulsar_DM = 36.44362; p_bar = 0.682542497406
    elif 'J2234+2114' in pulsar_name:
        pulsar_ra = '22h34m57s';      pulsar_dec = '+21d14m19s';     pulsar_DM = 35.08;    p_bar = 1.35874531269

    elif 'J2241+6941' in pulsar_name:
        pulsar_ra = '22h41m20s';      pulsar_dec = '+69d42m00s';     pulsar_DM = 67.67;    p_bar = 0.855401265709
    elif 'B2241+69' in pulsar_name:
        pulsar_ra = '22h42m56s';      pulsar_dec = '+69d50m52s';     pulsar_DM = 40.86039; p_bar = 1.664500786185
    elif 'J2243+1518' in pulsar_name:
        pulsar_ra = '22h43m10s';      pulsar_dec = '+15d18m25s';     pulsar_DM = 42.13;    p_bar = 0.596799464458
    elif 'J2244+63' in pulsar_name:
        pulsar_ra = '22h44m00s';      pulsar_dec = '+63d00m00s';     pulsar_DM = 92.15;    p_bar = 0.461
    elif 'B2303+30' in pulsar_name:
        pulsar_ra = '23h05m58s';      pulsar_dec = '+31d00m01s';     pulsar_DM = 49.5845;  p_bar = 1.575886338359

    elif 'B2303+46' in pulsar_name:
        pulsar_ra = '23h05m56s';      pulsar_dec = '+47d07m45s';     pulsar_DM = 62.0676;  p_bar = 1.066371071565
    elif 'J2306+31' in pulsar_name:
        pulsar_ra = '23h06m12s';      pulsar_dec = '+31d23m00s';     pulsar_DM = 46.13;    p_bar = 0.3416
    elif 'B2306+55' in pulsar_name:
        pulsar_ra = '23h08m14s';      pulsar_dec = '+55d47m36s';     pulsar_DM = 46.53905; p_bar = 0.4750676748022
    elif 'J2310+6706' in pulsar_name:
        pulsar_ra = '23h10m42s';      pulsar_dec = '+67d06m52s';     pulsar_DM = 97.7;     p_bar = 1.9447889728
    elif 'J2312+6931' in pulsar_name:
        pulsar_ra = '23h12m39s';      pulsar_dec = '+69d31m04s';     pulsar_DM = 71.6;     p_bar = 0.813374778317

    elif 'J2315+58' in pulsar_name:
        pulsar_ra = '23h15m00s';      pulsar_dec = '+58d00m00s';     pulsar_DM = 73.2;     p_bar = 1.061
    elif 'B2319+60' in pulsar_name:
        pulsar_ra = '23h21m55s';      pulsar_dec = '+60d24m31s';     pulsar_DM = 94.591;   p_bar = 2.256488426824
    elif 'J2326+6141' in pulsar_name:
        pulsar_ra = '23h26m00s';      pulsar_dec = '+61d00m00s';     pulsar_DM = 34.5;     p_bar = 0.79
    elif 'J2329+16' in pulsar_name:
        pulsar_ra = '23h29m50s';      pulsar_dec = '+16d57m00s';     pulsar_DM = 31.0;     p_bar = 0.6321
    elif 'J2329+4743' in pulsar_name:
        pulsar_ra = '23h29m32s';      pulsar_dec = '+47d43m40s';     pulsar_DM = 44.012;   p_bar = 0.728408609085

    elif 'B2334+61' in pulsar_name:
        pulsar_ra = '23h37m06s';      pulsar_dec = '+61d51m02s';     pulsar_DM = 58.410;   p_bar = 0.495369868028
    elif 'J2343+6221' in pulsar_name:
        pulsar_ra = '23h43m00s';      pulsar_dec = '+62d21m00s';     pulsar_DM = 116.6;    p_bar = 1.799
    elif 'J2350+31' in pulsar_name:
        pulsar_ra = '23h50m42s';      pulsar_dec = '+31d39m00s';     pulsar_DM = 39.14;    p_bar = 0.5081
    elif 'J2351+8533' in pulsar_name:
        pulsar_ra = '23h51m03s';      pulsar_dec = '+85d33m21s';     pulsar_DM = 38.2;     p_bar = 1.01172719111
    elif 'B2351+61' in pulsar_name:
        pulsar_ra = '23h54m05s';      pulsar_dec = '+61d55m47s';     pulsar_DM = 94.662;   p_bar = 0.944783886655

    # LOTAAS

    elif 'J1958+21' in pulsar_name:
        pulsar_ra = '19h58m23s';      pulsar_dec = '+21d52m32s';     pulsar_DM = 87.7;     p_bar = 1.0504058

    elif 'J1342+65' in pulsar_name:
        pulsar_ra = '13h42m51s';      pulsar_dec = '+65d40m10s';     pulsar_DM = 38.7;     p_bar = 0.12248054
    elif 'J1838+00' in pulsar_name:
        pulsar_ra = '18h38m05s';      pulsar_dec = '+00d00m00s';     pulsar_DM = 98.2;     p_bar = 0.127823611

    #

    elif 'B0136+57' in pulsar_name:
        pulsar_ra = '01h39m20s';      pulsar_dec = '+58d14m32s';     pulsar_DM = 73.81141;     p_bar = 0.272450631
    elif 'B0523+11' in pulsar_name:
        pulsar_ra = '05h25m56s';      pulsar_dec = '+11d15m19s';     pulsar_DM = 79.418;     p_bar = 0.354437595
    elif 'J2351+8533' in pulsar_name:
        pulsar_ra = '23h51m03s';      pulsar_dec = '+85d33m21s';     pulsar_DM = 38.5;     p_bar = 1.011727191

    ################## From Igor Kravtsov ########################^

    else: print('   !!! Source not found !!!')

    return pulsar_ra, pulsar_dec, pulsar_DM, p_bar


################################################################################
################################################################################


if __name__ == '__main__':

    pulsar_ra, pulsar_dec, DM, p_bar = catalogue_pulsar('j0006+1834')

    print(' Pulsar coordinates are:       ', pulsar_ra, pulsar_dec)
    print(' Pulsar dispersion measure is: ', DM, ' pc*cm-3')
    print(' Pulsar period is:             ', p_bar, ' s.')
