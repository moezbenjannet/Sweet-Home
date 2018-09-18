import cv2
import numpy as np
import math
import imutils
from collections import deque
import argparse
import time
import os

dirX1=""
dirY1=""
dirX=""
dirY=""
L=""
R=2
B=[4]
def mask(ROI):
    
 YCRCB = cv2.cvtColor(ROI, cv2.COLOR_BGR2YCR_CB)
 #transfert the image in YCRCB COLORS
 
 mask = cv2.inRange(YCRCB, min_ycrcb, max_ycrcb)
 #Detect Color range ( hand color )
 #Threshold the YCRCCB image to get only hand colors
 
 mask = cv2.erode(mask, None , iterations=1)
 #Erosion : useful for removing small white noises
 #will be considered 1 only if all the pixels under the kernel is 1
 
 mask = cv2.dilate(mask, None , iterations=1)
 #Dilation : in cases like noise removal, erosion is followed by dilation.
 #erosion removes white noises, but it also shrinks our object.
 #So we dilate it => object area increases

 
 opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
 #erosion followed by dilation
 closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
 #Dilation followed by Erosion
 # ==> NOISE REMOVAL  
 _,contours,_ = cv2.findContours(closing,1,2)
 #detect hand contours
 
 return contours



def handdetection(contours,flippedcap):
 global R
 global L
 global B
 if len(contours)> 0 :
  c = max(contours, key=cv2.contourArea)

  ((x, y), radius) = cv2.minEnclosingCircle(c)
  M = cv2.moments(c)
  center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

  # only proceed if the radius meets a minimum size
  if radius > 10:
  # draw the circle and centroid on the frame,
  # then update the list of tracked points
   cv2.circle(flippedcap, (int(x), int(y)), int(radius),(0, 255, 255), 2)
   cv2.circle(flippedcap, center, 5, (0, 0, 255), -1)
   pts.appendleft(center)

    # loop over the set of tracked points
 for i in np.arange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # check to see if enough points have been accumulated in
        # the buffer
        (dirX, dirY) = ("", "")
        
        if len(pts)>10 and counter >= 10 and i == 1 :
          if pts[-10] is not None:  
            # compute the difference between the x and y
            # coordinates and re-initialize the direction
            # text variables
            dX = pts[-10][0] - pts[i][0]
            dY = pts[-10][1] - pts[i][1]
            (dirX, dirY) = ("", "")

            # ensure there is significant movement in the
            # x-direction
            if np.abs(dX) > 90 :
                dirX = "Left" if np.sign(dX) == 1 else "Right"

            # ensure there is significant movement in the
            # y-direction
            if np.abs(dY) > 150 :
                dirY = "Up" if np.sign(dY) == 1 else "Down"

            # handle when both directions are non-empty
            if dirX != "" and dirY != "":
                direction = "{}-{}".format(dirY, dirX)
                
            # otherwise, only one direction is non-empty
            else:
                direction = dirX if dirX != "" else dirY
                
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(flippedcap, pts[i - 1], pts[i], (0, 0, 255), thickness)
        #coordinates of the text start point,font to be used,font size,text color,text thickness,the type of line used
    
        cv2.putText(flippedcap,dirY,(10,15), 4 , 0.8,(255,255,255),2,cv2.LINE_AA)      
        cv2.putText(flippedcap,dirX,(10,15), 4 , 0.8,(255,255,255),2,cv2.LINE_AA) 

        
        if (dirX=="Right" and B[-1]!=0):
            B.append(0)
        elif (dirX=="Left" and B[-1]!=1):
            B.append(1)
        elif (dirY=="Up" and B[-1]!=2):
            B.append(2)
        elif (dirY=="Down" and B[-1]!=3):
            B.append(3)    
        if (len(B)>3 and B[-1]==1 and B[-2]==0 and B[-3]==1 and B[-4]==0 ):
           if(R == 2):
               R=1
           else:
               R=2
           B=[4] 
        
        if (dirY=="Up" and R == 1):
               L="0"
               R=0
        elif (dirY=="Down" and R == 1):
               L="1"
               R=0
        elif (dirX=="Right" and R == 1):
               L="2"
               R=0
        elif (dirX=="Left" and R == 1 and B!=[4] and B!=[4,1]):
               L="3"
               R=0

            
    # show the movement deltas and the direction of movement on
    # the frame
    
 return None


