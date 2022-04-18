#run this program in background to provide tracker data to the nvim plugin

#when starting this file, look at center of screen and keep head still
#to flip the rotation axes to the correct orientation

import pysurvive
import os, sys

if __name__ == "__main__":
    c_x = 0.01 #center offset x
    c_y = -0.22 #center offset y
    s_x = 2.4 #scale x
    s_y = 2.4 #scale y

    fifofile = "/tmp/pytracker_fifo"
    if not os.path.exists(fifofile):
        os.mkfifo(fifofile)

    t = 0
    p0 = 0
    p1 = 0 
    p2 = 0
    r0 = 0
    r1 = 0
    r2 = 0
    r3 = 0
    dot_y, dot_x = 0, 0
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
    p0 = poseData.Pos[0]
    p1 = poseData.Pos[1]
    p2 = poseData.Pos[2]
    r0 = poseData.Rot[0]
    r1 = poseData.Rot[1]
    r2 = poseData.Rot[2]
    r3 = poseData.Rot[3]
    y = (r0 + c_y)*s_y
    x = (r1 + c_x)*s_x
    dot_y = (H * y)
    dot_x = (W * (1-x))

    #flip axes to correct orientation
    if dot_x < 0 or dot_x > W: s_x = -s_x
    if dot_y < 0 or dot_y > H: s_y = -s_y

    running = True
    try:
        while running:
            updated = actx.NextUpdated()
            if updated:
                poseObj = updated.Pose()
                poseData = poseObj[0]
                poseTimestamp = poseObj[1]
                if str(updated.Name(), 'utf-8') == "WM0":
                    p0 = poseData.Pos[0]
                    p1 = poseData.Pos[1]
                    p2 = poseData.Pos[2]
                    r0 = poseData.Rot[0]
                    r1 = poseData.Rot[1]
                    r2 = poseData.Rot[2]
                    r3 = poseData.Rot[3]
                    y = (r0 + c_y)*s_y
                    x = (r1 + c_x)*s_x
                    dot_y = (H * y)
                    dot_x = (W * (1-x))
                    #print(dot_x, dot_y)
                else:
                    continue

                with open(fifofile, 'w') as fifo:
                    fifo.write(str(dot_x) + ',' + str(dot_y) + '\n')
                    fifo.close()
    except KeyboardInterrupt:
        print("Stopping")
        running = False
        if os.path.exists(fifofile):
            os.remove(fifofile)
        quit()





