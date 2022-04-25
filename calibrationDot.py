#this is a tool to find the correct calibration values (c_x, c_y, s_x, s_y)
#it displays a dot on the screen that follows the tracker's motion
#controls:
# q - quit
# 6/y - increase/decrease c_x
# 7/u - increase/decrease c_y
# 8/i - increase/decrease s_x
# 9/o - increase/decrease s_y
# c - center the dot
# n - negate s_x, do this if looking left moves the dot right
# m - negate s_y, do this if looking up moves the dot down

import pysurvive
import os, sys
import pygame

if __name__ == "__main__":

    c_x = -0.04 #center offset x
    c_y = 0.23 #center offset y
    s_x = 2.4 #scale x
    s_y = 2.4 #scale y

    pygame.init()

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

    pygame.display.set_caption("tracker")
    screen = pygame.display.set_mode((W,H))
    font = pygame.font.SysFont('Arial', 30)
    text_surface = font.render('', False, (0, 0, 0))

    actx = pysurvive.SimpleContext(sys.argv)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)):
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_6: c_x += 0.02
                if event.key == pygame.K_y: c_x -= 0.02

                if event.key == pygame.K_7: c_y += 0.02
                if event.key == pygame.K_u: c_y -= 0.02

                if event.key == pygame.K_8: s_x += 0.02
                if event.key == pygame.K_i: s_x -= 0.02

                if event.key == pygame.K_9: s_y += 0.02
                if event.key == pygame.K_o: s_y -= 0.02

                if event.key == pygame.K_n: s_x = -s_x
                if event.key == pygame.K_m: s_y = -s_y

                if event.key == pygame.K_c:
                    c_y = 1/(2*s_y) - r0
                    c_x = 1/(2*s_x) - r1


        updated = actx.NextUpdated()
        if updated:
            poseObj = updated.Pose()
            poseData = poseObj[0]
            poseTimestamp = poseObj[1]
            #WM0 is the updated.Name() for vive tracker, T20 is HMD
            #when tracker is connected with usb, it may be T21 instead of WM0
            if str(updated.Name(), 'utf-8') == "WM0" or str(updated.Name(), 'utf-8') == "T21":
                #p0 = poseData.Pos[0]
                #p1 = poseData.Pos[1]
                #p2 = poseData.Pos[2]
                r0 = poseData.Rot[0]
                r1 = poseData.Rot[1]
                #r2 = poseData.Rot[2]
                #r3 = poseData.Rot[3]
                y = (r0 + c_y)*s_y
                x = (r1 + c_x)*s_x
                dot_y = (H * y)
                dot_x = (W * (1-x))
                print(dot_x, dot_y)
            else:
                continue

        screen.fill((255, 255, 255))

        pygame.draw.circle(screen, (0, 0, 255), (dot_x,dot_y), 50)

        text_surface = font.render('cx,cy,sx,sy = ' 
                + str(round(float(c_x),2)) + ',' 
                + str(round(float(c_y),2)) + ',' 
                + str(round(float(s_x),2)) + ',' 
                + str(round(float(s_y),2)), False, (0, 0, 0))
        text_surface2 = font.render('x,y = ' 
                + str(round(float(dot_x),2)) + ',' 
                + str(round(float(dot_y),2)), False, (0, 0, 0))

        screen.blit(text_surface, (100,100))
        screen.blit(text_surface2, (100,200))

        pygame.display.update()

    pygame.quit()



