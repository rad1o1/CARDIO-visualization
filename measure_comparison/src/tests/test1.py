###INCLUDES
import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
import math

###PATHS
media_path = 'C:/Users/radja/Documents/COURS/RSRC/CARDIO-visualization/data/'
##FILE TO WORK ON FOR NOW 
file2 = media_path + 'TESTVIDEOS/.10.1.avi'
file1 = media_path + 'TESTVIDEOS/Nifedipine4_CentreG18_basS9_video.AVI'
stream_url = "http:169.254.235.60:8080"
file = file2

#####CLEANING CONTOURS
###This function filters noise contour
def cleanContours(contours):
    new_contours = []
    for contour in contours:
        if (len(contour) > 40):
            new_contours.append(contour)
    return new_contours

    ###HIGHPASS FILTER FOR TRANSISTORS CONTOURING
    ##DISPLAY OF CONTOURS

cap = cv2.VideoCapture(file)
width  = cap.get(3)   # float `width`
height = cap.get(4)  # float `height`

##Assert
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

##window creation
# Set the display window size
cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)  #Allow window resizing
cv2.resizeWindow('Frame', round(width*0.6), round(height*0.6))  #Window size - 40% smaller

##READ FRAME BY FRAME
while True:
    ret, frame = cap.read()
    if ret ==True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 90, 155, cv2.THRESH_BINARY)
        contours_wires, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

        ###COPY FRAME 
        frame_trans_contour = frame.copy()
        #####clean contours and contour rectangle shapes
        clean_wires_contours = cleanContours(contours_wires)

        for contour in clean_wires_contours:
                area = cv2.contourArea(contour)
                if area > 1000:
                    x,y,w,h = cv2.boundingRect(contour)
                    cv2.rectangle(frame_trans_contour, (x, y), (x + w, y + h), (0, 255, 0), 3)   
                            ###drawing raw contours instead
                    #cv2.drawContours(image=frame_trans_contour, contours=clean_wires_contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    #Display Frame
        cv2.imshow('Frame',frame_trans_contour)
    #Exit on Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

