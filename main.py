from ultralytics import YOLO
import object_counter
import cv2

model = YOLO("model\yolov5nu.pt")
#Camera Device or Youtube Video 
cap = cv2.VideoCapture(0)
#status check
assert cap.isOpened(), "Error reading video file"
# weight, height, fps define for the camera
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Define region points || Fixx this line to mouse drag 

region_points = [(320, 480),(320, 0), (640, 0), (640, 480)]

# Video writer
video_writer = cv2.VideoWriter("object_counting_output.avi",
                       cv2.VideoWriter_fourcc(*'mp4v'),
                       fps,
                       (w, h))

# Init Object Counter
#Khoi tao doi tuong
counter = object_counter.ObjectCounter()

#Setup tham so cho Counter()
counter.set_args(view_img=True,
                 reg_pts=region_points,
                 classes_names=model.names,
                 draw_tracks=True)

#Looping : 
while cap.isOpened():

    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    tracks = model.track(im0, persist=True, show=False, classes=[0])

    im0 = counter.start_counting(im0, tracks)
    #video_writer.write(im0)


cap.release()
video_writer.release()
cv2.destroyAllWindows()