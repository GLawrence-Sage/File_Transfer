import sys
import requests
import time
import datetime
import tzlocal
import random
import traceback
from suntime import Sun
from geopy.geocoders import Nominatim

def WTP_SetTime():
    CLOCK_URL = "http://172.20.8.6/psw/system/clocktime"
    # LOCATION = "Keene New York 12942"
    CurrentTime = datetime.datetime.now().astimezone(tzlocal.get_localzone())
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

    #resp = requests.get('http://172.20.8.6/psw/system/network')
    #print(str(resp.status_code) + ' ' + resp.text)

    #time.sleep(0.250)

    #clock_dict = '{"time":"12:58:30","dayOfWeek":5,"month":1,"dayOfMonth":23,"year":25,"sunrise":"7:31:00","sunset":"19:14:00"}'
    clock_dict = '{"time":"' + str(CurrentTime.hour) + ':' + str(CurrentTime.minute) + ':' + str(CurrentTime.second) + '","dayOfWeek":' + str(CurrentTime.isoweekday() % 7) + ',"month":' + str(CurrentTime.month) + ',"dayOfMonth":' + str(CurrentTime.day) + ',"year":' + str(CurrentTime.year - 2000) + ',"sunrise":"7:31:00","sunset":"19:14:00"}'

    resp = requests.put(CLOCK_URL, clock_dict)
    print(str(resp.status_code) + ' ' + str(resp.content))

###########################################################################
def WTP_ReadConfigs(do_once_only):
    URL = "http://172.20.8.6"

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
    SERNUM_ENDPOINT = "http://172.20.8.6/psw/system/serial-number"

    while True:
        resp = requests.get(SERNUM_ENDPOINT)
        print(str(resp.status_code) + ' ' + resp.text)
        print("\n")

        if do_once:
            break
        else:
            time.sleep(0.1)


def WTP_GetDebugInfo(do_once):
    DEBUG_ENDPOINT = "http://172.20.8.6/psw/system/mac-address"

    while True:
        try:
            resp = requests.get(DEBUG_ENDPOINT)
        except:
            continue
        
        if resp.status_code == 200:
            now = datetime.datetime.now()
            time_str = now.strftime("%H:%M:%S.%f")[:-3]
            idx  = resp.text.find('debug": "')
#            idx2 = resp.text[idx:].find('\n')
            print(time_str + " " + resp.text[idx+9:idx+23])
            #print (resp.text)
        else:
            print(str(resp.status_code) + '\n' + resp.text)
            print("\n")

        if do_once:
            break
        else:
            time.sleep(1)

def WTP_Reset():
    RESET_ENDPOINT = "http://172.20.8.6//psw/system/reset"
    resp = requests.post(RESET_ENDPOINT)
    print("Reset resp: " + str(resp.status_code) + ' ' + str(resp.content))


def WTP_SetGetConfig():
    CONFIG_ENDPOINT = "http://172.20.8.6/psw/switch/system/config"

    lang_list = ['en', 'de', 'fr', 'gd']
    lang = lang_list[random.randint(0, len(lang_list)-1)]

    config_dict1 = '{"backgroundImage":"Urban","screenLockEnabled":0,"screenLockPin":7243,"screenWaitDelay":60,"sleepAfter":300,"panelBrightness":50}"'
    config_dict2 = '{"backgroundImage":"Dark","panelBrightness":50,"sleepAfter":300,"screenWaitDelay":60,"screenLockEnabled":0,"screenLockPin":1234,"screenLanguage":"'+ lang + '"}'

    resp = requests.get(CONFIG_ENDPOINT)
    print("Get resp: " + str(resp.status_code) + ' ' + resp.text)

    resp = requests.put(CONFIG_ENDPOINT, config_dict1)
    print("Put (dict1) resp: " + str(resp.status_code) + ' ' + resp.text)

    resp = requests.get(CONFIG_ENDPOINT)
    print("Get resp: " + str(resp.status_code) + ' ' + resp.text)

    print("Lang: " + lang)

    resp = requests.put(CONFIG_ENDPOINT, config_dict2)
    print("Put (dict2) resp: " + str(resp.status_code) + ' ' + resp.text)

    resp = requests.get(CONFIG_ENDPOINT)
    print("Get resp: " + str(resp.status_code) + ' ' + resp.text)


def WTP_SetNetwork():

    NETWORK_ENDPOINT = 'http://172.20.0.161/psw/system/network'
#    NETWORK_ENDPOINT = 'http://172.20.8.6/psw/system/network'
    NETWORK_JSON = '{"dhcpClientEnabled":0,"ipAddress":"172.20.8.6","ipSubnetMask":"255.255.240.0","ipGateway":""}'

    resp = requests.put(NETWORK_ENDPOINT, NETWORK_JSON)

    print("Set Network resp: " + str(resp.status_code) + ' ' + resp.text)



###########################################################################
if __name__ == '__main__':

    try:
        if len(sys.argv) > 1:
            for cmd in sys.argv:
                if cmd == "reset":
                    while True:
                        time.sleep(random.randint(10, 120))
                        print(datetime.datetime.now())
                        WTP_Reset()

                if cmd == "reset1":
                    WTP_Reset()
                
                if cmd == "clock":
                    # while True:
                    print(datetime.datetime.now())
                    WTP_SetTime()
                    # time.sleep(random.randint(3, 15))

                if cmd == "debug":
                    WTP_GetDebugInfo(False)
                    time.sleep(1)
                
                if cmd == "dbg4vr":
                    while True:
                        try:
                            WTP_GetDebugInfo(False)  # will never exit
                        except:
                            traceback.print_exc()
                            continue

                if cmd == "getset":
                    while True:
                        print(datetime.datetime.now())
                        WTP_SetGetConfig()
                        time.sleep(random.randint(5, 60))

                if cmd == "serial":
                    while True:
                        print(datetime.datetime.now())
                        WTP_GetSerNum(True)
                        time.sleep(random.randint(1, 60))

        else:
#            while(True):
#                try:
            #WTP_ReadConfigs(True)

            #WTP_Reset()

            # WTP_SetTime()
            #WTP_GetSerNum(True)

#                    WTP_GetDebugInfo(False)
            #WTP_Reset_And_SetGetConfig()
        #    WTP_ReadConfigs(True)
        #    WTP_GetDebugInfo(True)
#                except:
#                    time.sleep(3)
            WTP_SetNetwork()

    except:
        print(datetime.datetime.now())
        traceback.print_exc()

