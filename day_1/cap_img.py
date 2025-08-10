import cv2 as cv
import time

cap = cv.VideoCapture(0)
count = 600
while 1:
    _ ,frame = cap.read()
    if _:
        cv.imshow("img", frame)
        cv.imwrite(f'/home/winkawin2552/CODE/INNOVEDEX-2025/image/{count}.jpg', frame)
        time.sleep(0.25)
        print(count)
        count+= 1
        key = cv.waitKey(33)
    if key == ord('q') or count ==900:
        break