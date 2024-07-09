###INCLUDES
import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
import math

###PATHS
media_path = '../../data/'
##FILE TO WORK ON FOR NOW 
file = media_path + 'tftdevice2/04.04.2024/.10.1.avi'

#####CLEANING CONTOURS
###This function filters noise based on 
def cleanContours(contours):
    new_contours = []
    for contour in contours:
        if (len(contour) > 40):
            new_contours.append(contour)
    return new_contours


### Side of electrode in pixels on the microscope referrence ()
X = Y = 216.5 ###correspond à 100 micromètres
x_elec_side = 121.5 
y_elec_side = 100
##NO scaling to screen tft pixel side size for X_shift, Y_shift. Check below function for scaling
X_shift = X - x_elec_side
Y_shift = Y - y_elec_side
def shift(x, y, tft_size):
    X_shift_scaled = (X_shift*tft_size) / X 
    Y_shift_scaled = (Y_shift*tft_size) / Y
    #print ("SHIFT SCALED : " , X_shift_scaled, Y_shift_scaled, tft_size)
    return round(x + X_shift_scaled), round(y + Y_shift_scaled)


###Determines whether a square was already detected :
####If it was, and the new rectangle is smaller in size, it is replaced.
#####If the rectangle is not square shaped, it is also not kept
def clean_rectangle(new_rect, bounding_rectangles, thresh):
    for rect in bounding_rectangles :
        if (abs(new_rect[0] - rect[0]) <= thresh) and (abs(new_rect[1] - rect[1]) <= thresh):
            #########This below case is the case where it is a same or way bigger square. If it is, then we ignore
            if (new_rect[2] >= rect[2] + thresh ) :
                return rect[0], rect[1], rect[2], rect[3]
        else:
            x, y, w, h = new_rect[0], new_rect[1], new_rect[2], new_rect[3]
            bounding_rectangles.append([x, y, w, h])
            return x,y,w,h




def top_left_electrode(bounding_rectangles, smallest_x, smallest_y):
        if(len(bounding_rectangles)==1):
                print("NO bounding rectangles registered yet")
                return float('inf'), float('inf'), -math.inf, -math.inf
        
        #Convert bounding_boxes to a NumPy array
        bounding_rectangles_array = np.array(bounding_rectangles[1:])
        #Extract x and y coordinates from bounding_rectangles_array
        x_coordinates = bounding_rectangles_array[:, 0]
        y_coordinates = bounding_rectangles_array[:, 1]

        #Find the indices of the smallest x and y values
        min_x_index = np.argmin(x_coordinates)
        min_y_index = np.argmin(y_coordinates)
        max_x_index = np.argmax(x_coordinates)
        max_y_index = np.argmax(y_coordinates)

        #Get the smallest x and y values
        smallest_x = x_coordinates[min_x_index]
        smallest_y = y_coordinates[min_y_index]
        biggest_x = x_coordinates[max_x_index]
        biggest_y = y_coordinates[max_y_index]
        print("FROM FUNCTION:", smallest_x, smallest_y, biggest_x, biggest_y)
        return smallest_x, smallest_y, biggest_x, biggest_y




def annote_positions(tft_size, frame, smallest_x, smallest_y, width, height):
    font = cv2.FONT_HERSHEY_SIMPLEX
    pos_x_increment, pos_y_increment = smallest_x + tft_size/2 -(width+width/3)/width,  smallest_y + tft_size/2 - (height+height/3)/height ##minus (height+height/3)/height for text width or height
    cnt = 0 
    ###write down X axis
    while(pos_x_increment < width):
        cv2.putText(frame, str(cnt),(round(pos_x_increment), round(smallest_y - tft_size/10)), font, (width+width/3)/width, (0, 0, 255), 2, cv2.LINE_AA)
        pos_x_increment = pos_x_increment + tft_size
        cnt = cnt+1
    cnt = 0
    while(pos_y_increment < height):
        cv2.putText(frame, str(cnt), (round(smallest_x - tft_size/10), round(pos_y_increment)), font, (height+height/3)/height, (0, 0, 255), 2, cv2.LINE_AA)
        pos_y_increment = pos_y_increment + tft_size
        cnt = cnt+1




###RUN VIDEO
delay = 2 
frame_nb_tft_size = 50
thresh_px = 15
frame_cnt = 0
tft_size = 0
tft_sizes = []
bounding_rectangles = [[-100, -111, -222, -333]]
is_top_left_electrode_annotated = False
pos_annoted = False
pos_written = False

##Coordinates of top left corner electrode
smallest_x, smallest_y, biggest_x, biggest_y = float('inf'), float('inf'), -math.inf, -math.inf

cap = cv2.VideoCapture(file)
width  = cap.get(3)
height = cap.get(4)
fps = cap.get(cv2.CAP_PROP_FPS)
if (cap.isOpened()== False): 
    print("Error opening video stream or file")
cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Frame', round(width*0.6), round(height*0.6))




while True:
    ret, frame = cap.read()
    if ret ==True:
        frame_cnt+=1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 90, 155, cv2.THRESH_BINARY)
        contours_wires, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        frame_trans_contour = frame.copy()
        clean_wires_contours = cleanContours(contours_wires)
        ###Contour detection and display according to 
        if(frame_cnt >= delay*fps):
            pos_written = False
            for contour in clean_wires_contours:
                    area = cv2.contourArea(contour)
                    if area > 3000:
                        x,y,w,h = (cv2.boundingRect(contour))
                        if((w!=width or h!=height) and abs(w - h) < thresh_px):
                            x,y,w,h = clean_rectangle((x,y,w,h), bounding_rectangles, thresh_px)
                            tft_sizes.append(w)
                            tft_sizes.append(h)
                            tft_size = max(set(tft_sizes), key = tft_sizes.count)
                            if(abs(x - smallest_x) <= thresh_px and abs(y - smallest_y) <= thresh_px):
                                x, y = shift(x, y, tft_size)
                                cv2.rectangle(frame_trans_contour, (x, y), (x + round(tft_size), y + round(tft_size)), (0, 0, 255), 3)
                                is_top_left_electrode_annotated = True
                            else:
                                x, y = shift(x, y, tft_size)
                                cv2.rectangle(frame_trans_contour, (x, y), (x + round(tft_size), y + round(tft_size)), (0, 255, 0), 3)
                        if(pos_annoted and not pos_written):
                            annote_positions(tft_size, frame_trans_contour, smallest_x, smallest_y, width, height)
                            pos_written = True
            #Input on w
            if cv2.waitKey(1) & 0xFF == ord('w'):
                X_input = input("Please write x coordinate of the highlighted red electrode.")
                Y_input = input("Please write y coordinate of the highlighted red electrode.")
                pos_annoted = True
                print(X_input,Y_input)


            ###OPTIM
            thresh_px = round(len(bounding_rectangles)/3)
            tft_sizes = []
            smallest_x, smallest_y, biggest_x, biggest_y = top_left_electrode(bounding_rectangles, smallest_x, smallest_y)
            print("GENERAL:", smallest_x, smallest_y, biggest_x, biggest_y)
            bounding_rectangles = [[-100, -111, -222, -333]]


    #Display Frame
        '''if(is_top_left_electrode_annotated):
            cv2.imshow('Frame',stream_crop(smallest_x, smallest_y, biggest_x, biggest_y, frame_trans_contour))
        else:'''
        cv2.imshow('Frame',frame_trans_contour)
    

    #Print on p
    if cv2.waitKey(1) & 0xFF == ord('p'):
        print(bounding_rectangles, tft_size)
    #Exit on q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