def handdetectionL(contours,flippedcap):
 global L
 global R
 if len(contours)> 0 :
  cl = max(contours, key=cv2.contourArea)

  ((xl, yl), radiusl) = cv2.minEnclosingCircle(cl)
  Ml = cv2.moments(cl)
  centerl = (int(Ml["m10"] / Ml["m00"]), int(Ml["m01"] / Ml["m00"]))

  # only proceed if the radius meets a minimum size
  if radiusl > 10:
  # draw the circle and centroid on the frame,
  # then update the list of tracked points
   cv2.circle(flippedcap, (int(xl), int(yl)), int(radiusl),(0, 255, 255), 2)
   cv2.circle(flippedcap, centerl, 5, (0, 0, 255), -1)
   ptsl.appendleft(centerl)

    # loop over the set of tracked points
 for i in np.arange(1, len(ptsl)):
        # if either of the tracked points are None, ignore
        # them
        if ptsl[i - 1] is None or ptsl[i] is None:
            continue

        # check to see if enough points have been accumulated in
        # the buffer
        (dirXl, dirYl) = ("", "")
        
        if len(ptsl)>10 and counterl >= 10 and i == 1 :
          if ptsl[-10] is not None:  
            # compute the difference between the x and y
            # coordinates and re-initialize the direction
            # text variables
            dXl = ptsl[-10][0] - ptsl[i][0]
            dYl = ptsl[-10][1] - ptsl[i][1]
            (dirXl, dirYl) = ("", "")

            # ensure there is significant movement in the
            # x-direction
            if np.abs(dXl) > 90:
                dirXl = "Left" if np.sign(dXl) == 1 else "Right"

            # ensure there is significant movement in the
            # y-direction
            if np.abs(dYl) > 150:
                dirYl = "Up" if np.sign(dYl) == 1 else "Down"
            # handle when both directions are non-empty
            if dirXl != "" and dirYl != "":
                directionl = "{}-{}".format(dirYl, dirXl)
                
            # otherwise, only one direction is non-empty
            else:
                directionl = dirXl if dirXl != "" else dirYl
                
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(flippedcap, ptsl[i - 1], ptsl[i], (0, 0, 255), thickness)
        #coordinates of the text start point,font to be used,font size,text color,text thickness,the type of line used
    
        cv2.putText(flippedcap,dirYl,(10,15), 4 , 0.8,(255,255,255),2,cv2.LINE_AA)      
        cv2.putText(flippedcap,dirXl,(10,15), 4 , 0.8,(255,255,255),2,cv2.LINE_AA) 

        #if not os.path.exists('piste'.txt):
        # os.makedirs('piste'.txt)
        file = open('Share.txt','a')
        if (dirYl=="Up" and R==0):
                fileHandle = open ( 'Share.txt',"r" )
                lineList = fileHandle.readlines()
                fileHandle.close()
                if  len(lineList)!=0 :
                  word = lineList[len(lineList)-1].split()
                if  len(lineList)==0 or (word[0] != L+'0'):
                    file.write(L+'0\n')
                    R=1
                    file.flush()
        elif (dirYl=="Down" and R==0):
                fileHandle = open ( 'Share.txt',"r" )
                lineList = fileHandle.readlines()
                fileHandle.close()
                if  len(lineList)!=0 :
                  word = lineList[len(lineList)-1].split()
                if  len(lineList)==0 or (word[0] != L+'1'):
                    file.write(L+'1\n')
                    R=1
                    file.flush()
        elif (dirXl=="Right" and R==0):
                fileHandle = open ( 'Share.txt',"r" )
                lineList = fileHandle.readlines()
                fileHandle.close()
                if  len(lineList)!=0 :
                  word = lineList[len(lineList)-1].split()
                if  len(lineList)==0 or (word[0] != L+'2'):
                    file.write(L+'2\n')
                    R=1
                    file.flush()
        elif (dirXl=="Left" and R==0):
                fileHandle = open ( 'Share.txt',"r" )
                lineList = fileHandle.readlines()
                fileHandle.close()
                if  len(lineList)!=0 :
                  word = lineList[len(lineList)-1].split()
                if  len(lineList)==0 or (word[0] != L+'3'):
                    file.write(L+'3\n')
                    R=1
                    file.flush()

    # show the movement deltas and the direction of movement on
    # the frame
        
 return None



# global variables
bg = None



#parse

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
    help="max buffer size")
args = vars(ap.parse_args())

# region of interest (ROI) coordinates
top, right, bottom, left = 0, 420, 480, 640
topL, rightL, bottomL, leftL = 0, 20, 480,220

# intialisiation 
pts = deque(maxlen=args["buffer"])


counter = 0
(dX, dY) = (0, 0)
direction = ""
cap = cv2.VideoCapture(0)
kernel = np.ones((5,5),np.uint8)

ptsl = deque(maxlen=args["buffer"])
counterl = 0
(dXl, dYl) = (0, 0)
directionl = ""

# hand color range 
handLower = [0, 133, 85]
handUpper = [255,170,125]
min_ycrcb = np.array(handLower, np.uint8)
max_ycrcb = np.array(handUpper, np.uint8 )

while True:
 _,capture = cap.read()
 
 flippedcap = cv2.flip(capture,1)

 ROI = flippedcap[top:bottom, right:left]
 ROIL = flippedcap[topL:bottomL, rightL:leftL]


 
 contours = mask(ROI)
 handdetection(contours,ROI)
 
 
 contoursL = mask(ROIL)
 handdetectionL(contoursL,ROIL)

         
  
   
 # draw the segmented hand
 cv2.rectangle(flippedcap, (left, top), (right, bottom), (0,255,0), 2)
 cv2.rectangle(flippedcap, (leftL, topL), (right, bottom), (0,255,0), 2)
 
 cv2.imshow('origin',flippedcap)
 #cv2.imshow('right',ROI)
 #cv2.imshow('left',ROIL)
 
 k= cv2.waitKey(1) & 0xFF
 counter += 1
 counterl += 1
 if k == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
