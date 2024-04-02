import cv2

# Hàm callback sẽ được gọi khi có sự kiện click chuột
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Kiểm tra xem sự kiện có phải là click chuột trái không
        print("Tọa độ điểm ảnh (x, y):", x, y)

# Mở camera
cap = cv2.VideoCapture(0)

# Tạo cửa sổ để hiển thị video
cv2.namedWindow('Video')

# Gắn hàm callback với sự kiện chuột
cv2.setMouseCallback('Video', mouse_callback)

while True:
    ret, frame = cap.read()

    # Hiển thị frame
    cv2.imshow('Video', frame)

    # Thoát nếu nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
