from ultralytics import YOLO
import object_counter
import cv2
import numpy as np
model = YOLO("model\yolov5nu.pt")
cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
drawing = False
ix = -1
iy = -1
region_points=[]
counter = object_counter.ObjectCounter()
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Kiểm tra xem sự kiện có phải là click chuột trái không
        print("Tọa độ điểm ảnh (x, y):", x, y)
        region_points.append((x,y))
        if len(region_points) > 1:
            cv2.line(img, region_points[-2], region_points[-1], (0, 255, 0), thickness=2)
        cv2.imshow('Image', img)
        counter.set_args(view_img=True,
                 reg_pts=region_points,
                 classes_names=model.names,
                 draw_tracks=False)
def draw_rectangle(event,x,y,flag,params):
    global ix,iy,drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),0)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),1)
        region_points = [(ix,iy),(ix,y),(x,y),(x,iy)]
        counter.set_args(view_img=True,
                 reg_pts=region_points,
                 classes_names=model.names,
                 draw_tracks=True)     
cv2.namedWindow(winname='Image')
cv2.setMouseCallback('Image',mouse_callback)
ret, img = cap.read()
while True:
    cv2.imshow('Image',img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cv2.destroyAllWindows()
while True:
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    tracks = model.track(im0, persist=True, show=False, classes=[0],verbose=True)

    im0 = counter.start_counting(im0, tracks)
cap.release()
cv2.destroyAllWindows()