import os



def getCameraList():
    '''Returns list of connected video inputs by running a bash command and reading the output'''
    
    cameras = os.popen('system_profiler SPCameraDataType | grep "^    [^ ]" | sed "s/    //" | sed "s/://"')

    cameralist = []
    for camera in cameras:
        cameralist.append(camera.strip())

    return cameralist

print(getCameraList())