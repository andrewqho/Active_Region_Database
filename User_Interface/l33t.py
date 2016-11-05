

urlDataJSOC = 'http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info'
for i in range(len(dateAndTimeHEK)):
    JSOC_Dict = fetch.fetch('hmi.sharp_720s[]', start=stanfordJSOC.setLowerTimeBound(i), end_or_span=stanfordJSOC.setUpperTimeBound(i), keys=['NOAA_AR','T_OBS','LAT_MIN','LON_MIN','LAT_MAX','LON_MAX']) 
    print(JSOC_Dict)
    stanfordJSOC.getInfoHMI(i, JSOC_Dict, noaaNmbr)