import sys
import requests
import time
import datetime
import tzlocal
from suntime import Sun
from geopy.geocoders import Nominatim

def WTP_SetTime():
    CLOCK_URL = "http://172.20.8.7/psw/system/clocktime"
    # LOCATION = "Keene New York 12942"
    # CurrentTime = datetime.datetime.now().astimezone(tzlocal.get_localzone())
    # geolocator = Nominatim(user_agent="GetConfig")
    # localTz = tzlocal.get_localzone()

    # print(localTz)

    # location = geolocator.geocode(LOCATION)
    # print(location.address)
    # print(location.latitude)
    # print(location.longitude)

    # sun = Sun(location.latitude, location.longitude)

    # tz = datetime.date(CurrentTime.year, CurrentTime.month, CurrentTime.day)
    # sunRise = (sun.get_local_sunrise_time(CurrentTime)).astimezone(tzlocal.get_localzone())
    # sunSet = sun.get_local_sunset_time(tz)

    # print(sunRise.astimezone(tzlocal.get_localzone()), sunSet)

    #resp = requests.get('http://172.20.8.7/psw/system/network')
    #print(str(resp.status_code) + ' ' + resp.text)

    #time.sleep(0.250)

    clock_dict = '{"time":"12:58:30","dayOfWeek":5,"month":1,"dayOfMonth":23,"year":25,"sunrise":"7:31:00","sunset":"19:14:00"}'
    #clock_dict = '{"time":"' + str(CurrentTime.hour) + ':' + str(CurrentTime.minute) + ':' + str(CurrentTime.second) + '","dayOfWeek":' + str(CurrentTime.isoweekday() % 7) + ',"month":' + str(CurrentTime.month) + ',"dayOfMonth":' + str(CurrentTime.day) + ',"year":' + str(CurrentTime.year - 2000) + '',"sunrise":"7:31:00","sunset":"19:14:00"}'

    resp = requests.put(CLOCK_URL, clock_dict)
    print(str(resp.status_code) + ' ' + str(resp.content))

###########################################################################
def WTP_ReadConfigs(do_once_only):
    URL = "http://172.20.8.7"

    URLs = [#'/psw/system/network',
            # "/psw/system/info",
#            "/psw/system/serial-number",
#            "/psw/system/ux-info",
#            "/psw/system/mac-address",
            # "/psw/switch/rooms/config/10",
            # "/psw/switch/zones/config/10",
            # "/psw/switch/zones/config/11",
            # "/psw/switch/zones/config/12",
            # "/psw/switch/zones/config/13",
#            "/psw/switch/scenes",
            "/psw/switch/system/config",
#            "/psw/system/stored-applications",
#            "/psw/diagnostics",
            ]
    
    while True:
        for url in URLs:
            print(URL + url)
            resp = requests.get(URL + url)
            print(str(resp.status_code) + ' ' + resp.text)
            print("\n")

        if do_once_only:
            break
        else:
            time.sleep(0.250)

def WTP_GetSerNum(do_once):
    SERNUM_ENDPOINT = "http://172.20.8.7/psw/system/serial-number"

    while True:
        resp = requests.get(SERNUM_ENDPOINT)
        print(str(resp.status_code) + ' ' + resp.text)
        print("\n")

        if do_once:
            break
        else:
            time.sleep(0.1)


def WTP_GetDebugInfo(do_once):
    DEBUG_ENDPOINT = "http://172.20.8.7/psw/system/mac-address"

    while True:
        resp = requests.get(DEBUG_ENDPOINT)
        print(str(resp.status_code) + '\n' + resp.text)
        print("\n")

        if do_once:
            break
        else:
            time.sleep(1.1)

def WTP_Reset():
    RESET_ENDPOINT = "http://172.20.8.7//psw/system/reset"
    resp = requests.post(RESET_ENDPOINT)
    print("Reset resp: " + str(resp.status_code) + ' ' + str(resp.content))


def WTP_Reset_And_SetGetConfig():
    CONFIG_ENDPOINT = "http://172.20.8.7/psw/switch/system/config"

    config_dict1 = '{"backgroundImage":"Dark","panelBrightness":50,"sleepAfter":300,"screenWaitDelay":120,"screenLockEnabled":0,"screenLockPin":0}'
    config_dict2 = '{"backgroundImage":"Dark","panelBrightness":50,"sleepAfter":300,"screenWaitDelay":60,"screenLockEnabled":0,"screenLockPin":0,"screenLanguage":"fr"}'

    WTP_Reset()

    time.sleep(3)

    resp = requests.get(CONFIG_ENDPOINT)
    print("Get resp: " + str(resp.status_code) + ' ' + resp.text)

    resp = requests.put(CONFIG_ENDPOINT, config_dict1)
    print("Put (dict1) resp: " + str(resp.status_code) + ' ' + resp.text)

    resp = requests.get(CONFIG_ENDPOINT)
    print("Get resp: " + str(resp.status_code) + ' ' + resp.text)

    resp = requests.put(CONFIG_ENDPOINT, config_dict2)
    print("Put (dict2) resp: " + str(resp.status_code) + ' ' + resp.text)

    resp = requests.get(CONFIG_ENDPOINT)
    print("Get resp: " + str(resp.status_code) + ' ' + resp.text)


###########################################################################
if __name__ == '__main__':

    if len(sys.argv) > 0:
        

    else:
        #WTP_ReadConfigs(True)

        #WTP_Reset()

        #WTP_SetTime()
        #WTP_GetSerNum(True)

        WTP_GetDebugInfo(False)
        #WTP_Reset_And_SetGetConfig()
    #    WTP_ReadConfigs(True)
    #    WTP_GetDebugInfo(True)

