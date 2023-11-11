import numpy as np
import cv2
# from matplotlib import pyplot as plt

max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0

high_H = 180
high_S = 32
high_V = 255

window_detection_name = "Processed image"

def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv2.setTrackbarPos("Low H", window_detection_name, low_H)

def on_high_H_thresh_trackbar(val):
	global low_H
	global high_H
	high_H = val
	high_H = max(high_H, low_H+1)
	cv2.setTrackbarPos("High H", window_detection_name, high_H) 

def on_low_S_thresh_trackbar(val):
	global low_S 
	global high_S
	low_S = val
	low_S = min(high_S - 1, low_S)
	cv2.setTrackbarPos("Low S", window_detection_name, low_S)

def on_high_S_thresh_trackbar(val):
	global low_S
	global high_S
	high_S = val
	high_S = max(high_S, low_S+1)
	cv2.setTrackbarPos("High S", window_detection_name, high_S)

def on_low_V_thresh_trackbar(val):
	global low_V 
	global high_V
	low_V = val
	low_V = min(high_V-1, low_V)
	cv2.setTrackbarPos("Low V", window_detection_name, low_V)

def on_high_V_thresh_trackbar(val):
	global low_V
	global high_V
	high_V = val
	high_V = max(high_V, low_V+1)
	cv2.setTrackbarPos("High V", window_detection_name, high_V)

def runProcedure():
    img = cv2.imread('Python\\Images\\2020-11-11_15-33-29.jpg')
    if img is None:
        print("Error opening image!")

    showDebugImage('image', img, 640, 480)

    blur = cv2.blur(img,(5,5))
    showDebugImage('blurred image', blur, 640, 480)
    HSVimage = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # HSVValuePicker(HSVimage)
    threshold_image = cv2.inRange(HSVimage, (low_H, low_S, low_V), (high_H, high_S, high_V))
    showDebugImage('thresholded image', threshold_image, 640, 480)

    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(threshold_image, kernel, iterations = 2)

    showDebugImage('Erode image', erosion)

    invert = cv2.bitwise_not(erosion)

    showDebugImage('Inverted erode image', invert)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(erosion, 8, cv2.CV_32S)

    sizes = stats[1:, -1]
    num_labels = num_labels - 1

    newimg = erosion

    for i in range(0, num_labels):
        if sizes[i] < 400:
            newimg[labels == i + 1] = 0
        
        # check if the blob is attached to the border of the image
    
    showDebugImage('Labels', newimg)

    inputContourImage = newimg

    contours, hierarchy = cv2.findContours(inputContourImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    showDebugImage('Contouring', inputContourImage)

    print(f"Number of Contours found: {len(contours)}" )
    print(f"Amount of Points in first contour: {len(contours[0])}")

    cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

    showDebugImage('image Contouring', img)

    # for contour in contours:
    #     print(contour)
    #     for point in contour:
    #         print(point)


    cv2.waitKey(0)
    cv2.destroyAllWindows()

def showDebugImage(windowName, image, windowWidth = 640, windowHeight = 480):
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, windowWidth, windowHeight)
    cv2.imshow(windowName, image)

def HSVValuePicker(HSV_image):
    cv2.namedWindow(window_detection_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_detection_name, 640, 480)

    cv2.createTrackbar("Low H", window_detection_name, low_H, max_value_H, on_low_H_thresh_trackbar)
    cv2.createTrackbar("High H", window_detection_name, high_H, max_value_H, on_high_H_thresh_trackbar)
    cv2.createTrackbar("Low S", window_detection_name, low_S, max_value, on_low_S_thresh_trackbar)
    cv2.createTrackbar("High S", window_detection_name, high_S, max_value, on_high_S_thresh_trackbar)
    cv2.createTrackbar("Low V", window_detection_name, low_V, max_value, on_low_V_thresh_trackbar)
    cv2.createTrackbar("High V", window_detection_name, high_V, max_value, on_high_V_thresh_trackbar)

    while True:
        threshold_image = cv2.inRange(HSV_image, (low_H, low_S, low_V), (high_H, high_S, high_V))
        cv2.imshow(window_detection_name, threshold_image)
        
        key = cv2.waitKey(30)
        if key == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break