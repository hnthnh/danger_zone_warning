from ultralytics import YOLO
import object_counter
import cv2
import numpy as np
model = YOLO("model\yolov5nu.pt")
#Camera Device or Youtube Video 
cap = cv2.VideoCapture(0)
#Setup cuong do anh sang cho camera 
#cap.set(cv2.CAP_PROP_BRIGHTNESS, 0) 
#status check
assert cap.isOpened(), "Error reading video file"
# weight, height, fps define for the camera
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Define region points || Fixx this line to mouse drag 


# Video writer
# video_writer = cv2.VideoWriter("object_counting_output.avi",
#                        cv2.VideoWriter_fourcc(*'mp4v'),
#                        fps,
#                        (w, h))

# Init Object Counter
#Khoi tao doi tuong


# Creating global variables
# Drawing is True while the mouse button is down and false while the mouse button is up
drawing = False
ix = -1
iy = -1
region_points=[(0,0),(0,0),(0,0),(0,0)]
# Defining a function to draw a rectangle over the image

counter = object_counter.ObjectCounter()
#Setup tham so cho Counter()


def draw_rectangle(event,x,y,flag,params):
    global ix,iy,drawing
    
    # Check if the mouse event triggered is cv2.EVENT_LBUTTONDOWN
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
        
    # Check if mouse is moving using cv2.EVENT_MOUSEMOVE 
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),0)
            
    # Checking whether the Left button is up using cv2.EVENT_LBUTTONUP
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),1)
        
        region_points = [(ix,iy),(ix,y),(x,y),(x,iy)]
        counter.set_args(view_img=True,
                 reg_pts=region_points,
                 classes_names=model.names,
                 draw_tracks=True)
# Creating a named window        
cv2.namedWindow(winname='Image')
# Creating a callback function
cv2.setMouseCallback('Image',draw_rectangle)
# Creating blank image
ret, img = cap.read()
# Displaying the image frame till the q key is pressed.
while True:
    cv2.imshow('Image',img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cv2.destroyAllWindows()


#Looping : 
while cap.isOpened():
    
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    tracks = model.track(im0, persist=True, show=False, classes=[0],verbose=True)

    im0 = counter.start_counting(im0, tracks)
    #video_writer.write(im0)



cap.release()
#video_writer.release()
cv2.destroyAllWindows()