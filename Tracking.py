import time
import cv2
import sys
import imutils
import numpy as np


FRAME_W = 320
FRAME_H = 240

# Default Pan/Tilt for the camera in degrees.
# Camera range is from -90 to 90
cam_pan = 90
cam_tilt = 90

# initialize the camera and grab a reference to the raw camera capture
camera = cv2.VideoCapture(0)
camera.set(3, 320)
camera.set(4, 240)

LW = np.array([0, 100, 100 ])
UP = np.array([25, 255, 255])

# allow the camera to warmup
time.sleep(3)
lastTime = time.time()*1000.0

while True:
    ret, frame = camera.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame = imutils.resize(frame, width=600)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LW, UP)
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
    lastTime = time.time()*1000.0
    
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y),radius) = cv2.minEnclosingCircle(c)

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), 5,(255, 0, 255), 2)
            # Correct relative to center of image
            turn_x  = float(-(x + radius - (FRAME_W/2)))
            turn_y  = float(y + radius - (FRAME_H/2))

            # Convert to percentage offset
            turn_x  /= float(FRAME_W/2)
            turn_y  /= float(FRAME_H/2)

            # Scale offset to degrees
            turn_x   *= 10 # V
            turn_y   *= 10 # H
            #print (turn_x, turn_y)
            
            cam_pan  += turn_x
            cam_tilt -= turn_y

            # Clamp Pan/Tilt to 0 to 180 degrees
            cam_pan = max(712,min(312,cam_pan))
            cam_tilt = max(612,min(244,cam_tilt))
            print(cam_pan, cam_tilt)
            

        # Update the servos
        
        cv2.putText(frame, "Pan : " + str(int(cam_pan)) + " tilt: " + str(int(cam_tilt)), (20,20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        #print ("pan :" + str(int(cam_pan - 90)), "tilt : " + str(int(cam_tilt)))

        #break

    # show the frame
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(1) & 0xFF
 
    
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
camera.close()
