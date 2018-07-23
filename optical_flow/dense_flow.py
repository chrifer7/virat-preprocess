import cv2
import numpy as np
#cap = cv2.VideoCapture("video_opencv_mjpg.avi")

#im = cv2.imread("samples/VIRAT_S_000001_frame-3693.jpg")
#imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)


cap = cv2.VideoCapture("Megamind.avi")

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255
i = 0
while(1):
    ret, frame2 = cap.read()
    next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    r1 = cv2.imwrite('flow/f_'+str(i)+'_opticalfb.png',frame2)
    r2 = cv2.imwrite('flow/f_'+str(i)+'_opticalhsv.png',rgb)
        
    #cv2.imshow('frame2',rgb)
    #k = cv2.waitKey(30) & 0xff
    #if k == 27:
    #    break
    #elif k == ord('s'):
        #cv2.imwrite('.\opticalfb'+str(i)+'.png',frame2)
        #cv2.imwrite('.\opticalhsv'+str(i)+'.png',rgb)
    prvs = next
    
    i = i + 1
    
    print("frame: ",i, r1, r2)
    
    if (i > 40):
    	break

cap.release()
cv2.destroyAllWindows()
