import cv2
import numpy as np
import math
import winsound
import time
cap = cv2.VideoCapture("C:\\Users\\singl\\Downloads\\MM803\\Video DataSet\\Office\\Video (3).avi")
#cap = cv2.VideoCapture("C:\\Users\\singl\\Downloads\\MM803\\Video DataSet\\Home_02\\video (41).avi")
#cap = cv2.VideoCapture("C:\\Users\\singl\\Downloads\\MM803\\Video DataSet\\Lecture room\\video (9).avi")




count = 0
count1 =0
slope=0
slope1 = 100
minArea = 120*100
radianToDegree=57.324
minimumLengthOfLine=150.0
minAngle=18
maxAngle=72
list_falls=[]
count_fall=0
firstFrame= None

time.sleep(1)

#Function definition for frame Conversion
def convertFrame(frame):
    r = 750.0 / frame.shape[1]
    dim = (750, int(frame.shape[0] * r))
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (31,31),0)

    return frame,gray

while True:

    ret,frame= cap.read()
    if frame is None:
        break
    frame,gray = convertFrame(frame);

    #comparison Frame
    if firstFrame is None:
        time.sleep(1.0)
        _,frame= cap.read()
        frame,gray=convertFrame(frame)
        firstFrame = gray
        continue

    #Frame difference between current and comparison frame
    frameDelta= cv2.absdiff(firstFrame,gray)
    #Thresholding
    thresh1 = cv2.threshold(frameDelta,20,255,cv2.THRESH_BINARY)[1]
    #Dilation of Pixels
    thresh = cv2.dilate(thresh1,None,iterations = 15)



    #Finding the Region of Interest with changes
    _,contour,_ = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for con in contour:

        if len(con)>=5 and cv2.contourArea(con)>minArea:
            ellipse = cv2.fitEllipse(con)
            cv2.ellipse(frame,ellipse,(255,255,0),5)

            #Co-ordinates of extreme points
            extTop = tuple(con[con[:, :, 1].argmin()][0])
            extBot = tuple(con[con[:, :, 1].argmax()][0])
            extLeft = tuple(con[con[:, :, 0].argmin()][0])
            extRight = tuple(con[con[:, :, 0].argmax()][0])

            line1 = math.sqrt((extTop[0]-extBot[0])*(extTop[0]-extBot[0])+(extTop[1]-extBot[1])*(extTop[1]-extBot[1]))
            midPoint = [extTop[0]-int((extTop[0]-extBot[0])/2),extTop[1]-int((extTop[1]-extBot[1])/2)]
            if line1>minimumLengthOfLine:
                #cv2.line(frame,(extBot[0],extBot[1]),(extTop[0],extTop[1]), (255, 0, 0), 5)
                if (extTop[0]!=extBot[0]):
                    slope = abs(extTop[1]-extBot[1])/(extTop[0]-extBot[0])

            else:
                #cv2.line(frame, (extLeft[0], extLeft[1]), (extRight[0], extRight[1]), (255, 0, 0), 5)
                if (extRight[0] != extLeft[0]):
                    slope = abs(extRight[1]-extLeft[1])/(extRight[0]-extLeft[0])
            #print(slope)

            #cv2.line(frame, (midPoint[0], midPoint[1]), (midPoint[0] + 1, midPoint[1] + 100), (255, 255, 255), 5)
            #angle in Radians with perpendicular
            originalAngleP = np.arctan((slope1 - slope) / (1 + slope1 * slope))
            #angle with Horizontal
            originalAngleH = np.arctan(slope)
            #Angle in degrees
            originalAngleH = originalAngleH*radianToDegree
            originalAngleP=originalAngleP*radianToDegree
            #print(originalAngleP)
            if (abs(originalAngleP) > minAngle and abs(originalAngleH) < maxAngle and abs(originalAngleP)+abs(originalAngleH)>89 and abs(originalAngleP)+abs(originalAngleH)<91):
                count += 1
                if (count > 18):
                    count_fall+=1
                    #print("Fall detected")
                    list_falls.append((time.time()))
                    if(count_fall>1):
                        if(list_falls[len(list_falls)-1]-list_falls[len(list_falls)-2]<.5):
                            #print (list_falls[len(list_falls)-1]-list_falls[len(list_falls)-2])
                            print ("Fall detected")
                        else:
                            continue

                    count = 0

    cv2.imshow('Frame', frame)
    #cv2.imshow('gray',gray)
    #cv2.imshow('Thresh',thresh)
    #cv2.imshow('FirstFrame',firstFrame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
#print (list_falls)
cap.release()
cv2.waitKey(1)
cv2.destroyAllWindows()



