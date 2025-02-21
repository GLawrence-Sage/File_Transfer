import sys
import time
import requests
import traceback

def WTP_GetDebugInfo(do_once):
    # DEBUG_ENDPOINT = "http://172.20.8.6/psw/system/mac-address"
    DEBUG_ENDPOINT = "http://172.20.8.6/psw/system/boot-error"
    DEBUG_JSON  = '{"value":0}'

    while True:
        resp = requests.get(DEBUG_ENDPOINT)
        print(str(resp.status_code) + '\n' + resp.text + "\n")

        resp = requests.put(DEBUG_ENDPOINT, DEBUG_JSON)
        print(str(resp.status_code) + '\n' + resp.text + "\n")

        if do_once:
            break
        else:
            time.sleep(3)

def WTP_GetDiagInfo():

    DIAG_ENDPOINT = "http://172.20.8.6/psw/diagnostics"

    resp = requests.get(DIAG_ENDPOINT)
    print(str(resp.status_code) + '\n' + resp.text)
    print("\n")

def WTP_InitFlash():
    INIT_FLASH_ENDPOINT = "http://172.20.8.6/psw/system/initialize"

    resp = requests.put(INIT_FLASH_ENDPOINT, WTP_EMPTY_JSON)
    print(str(resp.status_code) + '\n' + resp.text + '\n')

def WTP_GetExtFlashInfo():
    EXT_FLASH_ENDPOINT = "http://172.20.8.6/psw/system/stored-applications"

    resp = requests.get(EXT_FLASH_ENDPOINT)
    print(str(resp.status_code) + '\n' + resp.text + '\n')

def WTP_Reboot(buildRev):
    WTP_REBOOT_EP   = "http://172.20.8.6/psw/system/reboot"
    WTP_REBOOT_JSON = '{"major":3,"minor":2,"build":' + str(buildRev) + '}"'

    resp = requests.post(WTP_REBOOT_EP, WTP_REBOOT_JSON)
    print(str(resp.status_code) + '\n' + resp.text + '\n')

def WTP_AddRoom(name, id):
    WTP_ADD_ROOM_EP     = "/psw/switch/rooms/config/add"
    WTP_ROOM_JSON     = '{"roomName":"' + name + '","uniqueID":' + str(id) + '}'

    # Add a room
    resp = requests.put(WTP_IP_ADDR + WTP_ADD_ROOM_EP, WTP_ROOM_JSON)

    if resp.status_code == 200:
        print("Room Added: " + str(resp.status_code) + ' ' + str(resp.content) + '\n')
    else:
        print(str(id) + " Adding room failed: " + str(resp.status_code) + ' ' + str(resp.content) + '\n')
        print(str(id) + " Failure JSON: " + (WTP_ROOM_JSON))

        WTP_GetDebugInfo(True)

def WTP_AddZone(name, roomId, zoneId):
    WTP_ADD_ZONE_EP     = "/psw/switch/zones/config/add"
    WTP_ZONE_JSON = '{"displayedName":"' + name + '","roomUniqueID":' + str(roomId) + ',"type":0,"numberOfLevels":4,"uniqueID":' + str(zoneId) + ',"level1":0,"level2":28,"level3":49,"level4":82,}"'

    resp = requests.put(WTP_IP_ADDR + WTP_ADD_ZONE_EP, WTP_ZONE_JSON)

    if resp.status_code == 200:
        print("Zone " + name + " Added: " + str(resp.status_code) + ' ' + str(resp.content) + '\n')
    else:
        print(str(zoneId) + " Adding zone failed: " + str(resp.status_code) + ' ' + str(resp.content) + '\n')
        print(str(zoneId) + " Failure JSON: " + (WTP_ZONE_JSON))

        WTP_GetDebugInfo(True)

