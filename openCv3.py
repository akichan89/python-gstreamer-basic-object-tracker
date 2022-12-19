import cv2
import numpy as np
import time

print(cv2.__version__)
timeMark=time.time()
dtFIL=0

def nothing(x):
    pass

cv2.namedWindow("TrackBars")
cv2.moveWindow("TrackBars",1320,0 )
cv2.createTrackbar('hueLower', 'TrackBars', 100,179,nothing)
cv2.createTrackbar('hueUpper', 'TrackBars', 116,179, nothing)
cv2.createTrackbar('satLower', 'TrackBars', 160,255, nothing)
cv2.createTrackbar('satUpper', 'TrackBars', 255,255,nothing)
cv2.createTrackbar('valLower', 'TrackBars', 150,255,nothing)
cv2.createTrackbar('valUpper', 'TrackBars', 255,255,nothing)

# width=720
# height=480
# flip=2
font=cv2.FONT_HERSHEY_SIMPLEX
camSet1='/dev/video0'

cam1=cv2.VideoCapture(camSet1)

while True:
    __, frame=cam1.read()
    hsv1=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    hueLow=cv2.getTrackbarPos('hueLower', 'TrackBars')
    hueUp=cv2.getTrackbarPos('hueUpper', 'TrackBars')

    Ls=cv2.getTrackbarPos('satLower', 'TrackBars')
    Us=cv2.getTrackbarPos('satUpper', 'TrackBars')

    Lv=cv2.getTrackbarPos('valLower', 'TrackBars')
    Uv=cv2.getTrackbarPos('valUpper', 'TrackBars')

    l_b=np.array([hueLow, Ls, Lv])
    u_b=np.array([hueUp, Us, Uv])

    FGmask=cv2.inRange(hsv1, l_b, u_b)

    # dt=time.time()-timeMark()
    cv2.imshow('FGmask', FGmask)
    timeMark=time.time()
    # dtFIL=1/dtFIL+.1
    # fps=1/dtFIL
    # cv2.putText(frame, "time: "+str(timeMark), )
    #cv2.imshow('myCam', frame)
    cv2.moveWindow('FGmask', 0,0)

    contours,__ = cv2.findContours(FGmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        (x,y,w,h)=cv2.boundingRect(cnt)
            
        if area>=100:
            cv2.rectangle(frame,(x,y),(x+w, y+h), (0,255,255),3)
            break
    
    cv2.rectangle(frame,(0,0),(150,40),(0,0,225),-1)
  
    cv2.imshow('frame', frame)
    cv2.moveWindow('frame', 0, 450)
    if cv2.waitKey(1)==ord('q'):
        print("Exiting")
        break
cam1.release()
cv2.destroyAllWindows()


