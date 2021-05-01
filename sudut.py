import cv2
import math
import numpy as np

hsvColorBounds = {}
hsvColorBounds['darkGreen'] = (np.array([35,50,20],np.uint8), np.array([80,255,120],np.uint8))
hsvColorBounds['green'] = (np.array([30,0,0],np.uint8), np.array([100,255,255],np.uint8))
hsvColorBounds['white'] = (np.array([0,0,80],np.uint8), np.array([255,50,120],np.uint8))
hsvColorBounds['yellow'] = (np.array([15, 204, 204],np.uint8), np.array([20, 255, 255],np.uint8))
hsvColorBounds['red'] = (np.array([0, 153, 127],np.uint8), np.array([4, 230, 179],np.uint8))
hsvColorBounds['orange'] = (np.array([15, 204, 204],np.uint8), np.array([20, 255, 255],np.uint8))
hsvColorBounds['darkYellow'] = (np.array([20, 115, 140],np.uint8), np.array([25, 205, 230],np.uint8))
hsvColorBounds['darkYellowAttempt2(isolating)'] = (np.array([20, 90, 117],np.uint8), np.array([32, 222, 222],np.uint8))
hsvColorBounds['orange2'] = (np.array([0, 99, 102],np.uint8), np.array([16, 255, 255],np.uint8))

sisia=0
sisib=0
sisic=0
x=0
y=0


fo = cv2.FONT_HERSHEY_DUPLEX
w = (200,200,0)

LW = np.array([100, 100, 100 ])
UP = np.array([120, 255, 255])

LW_P = np.array([0, 97, 80 ])
UP_P = np.array([15, 255, 255])

cap = cv2.VideoCapture(0)

def smoothNoise(frame):
    
    

    return frame

# A function of both velocity and position to find difference
# between two sets of two values (like 4D distance)
def distance4D(p, q, r, s):
    dist = math.sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2 + (r[0]-s[0])**2 + (r[1]-s[1])**2)
    return dist

# A function of position to find difference
# between two values (2D distance)
def distance2D(x,y):
    dist = math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)
    return dist


def cariSudut(contour,frame):
    M = cv2.moments(contour)

    if M['m00']==0:
        print("Tidak bisa dibagi nol")
        return ''

    else:
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        cv2.circle(frame,(cx,cy),5,(0,0,255),3)
        #cv2.imshow("Frame", frame)

    

    cx=cx-(640/2)
    cy=cy-(480/2)

    if(cx==0):
        cx=1
    sudut = round(math.atan2(cx,cy)*180/math.pi)
    print(sudut)

    return sudut

def cariSudutDeteksi(contour,frame):
    #Cari titik tengah berdasarkan contour terbesar
    M = cv2.moments(contour)

    if M['m00']==0:
        print("Tidak bisa dibagi nol")
        return ''

    else:
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        cv2.circle(frame,(cx,cy),5,(0,0,255),3)
        #cv2.imshow("Frame", frame)
        
    x=cy
    y=cy
    
    cx=cx-(640/2)
    cy=cy-(480/2)

    if(cx==0):
        cx=1

    
    distance = (2 * 3.14 * 180) / (x+ y * 360) * 1000 + 3 ### Distance measuring in Inch
    cm = distance * 2.54
    print(cm)
    sudut = round(math.degrees(math.atan2(cx,cy))*180/math.pi)
    
    posisiBola = str("Posisi Bola {0}".format(sudut))
    cv2.putText(frame,posisiBola,(10,10),fo,0.5,w)
    print(sudut)

    return sudut
    

    

def cariBola(frame,color):
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    kernel = np.ones((3,3)).astype(np.uint8)
    colorBall=hsvColorBounds[color]
    mask = cv2.inRange(hsv, colorBall[0], colorBall[1])
    
    mask = cv2.erode(mask, kernel)
    mask = cv2.dilate(mask, kernel)
    contours, hierarcy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #Return jika tidak ada contour yang ditemukan
    
    if len(contours)==0:
        print("Bola tidak ditemukan")
        return ''
    else:
        cv2.imshow("Masked Bola",mask)
    


    #Cari contour terbesar
    contour=max(contours, key=cv2.contourArea)
    return cariSudutDeteksi(contour, frame)

def cariPartner(frame,color):
    colorBall=hsvColorBounds[color]
    mask = cv2.inRange(frame, colorBall[0], colorBall[1])
    contours, hierarcy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #Return jika tidak ada contour yang ditemukan
    
    if len(contours)==0:
        print("Partner tidak ditemukan")
        return ''
    else:
        cv2.imshow("Masked Lawan", mask)

    for contour in contours:
        sudut=cariSudutDeteksi(contour, frame)

        if sudut!='':
            suduts.append(sudut)

    if len(suduts)==0:
        return ''

    return suduts
            
        


while True:
    ret, frame = cap.read(0)
    frame=smoothNoise(frame)

    bola = cariBola(frame,'red')
    partner = cariPartner(frame,'yellow')

    cv2.imshow("Frame on Detect",frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
	