def WTP_AddScene(name, roomId, sceneId):
    WTP_ADD_SCENE_EP    = "/psw/switch/scenes/config/add"
    WTP_SCENE_JSON  = '{"displayedName":"' + name + '","roomUniqueID":' + str(roomId) + ',"uniqueID":' + str(sceneId) + '}'

    resp = requests.put (WTP_IP_ADDR + WTP_ADD_SCENE_EP, WTP_SCENE_JSON)
    if resp.status_code == 200:
        print("Scene Added: " + str(resp.status_code) + ' ' + str(resp.content) + '\n')
    else:
        print(str(sceneId) + " Adding scene failed: " + str(resp.status_code) + ' ' + str(resp.content) + '\n')
        print(str(sceneId) + " Failure JSON: " + (WTP_SCENE_JSON))

        WTP_GetDebugInfo(True)

def WTP_RemoveAllRooms():
    WTP_REMOVE_ROOMS_EP = "/psw/switch/rooms/config/remove"

    # Remove all existing Rooms
    resp = requests.put(WTP_IP_ADDR + WTP_REMOVE_ROOMS_EP, WTP_EMPTY_JSON)
    print("Removing Rooms:" + str(resp.status_code) + ' ' + str(resp.content) + '\n')

def WTP_RemoveAllZones():
    WTP_REMOVE_ZONES_EP = "/psw/switch/zones/config/remove"

    # Remove all zones
    resp = requests.put(WTP_IP_ADDR + WTP_REMOVE_ZONES_EP, WTP_EMPTY_JSON)
    print("Removing Zones: " + str(resp.status_code) + ' ' + str(resp.content) + '\n')

def WTP_RemoveAllScenes():
    WTP_REMOVE_SCENES_EP = "/psw/switch/scenes/config/remove"

    # Remove all zones
    resp = requests.put(WTP_IP_ADDR + WTP_REMOVE_SCENES_EP, WTP_EMPTY_JSON)
    print("Removing Scenes: " + str(resp.status_code) + ' ' + str(resp.content) + '\n')

###########################################################################
if __name__ == '__main__':

    NUM_ZONES_TO_ADD    = 30
    UNIQUE_ROOM_ID      = 9
    ZONE_BASE_OFFSET    = 10

    WTP_IP_ADDR         = "http://172.20.8.6"
    WTP_EMPTY_JSON      = "{}"

    roomId = UNIQUE_ROOM_ID
    sceneId = 12

    try:

        if len(sys.argv) > 1:
            for cmd in sys.argv:
                if cmd.lower() == "clean":
                    WTP_RemoveAllRooms()
                    WTP_RemoveAllZones()
                    WTP_RemoveAllScenes()

                if cmd.lower() == "debug":
                    WTP_GetDebugInfo(True)

                if cmd.lower() == "diag":
                    WTP_GetDiagInfo()

                if cmd.lower() == "initflash":
                    WTP_InitFlash()

                if cmd.lower() == "extapps":
                    WTP_GetExtFlashInfo()

                if cmd.lower() == "reboot":
                    WTP_Reboot(sys.argv[2])

        else:
#        for runs in range(0, 20):
            WTP_RemoveAllRooms()
            WTP_RemoveAllZones()
            WTP_RemoveAllScenes()
            WTP_GetDebugInfo(True)

            # Add a room
            # WTP_AddRoom("Test Room " + str(roomId), roomId)
            # WTP_AddScene("All Tint", roomId, sceneId)
            # WTP_AddScene("All Clear", roomId, sceneId + 1)
            # sceneId += 2

            # Add zone(s) to the room
            for i in range(0, NUM_ZONES_TO_ADD):

                if (i % 1) == 0:
                    roomId += 1
                    WTP_AddRoom("Test Room " + str(roomId), roomId)
                    WTP_AddScene("All Tint", roomId, sceneId)
                    WTP_AddScene("All Clear", roomId, sceneId + 1)
                    sceneId += 2

                WTP_AddZone('TestZone'+str(i), roomId, i + ZONE_BASE_OFFSET)


    except:
        traceback.print_exc()
