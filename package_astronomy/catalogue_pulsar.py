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
        pulsar_ra = '0h13m16s';      pulsar_dec = '+29d49m18s';     pulsar_DM = 36.2;     p_bar = 1.5
    elif 'J0027+84' in pulsar_name:
        pulsar_ra = '0h27m16s';      pulsar_dec = '+84d17m23s';     pulsar_DM = 9.65;     p_bar = 1.5
    elif 'J0034+27' in pulsar_name:
        pulsar_ra = '0h34m57s';      pulsar_dec = '+27d47m00s';     pulsar_DM = 16.0;     p_bar = 1.5
    elif 'J0053+6938' in pulsar_name:
        pulsar_ra = '00h53m13s';     pulsar_dec = '+69d39m03s';     pulsar_DM = 90.3;     p_bar = 1.16
    elif 'J0054+6650' in pulsar_name:
        pulsar_ra = '0h54m55.41s';   pulsar_dec = '+66d50m23.8s';   pulsar_DM = 14.550974; p_bar = 1.39017001799
    elif 'J0103+54' in pulsar_name:
        pulsar_ra = '1h03m37s';      pulsar_dec = '+54d02m00s';     pulsar_DM = 55.605;   p_bar = 0.354304
    elif 'J0121+5329' in pulsar_name:
        pulsar_ra = '1h21m19s';      pulsar_dec = '+53d29m24s';     pulsar_DM = 87.35;    p_bar = 2.7255
    elif 'J0156+04' in pulsar_name:
        pulsar_ra = '1h56m01s';      pulsar_dec = '+4d02m0s';       pulsar_DM = 27.5;     p_bar = 1.5
    elif 'J0201+7005' in pulsar_name:
        pulsar_ra = '2h01m41s';      pulsar_dec = '70d05m18s';      pulsar_DM = 21.029;   p_bar = 1.349184471846
    elif 'J0203+7022' in pulsar_name:
        pulsar_ra = '02h03m28s';     pulsar_dec = '+70d22m44s';     pulsar_DM = 21.0;     p_bar = 1.35
    elif 'J0209+58' in pulsar_name:
        pulsar_ra = '02h09m12s';     pulsar_dec = '+58d12m01s';     pulsar_DM = 56.0;     p_bar = 1.0637
    elif 'J0226+3356' in pulsar_name:
        pulsar_ra = '2h27m08s';      pulsar_dec = '+33d55m44s';     pulsar_DM = 27.397;   p_bar = 1.2401
    elif 'J0253+52' in pulsar_name:
        pulsar_ra = '2h53m35s';      pulsar_dec = '+52d43m18s';     pulsar_DM = 28.5757810804579;     p_bar = 1.5
    elif 'J0301+20' in pulsar_name:
        pulsar_ra = '3h01m04s';      pulsar_dec = '20d52m33s';      pulsar_DM = 19.0;     p_bar = 1.207
    elif 'J0305+4001' in pulsar_name:
        pulsar_ra = '3h05m26s';      pulsar_dec = '40d01m0s';       pulsar_DM = 24;       p_bar = 1.5
    elif 'J0317+1328' in pulsar_name:
        pulsar_ra = '3h17m54s';      pulsar_dec = '13d29m0s';       pulsar_DM = 12.7452;  p_bar = 1.9742
    elif 'J0327+09' in pulsar_name:
        pulsar_ra = '3h27m58s';      pulsar_dec = '9d35m6s';        pulsar_DM = 93.68;    p_bar = 1.5
    elif 'J0332+7910' in pulsar_name:
        pulsar_ra = '3h32m45s';      pulsar_dec = '79d10m00s ';     pulsar_DM = 16.589;   p_bar = 2.0562
    elif 'J0348+79' in pulsar_name:
        pulsar_ra = '3h48m18s';      pulsar_dec = '+79d18m26s';     pulsar_DM = 26.09;    p_bar = 1.5
    elif 'J0357-05' in pulsar_name:
        pulsar_ra = '03h57m56s';     pulsar_dec = '-05d09m44s';     pulsar_DM = 56.4;     p_bar = 2.0
    elif 'J0441-04' in pulsar_name:
        pulsar_ra = '4h41m0s';       pulsar_dec = '-04d18m00s';     pulsar_DM = 20.0;     p_bar = 1.5
    elif 'J0447-04' in pulsar_name:
        pulsar_ra = '4h47m0s';       pulsar_dec = '-04d35m00s';     pulsar_DM = 29.83;    p_bar = 2.18819
    elif 'J0452+1651' in pulsar_name:
        pulsar_ra = '4h52m0s';       pulsar_dec = '16d51m0s';       pulsar_DM = 18.5;     p_bar = 1.5
    elif 'J0503+22' in pulsar_name:
        pulsar_ra = '5h03m0s';       pulsar_dec = '+22d20m00s';     pulsar_DM = 92;       p_bar = 1.5
    elif 'J0513-04' in pulsar_name:
        pulsar_ra = '5h13m0s';       pulsar_dec = '-04d18m00s';     pulsar_DM = 18.5;     p_bar = 1.5
    elif 'J0517+24' in pulsar_name:
        pulsar_ra = '05h17m55s';     pulsar_dec = '+24d30m38s';     pulsar_DM = 74.3;     p_bar = 1.5
    elif 'J0534+3407' in pulsar_name:
        pulsar_ra = '05h34m30s';     pulsar_dec = '+34d07m0s';      pulsar_DM = 24.5;     p_bar = 1.5
    elif 'J0544+20' in pulsar_name:
        pulsar_ra = '5h44m12s';      pulsar_dec = '-20d50m00s';     pulsar_DM = 56.9;     p_bar = 1.5
    elif 'J0545-03' in pulsar_name:
        pulsar_ra = '5h45m0s';       pulsar_dec = '-03d10m00s';     pulsar_DM = 67.2;     p_bar = 1.5
    elif 'J0550+09' in pulsar_name:
        pulsar_ra = '5h50m28s';      pulsar_dec = '9d51m0s';        pulsar_DM = 86.6;     p_bar = 1.745
    elif 'J0609+1635' in pulsar_name:
        pulsar_ra = '06h09m13s';     pulsar_dec = '16d34m0s';       pulsar_DM = 85;       p_bar = 1.5
    elif 'J0614-03' in pulsar_name:
        pulsar_ra = '06h15m00s';     pulsar_dec = '-03d29m00s';     pulsar_DM = 17.9;     p_bar = 0.136
    elif 'J0625+1730' in pulsar_name:
        pulsar_ra = '06h25m19s';     pulsar_dec = '17d30m0s';       pulsar_DM = 58;       p_bar = 1.5
    elif 'J0627+16' in pulsar_name:
        pulsar_ra = '6h27m13s';      pulsar_dec = '16d12m0s';       pulsar_DM = 113;      p_bar = 2.180
    elif 'J0628+09' in pulsar_name:
        pulsar_ra = '6h28m36s';      pulsar_dec = '9d09m14s';       pulsar_DM = 88.3;     p_bar = 1.241
    elif 'J0630+19' in pulsar_name:
        pulsar_ra = '6h30m4s';       pulsar_dec = '19d37m30s';      pulsar_DM = 48.3;     p_bar = 1.24855
    elif 'J0630+25' in pulsar_name:
        pulsar_ra = '06h31m00s';     pulsar_dec = '+25d23m14s';     pulsar_DM = 22.3;     p_bar = 1.5
    elif 'J0653-06' in pulsar_name:
        pulsar_ra = '06h53m00s';     pulsar_dec = '-06d16m00s';     pulsar_DM = 83.7;     p_bar = 0.79
    elif 'J0658+29' in pulsar_name:
        pulsar_ra = '06h58m06s';     pulsar_dec = '+29d32m08s';     pulsar_DM = 40.05;    p_bar = 0.82
    elif 'J0658-15' in pulsar_name:
        pulsar_ra = '06h58m55s';     pulsar_dec = '-15d16m50s';     pulsar_DM = 57.6;     p_bar = 1.5
    elif 'J0741+17' in pulsar_name:
        pulsar_ra = '07h41m00';      pulsar_dec = '17d03m00s';      pulsar_DM = 44.3;     p_bar = 1.73
    elif 'J0746+55' in pulsar_name:
        pulsar_ra = '07h46m48s';     pulsar_dec = '+55d14m33s';     pulsar_DM = 10.326333; p_bar = 2.89378549447
    elif 'J0803+3410' in pulsar_name:
        pulsar_ra = '8h03m05s';      pulsar_dec = '34d19m0s';       pulsar_DM = 34;       p_bar = 1.5
    elif 'J0812+8626' in pulsar_name:
        pulsar_ra = '08h12m30s';     pulsar_dec = '86d26m00s';      pulsar_DM = 40.25;    p_bar = 1.5
    elif 'J0845-03' in pulsar_name:
        pulsar_ra = '08h45m00s';     pulsar_dec = '-03d34m48s';     pulsar_DM = 14.15;    p_bar = 1.5
    elif 'J0854+54' in pulsar_name:
        pulsar_ra = '08h54m24';      pulsar_dec = '54d48m00s';      pulsar_DM = 17.8;     p_bar = 1.2329

    #     elif 'J0854+54_1' in pulsar_name: pulsar_ra = '08h54m24s';      pulsar_dec = '54d48m00s';       pulsar_DM = 18.843;   p_bar = 1.2330

    elif 'J0939+45' in pulsar_name:
        pulsar_ra = '09h39m31s';     pulsar_dec = '45d15m00s';      pulsar_DM = 17.45;   p_bar = 1.5
    elif 'J0941+1621' in pulsar_name:
        pulsar_ra = '09h43m30s';     pulsar_dec = '16d31m00';       pulsar_DM = 23.5;    p_bar = 1.5
    elif 'J0957-06' in pulsar_name:
        pulsar_ra = '09h57m00s';     pulsar_dec = '-6d17m00s';      pulsar_DM = 26.95;   p_bar = 1.72370
    elif 'J1010+15' in pulsar_name:
        pulsar_ra = '10h10m00s';     pulsar_dec = '15d0m00s';       pulsar_DM = 42.15;   p_bar = 1.5
    elif 'J1048+53' in pulsar_name:
        pulsar_ra = '10h48m28s';     pulsar_dec = '53d41m49s';      pulsar_DM = 30.85;   p_bar = 1.5
    elif 'J1059-01' in pulsar_name:
        pulsar_ra = '10h59m00s';     pulsar_dec = '-1d2m00s';       pulsar_DM = 18.7;    p_bar = 1.5
    elif 'J1105+02' in pulsar_name:
        pulsar_ra = '11h05m32s';     pulsar_dec = '2d28m50s';       pulsar_DM = 16.5;    p_bar = 6.403055372
    elif 'J1130+09' in pulsar_name:
        pulsar_ra = '11h30m55s';     pulsar_dec = '09d20m00s';      pulsar_DM = 21.9;    p_bar = 4.796636974

    #    elif 'J1130+09_1' in pulsar_name: pulsar_ra = '11h30m55s';      pulsar_dec = '09d20m00s';       pulsar_DM = 21.0;    p_bar = 4.796636974

    elif 'J1132+0921' in pulsar_name:
        pulsar_ra = '11h32m00s';     pulsar_dec = '09d21m00s';      pulsar_DM = 22.0;    p_bar = 1.5
    elif 'J1156-1318' in pulsar_name:
        pulsar_ra = '11h56m42s';     pulsar_dec = '-13d18m22s';     pulsar_DM = 28.0;    p_bar = 1.5
    elif 'J1246+53' in pulsar_name:
        pulsar_ra = '12h51m48s';     pulsar_dec = '53d41m24s';      pulsar_DM = 21.03;   p_bar = 1.5
    elif 'J1326+33' in pulsar_name:
        pulsar_ra = '13h26m42s';     pulsar_dec = '33d46m00s';      pulsar_DM = 4.19;    p_bar = 0.0415
    elif 'J1332-03' in pulsar_name:
        pulsar_ra = '13h32m00s';     pulsar_dec = '-3d26m00s';      pulsar_DM = 27.1;    p_bar = 1.10640
    elif 'J1336-20' in pulsar_name:
        pulsar_ra = '13h36m00s';     pulsar_dec = '-20d34m00s';     pulsar_DM = 19.3;    p_bar = 0.184
    elif 'J1336+3346' in pulsar_name:
        pulsar_ra = '13h36m34s';     pulsar_dec = '34d14m38s';      pulsar_DM = 8.4688;  p_bar = 1.50660326546

    #    elif 'J1336+3346_1' in pulsar_name: pulsar_ra = '13h36m34s';    pulsar_dec = '34d14m38s';       pulsar_DM = 8.4688;  p_bar = 3.013

    elif 'J1346+06' in pulsar_name:
        pulsar_ra = '13h46m11s';     pulsar_dec = '06d10m00s';      pulsar_DM = 9.0;     p_bar = 1.5
    elif 'J1354+2454' in pulsar_name:
        pulsar_ra = '13h54m00s';     pulsar_dec = '24d54m00s';      pulsar_DM = 20.1;    p_bar = 0.85106

    #    elif 'J1354+2454_1' in pulsar_name: pulsar_ra = '13h54m00s';    pulsar_dec = '24d54m00s';       pulsar_DM = 20.1;    p_bar = 6.27

    elif 'J1404+1210' in pulsar_name:
        pulsar_ra = '14h04m36s';     pulsar_dec = '11d59m00s';      pulsar_DM = 18.53;   p_bar = 2.6504
    elif 'J1430+22' in pulsar_name:
        pulsar_ra = '14h30m01s';     pulsar_dec = '22d24m24s';      pulsar_DM = 23.32;   p_bar = 1.5
    elif 'J1432+09' in pulsar_name:
        pulsar_ra = '14h32m30s';     pulsar_dec = '09d08m00s';      pulsar_DM = 14.0;    p_bar = 1.5
    elif 'J1433+00' in pulsar_name:
        pulsar_ra = '14h33m30s';     pulsar_dec = '00d28m00s';      pulsar_DM = 23.5;    p_bar = 1.5
    elif 'J1439+7655' in pulsar_name:
        pulsar_ra = '14h39m00s';     pulsar_dec = '76d55m00s';      pulsar_DM = 22.29;   p_bar = 0.948
    elif 'J1502+2813' in pulsar_name:
        pulsar_ra = '15h02m09s';     pulsar_dec = '28d13m00s';      pulsar_DM = 14.0;    p_bar = 3.784
    elif 'J1524-20' in pulsar_name:
        pulsar_ra = '15h24m44s';     pulsar_dec = '-20d59m21s';     pulsar_DM = 40.1;    p_bar = 1.5
    elif 'J1532+00' in pulsar_name:
        pulsar_ra = '15h32m40s';     pulsar_dec = '00d42m00s';      pulsar_DM = 12.3;    p_bar = 1.5
    elif 'J1538+2345' in pulsar_name:
        pulsar_ra = '15h38m06s';     pulsar_dec = '23d45m04s';      pulsar_DM = 6.9;     p_bar = 3.44938495332
    elif 'J1541+47' in pulsar_name:
        pulsar_ra = '15h41m00s';     pulsar_dec = '47d03m00s';      pulsar_DM = 19.4;    p_bar = 0.277700692893
    elif 'J1550+0943' in pulsar_name:
        pulsar_ra = '15h50m47s';     pulsar_dec = '09d43m00s';      pulsar_DM = 21.0;    p_bar = 0.28
    elif 'J1554+18' in pulsar_name:
        pulsar_ra = '15h54m17s';     pulsar_dec = '18d04m00s';      pulsar_DM = 23.94;   p_bar = 1.5
    elif 'J1555+0108' in pulsar_name:
        pulsar_ra = '15h55m58s';     pulsar_dec = '01d08m00s';      pulsar_DM = 18.0;    p_bar = 1.5
    elif 'J1603+18' in pulsar_name:
        pulsar_ra = '16h03m34s';     pulsar_dec = '18d51m00s';      pulsar_DM = 29.7;    p_bar = 0.503
    elif 'J1603-1655' in pulsar_name:
        pulsar_ra = '16h03m09s';     pulsar_dec = '-16d55m28s';     pulsar_DM = 63.22;   p_bar = 0.7147
    elif 'J1611-01' in pulsar_name:
        pulsar_ra = '16h11m00s';     pulsar_dec = '-1d28m00s';      pulsar_DM = 27.21;   p_bar = 1.29687
    elif 'J1610-17' in pulsar_name:
        pulsar_ra = '16h10m11s';     pulsar_dec = '-17d50m00s';     pulsar_DM = 52.5;    p_bar = 1.3
    elif 'J1623-0841' in pulsar_name:
        pulsar_ra = '16h23m43s';     pulsar_dec = '-8d41m37s';      pulsar_DM = 59.79;   p_bar = 0.503045281599
    elif 'J1639+21' in pulsar_name:
        pulsar_ra = '16h39m40s';     pulsar_dec = '21d59m30s';      pulsar_DM = 14.4;    p_bar = 0.79073276630
    elif 'J1640-09' in pulsar_name:
        pulsar_ra = '16h40m17s';     pulsar_dec = '-9d15m49s';      pulsar_DM = 50.2;    p_bar = 1.5
    elif 'J1705-04' in pulsar_name:
        pulsar_ra = '17h05m00s';     pulsar_dec = '-4d41m0s';       pulsar_DM = 42.951;  p_bar = 0.23748
    elif 'J1717+03' in pulsar_name:
        pulsar_ra = '17h17m56s';     pulsar_dec = '3d11m00s';       pulsar_DM = 25.6;    p_bar = 3.901
    elif 'J1720+00' in pulsar_name:
        pulsar_ra = '17h20m55s';     pulsar_dec = '0d40m00s';       pulsar_DM = 46.2;    p_bar = 3.353
    elif 'J1722+31' in pulsar_name:
        pulsar_ra = '17h22m0s';      pulsar_dec = '31d00m00s';      pulsar_DM = 109.88;  p_bar = 1.5
    elif 'J1732+2700' in pulsar_name:
        pulsar_ra = '17h32m24s';     pulsar_dec = '27d00m00s';      pulsar_DM = 36.0;    p_bar = 1.5
    elif 'J1737+24' in pulsar_name:
        pulsar_ra = '17h37m00s';     pulsar_dec = '24d00m00s';      pulsar_DM = 59.80;   p_bar = 2.449
    elif 'J1753-12' in pulsar_name:
        pulsar_ra = '17h52m53s';     pulsar_dec = '-12d59m00s';     pulsar_DM = 73.2;    p_bar = 0.405454
    elif 'J1835-15' in pulsar_name:
        pulsar_ra = '18h35m54s';     pulsar_dec = '-15d35m25s';     pulsar_DM = 22.9;    p_bar = 1.5
    elif 'J1838+5051' in pulsar_name:
        pulsar_ra = '18h38m01s';     pulsar_dec = '50d54m00s';      pulsar_DM = 21.8;    p_bar = 2.5772
    elif 'J1840-1419' in pulsar_name:
        pulsar_ra = '18h40m33s';     pulsar_dec = '-14d19m07s';     pulsar_DM = 19.4;    p_bar = 6.59756252242
    elif 'J1841-0448' in pulsar_name:
        pulsar_ra = '18h41m10s';     pulsar_dec = '4d48m00s';       pulsar_DM = 29.0;    p_bar = 1.5
    elif 'J1848-12' in pulsar_name:
        pulsar_ra = '18h48m18s';     pulsar_dec = '-12d43m30s';     pulsar_DM = 91.96;   p_bar = 0.414
    elif 'J1848+1516' in pulsar_name:
        pulsar_ra = '18h49m21s';     pulsar_dec = '15d17m07s';      pulsar_DM = 77.436;  p_bar = 2.23376977466
    elif 'J1850+15' in pulsar_name:
        pulsar_ra = '18h50m09s';     pulsar_dec = '15d32m00s';      pulsar_DM = 24.7;    p_bar = 1.383965
    elif 'J1907+34' in pulsar_name:
        pulsar_ra = '19h07m00s';     pulsar_dec = '34d00m00s';      pulsar_DM = 64.85;   p_bar = 1.5
    elif 'J1911+00' in pulsar_name:
        pulsar_ra = '19h11m48s';     pulsar_dec = '0d37m00s';       pulsar_DM = 100.0;   p_bar = 6.94
    elif 'J1912+08' in pulsar_name:
        pulsar_ra = '19h12m00s';     pulsar_dec = '8d00m00s';       pulsar_DM = 96.0;    p_bar = 1.5
    elif 'J1915-11' in pulsar_name:
        pulsar_ra = '19h15m00s';     pulsar_dec = '-11d30m00s';     pulsar_DM = 91.06;   p_bar = 2.1770
    elif 'J1917+1723' in pulsar_name:
        pulsar_ra = '19h17m30s';     pulsar_dec = '17d23m00s';      pulsar_DM = 38.0;    p_bar = 1.5
    elif 'J1925-16' in pulsar_name:
        pulsar_ra = '19h25m06s';     pulsar_dec = '-16d01m00s';     pulsar_DM = 88.0;    p_bar = 3.8858
    elif 'J1929+11' in pulsar_name:
        pulsar_ra = '19h29m00s';     pulsar_dec = '11d00m00s';      pulsar_DM = 80.0;    p_bar = 3.218
    elif 'J1929+42' in pulsar_name:
        pulsar_ra = '19h29m11s';     pulsar_dec = '42d40m00s';      pulsar_DM = 51.25;   p_bar = 3.6375
    elif 'J1930+0104' in pulsar_name:
        pulsar_ra = '19h30m30s';     pulsar_dec = '1d04m00s';       pulsar_DM = 42.0;    p_bar = 1.5
    elif 'J1941-0746' in pulsar_name:
        pulsar_ra = '19h41m05s';     pulsar_dec = '-7d46m19s';      pulsar_DM = 43.6;    p_bar = 1.5
    elif 'J1943+58' in pulsar_name:
        pulsar_ra = '19h43m00s';     pulsar_dec = '58d13m00s';      pulsar_DM = 71.2;    p_bar = 1.27085
    elif 'J1944-10' in pulsar_name:
        pulsar_ra = '19h44m00s';     pulsar_dec = '-10d17m00s';     pulsar_DM = 31.009999;    p_bar = 0.409115991961
    elif 'J1945+61' in pulsar_name:
        pulsar_ra = '19h45m40s';     pulsar_dec = '61d46m12s';      pulsar_DM = 83.3;    p_bar = 1.5
    elif 'J1946+24' in pulsar_name:
        pulsar_ra = '19h46m00s';     pulsar_dec = '23d58m00s';      pulsar_DM = 96.0;    p_bar = 4.729
    elif 'J1955-0907' in pulsar_name:
        pulsar_ra = '19h55m57s';     pulsar_dec = '-9d07m14s';      pulsar_DM = 72.0;    p_bar = 0.484
    elif 'J2002+13' in pulsar_name:
        pulsar_ra = '20h02m07s';     pulsar_dec = '13d03m00s';      pulsar_DM = 5.0;     p_bar = 1.5
    elif 'J2007+20' in pulsar_name:
        pulsar_ra = '20h07m00s';     pulsar_dec = '20d21m00s';      pulsar_DM = 67.0;    p_bar = 4.634
    elif 'J2018-07' in pulsar_name:
        pulsar_ra = '20h18m00s';     pulsar_dec = '-7d45m00s';      pulsar_DM = 15.0;    p_bar = 1.5
    elif 'J2033+00' in pulsar_name:
        pulsar_ra = '20h33m31s';     pulsar_dec = '0d42m23s';       pulsar_DM = 37.84;   p_bar = 5.013
    elif 'J2047+1259' in pulsar_name:
        pulsar_ra = '20h47m45s';     pulsar_dec = '12d59m00s';      pulsar_DM = 36.00;   p_bar = 1.5
    elif 'J2052+1308' in pulsar_name:
        pulsar_ra = '20h52m47s';     pulsar_dec = '12d19m00s';      pulsar_DM = 42.00;   p_bar = 1.5
    elif 'J2100+50' in pulsar_name:
        pulsar_ra = '21h01m00s';     pulsar_dec = '50d55m43s';      pulsar_DM = 18.462;  p_bar = 1.5
    elif 'J2105+1917' in pulsar_name:
        pulsar_ra = '21h05m20s';     pulsar_dec = '19d21m00s';      pulsar_DM = 34.47;   p_bar = 3.5298
    elif 'J2105+6223' in pulsar_name:
        pulsar_ra = '21h05m13s';     pulsar_dec = '62d23m05s';      pulsar_DM = 50.75;   p_bar = 2.30487883766
    elif 'J2107+2606' in pulsar_name:
        pulsar_ra = '21h07m30s';     pulsar_dec = '26d06m00s';      pulsar_DM = 11.12;   p_bar = 5.458
    elif 'J2108+45' in pulsar_name:
        pulsar_ra = '21h08m01s';     pulsar_dec = '45d18m00s';      pulsar_DM = 84.0;    p_bar = 0.577369
    elif 'J2111+34' in pulsar_name:
        pulsar_ra = '21h11m26s';     pulsar_dec = '34d43m23s';      pulsar_DM = 79.8;    p_bar = 1.5
    elif 'J2116+37' in pulsar_name:
        pulsar_ra = '21h16m20s';     pulsar_dec = '37d07m45s';      pulsar_DM = 44.0;    p_bar = 0.145
    elif 'J2135+3032' in pulsar_name:
        pulsar_ra = '21h35m00s';     pulsar_dec = '30d32m00s';      pulsar_DM = 63.0;    p_bar = 1.5
    elif 'J2138+69' in pulsar_name:
        pulsar_ra = '21h38m00s';     pulsar_dec = '69d50m00s';      pulsar_DM = 46.6;    p_bar = 0.22
    elif 'J2146+2148' in pulsar_name:
        pulsar_ra = '21h46m00s';     pulsar_dec = '21d48m00s';      pulsar_DM = 43.0;    p_bar = 1.5
    elif 'J2202+2134' in pulsar_name:
        pulsar_ra = '21h02m21s';     pulsar_dec = '21d47m00s';      pulsar_DM = 17.7473; p_bar = 1.3573
    elif 'J2205+2244' in pulsar_name:
        pulsar_ra = '22h05m30s';     pulsar_dec = '22d44m00s';      pulsar_DM = 22.0;    p_bar = 1.5
    elif 'J2208+46' in pulsar_name:
        pulsar_ra = '22h08m31s';     pulsar_dec = '46d06m50s';      pulsar_DM = 63.0;    p_bar = 0.6425
    elif 'J2210+2118' in pulsar_name:
        pulsar_ra = '22h09m54s';     pulsar_dec = '21d17m00s';      pulsar_DM = 45.0;    p_bar = 1.5
    elif 'J2215+4524' in pulsar_name:
        pulsar_ra = '22h14m01s';     pulsar_dec = '45d25m00s';      pulsar_DM = 18.5917; p_bar = 2.7230498235
    elif 'J2221+81' in pulsar_name:
        pulsar_ra = '22h21m00s';     pulsar_dec = '81d32m00s';      pulsar_DM = 39.0;    p_bar = 1.5
    elif 'J2225+35' in pulsar_name:
        pulsar_ra = '22h24m48s';     pulsar_dec = '35d30m00s';      pulsar_DM = 51.8;    p_bar = 0.94
    elif 'J2237+2828' in pulsar_name:
        pulsar_ra = '22h37m29s';     pulsar_dec = '28d28m40s';      pulsar_DM = 38.1;    p_bar = 1.0773950914
    elif 'J2239+42' in pulsar_name:
        pulsar_ra = '22h39m01s';     pulsar_dec = '42d35m28s';      pulsar_DM = 28.306;  p_bar = 1.5
    elif 'J2252+2451' in pulsar_name:
        pulsar_ra = '22h52m23s';     pulsar_dec = '24d51m23s';      pulsar_DM = 34.4;    p_bar = 1.7979
    elif 'J2311+6656' in pulsar_name:
        pulsar_ra = '23h11m39s';     pulsar_dec = '66d55m26s';      pulsar_DM = 97.1;    p_bar = 1.945
    elif 'J2316+75' in pulsar_name:
        pulsar_ra = '23h15m00s';     pulsar_dec = '75d44m00s';      pulsar_DM = 53.4;    p_bar = 1.5
    elif 'J2329+04' in pulsar_name:
        pulsar_ra = '23h29m48s';     pulsar_dec = '4d00m00s';       pulsar_DM = 12.5126; p_bar = 1.5
    elif 'J2334+20' in pulsar_name:
        pulsar_ra = '23h34m00s';     pulsar_dec = '20d00m00s';      pulsar_DM = 13.22;   p_bar = 1.5
    elif 'J2355+1523' in pulsar_name:
        pulsar_ra = '23h55m48s';     pulsar_dec = '15d23m18s';      pulsar_DM = 26.924;  p_bar = 1.09439626467

    #    elif 'J2355+1523_1' in pulsar_name: pulsar_ra = '23h55m48s';     pulsar_dec = '15d23m18s';      pulsar_DM = 26.0;   p_bar = 1.09439626467

    elif 'J2357+24' in pulsar_name:
        pulsar_ra = '23h57m48s';     pulsar_dec = '24d00m00s';      pulsar_DM = 8.6;     p_bar = 1.5

    #    PC2

    #    DPC

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

    # Distant pulsars

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
