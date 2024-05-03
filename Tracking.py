from ultralytics import YOLO
import object_counter
import cv2
import numpy as np
import keyboard
import configparser
import messagetest
import tkinter as tk
from tkinter import messagebox



config = configparser.ConfigParser()
config.sections()
config.read('setting.ini')
# Change model path
model = YOLO("model\yolov5nu.pt")
counter = object_counter.ObjectCounter()

# Open video capture
cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Initialize variables
drawing = False
ix = -1
iy = -1
#region_points = []
region_point = config['region_points']
region_points = eval(region_point['position'])
# Mouse click event handler
def click_event(event, x, y, flags, param):
    global point1
    global img
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ",", y)
        point1 = (x, y)
        region_points.append(point1)
        img_og = img.copy()
        if len(region_points) == 1:
            cv2.circle(img_og, point1, 2, (255, 0, 0), -1)
        elif len(region_points) == 2:
            cv2.line(img_og, region_points[0], region_points[1], (255, 0, 0), 2)
        elif len(region_points) > 2:
            for i in range(len(region_points) - 1):
                cv2.line(img_og, region_points[i], region_points[i + 1], (255, 0, 0), 2)
            cv2.line(img_og, region_points[len(region_points) - 1], region_points[0], (255, 0, 0), 2)
        cv2.imshow("image", img_og)
    if event == cv2.EVENT_RBUTTONDOWN:
        region_points.clear()
        img_og = img.copy()
        cv2.imshow("image", img_og)

if( region_points is None  or len(region_points)<=1 ) :

    # Read the first frame
    RET, img = cap.read()
    cv2.imwrite('captured_photo.jpg', img)
    img_og = img.copy()
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", click_event)
    # Handle user input
    while True:
        k = cv2.waitKey(0)
        print(k)
        if k == 27:
            cv2.destroyAllWindows()
            break
        elif k == 115:
            cv2.imwrite("copy.jpg","message", img)
            cv2.destroyAllWindows()
            break

# Set counter arguments
counter.set_args(view_img=True, reg_pts=region_points, classes_names=model.names, draw_tracks=False)

# Process video frames
while True:
    counter.set_args(view_img=True, reg_pts=region_points, classes_names=model.names, draw_tracks=False)
    success, im0 = cap.read()
    print(f"Current point is {region_points} \n")
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    if keyboard.is_pressed('esc'):
        break
    tracks = model.track(im0, persist=False, show=False, classes=[0], verbose=False)
    
    if tracks is not None:
        im0 = counter.start_counting(im0, tracks)

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()

# Run object_counter if executed as a script
if __name__ == "__main__":
    object_counter()
