# Importing OpenCV
import cv2

# Creating global variables
# Drawing is True while the mouse button is down and false while the mouse button is up

def draw_rectangle(event,x,y,img,flag,params):
    global ix,iy,drawing
        
        # Check if the mouse event triggered is cv2.EVENT_LBUTTONDOWN
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
            
        # Check if mouse is moving using cv2.EVENT_MOUSEMOVE 
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
                
        # Checking whether the Left button is up using cv2.EVENT_LBUTTONUP
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
    return ix,iy,x,y

        






