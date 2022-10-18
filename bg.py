#run this program in background to provide tracker data to the nvim plugin

import os, sys
import pysurvive

def main():
    c_x = 0.495 #center offset x
    c_y = 0.07 #center offset y
    s_x = 2.45 #scale x
    s_y = 2.45 #scale y

    f1 = "/tmp/nvim_tracker_f1"
    if not os.path.exists(f1):
        os.mkfifo(f1)

    r0 = 0
    r1 = 0
    screen_y, screen_x = 0, 0
    W, H = 2560, 1440

    actx = pysurvive.SimpleContext(sys.argv)
    fifofile = open(f1, 'w')

    running = True
    while running:
        try:
            updated = actx.NextUpdated()
            if updated:
                poseObj = updated.Pose()
                poseData = poseObj[0]
                poseTimestamp = poseObj[1]
                #WM0 is vive tracker, T20 is HMD
                #when tracker is connected with usb, may be T21 instead of WM0
                if str(updated.Name(), 'utf-8') == "WM0":
                    r0 = poseData.Rot[0]
                    r1 = poseData.Rot[1]
                    screen_y = H * (r0 + c_y)*s_y 
                    screen_x = W * (1- (r1 + c_x)*s_x)

                    fifofile.write(str(screen_x) + ',' + str(screen_y) + '\n')
                    fifofile.flush()

        except KeyboardInterrupt:
            print("Stopping")
            running = False
            fifofile.close()
            if os.path.exists(f1):
                os.remove(f1)
            quit()

        except BrokenPipeError:
            #remakes the fifo file if pipe is broken, so other instances of nvim plugin can get data without restarting bg script
            print("Broken Pipe, restarting")
            if os.path.exists(f1):
                os.remove(f1)
            os.mkfifo(f1)
            fifofile = open(f1, 'w')

if __name__ == "__main__":
    f1 = "/tmp/nvim_tracker_f1"
    try:
        main()
    finally:
        if os.path.exists(f1):
            os.remove(f1)
            
