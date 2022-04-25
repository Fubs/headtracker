#run this program in background to provide tracker data to the nvim plugin

#when starting this file, look at center of screen and keep head still
#to flip the rotation axes to the correct orientation

import os, sys, threading
import pysurvive

def main():
    c_x = 0.01 #center offset x
    c_y = 0.22 #center offset y
    s_x = 2.4 #scale x
    s_y = 2.4 #scale y

    f1 = "/tmp/nvim_tracker_f1"
    if not os.path.exists(f1):
        os.mkfifo(f1)

    r0 = 0
    r1 = 0
    screen_y, screen_x = 0, 0
    W, H = 2560, 1440

    actx = pysurvive.SimpleContext(sys.argv)

    #WM0 is vive tracker, T20 is HMD
    #when tracker is connected with usb, may be T21 instead of WM0
    updated = actx.NextUpdated()
    while not updated:
        while not str(updated.Name(), 'utf-8') == "WM0":
            updated = actx.NextUpdated()

    poseObj = updated.Pose()
    poseData = poseObj[0]
    poseTimestamp = poseObj[1]
    r0 = poseData.Rot[0]
    r1 = poseData.Rot[1]
    screen_y = H * (r0 + c_y)*s_y 
    screen_x = W * (1- (r1 + c_x)*s_x)


    running = True
    try:
        while running:
            updated = actx.NextUpdated()
            if updated:
                poseObj = updated.Pose()
                poseData = poseObj[0]
                poseTimestamp = poseObj[1]
                if str(updated.Name(), 'utf-8') == "WM0":
                    r0 = poseData.Rot[0]
                    r1 = poseData.Rot[1]
                    screen_y = H * (r0 + c_y)*s_y 
                    screen_x = W * (1- (r1 + c_x)*s_x)

                with open(f1, 'w') as f:
                    f.write(str(screen_x) + ',' + str(screen_y) + '\n')
                    f.close()

    except KeyboardInterrupt:
        print("Stopping")
        running = False
        if os.path.exists(f1):
            os.remove(f1)
        quit()

if __name__ == "__main__":
    main()




