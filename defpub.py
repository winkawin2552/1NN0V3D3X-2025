import cv2
from ultralytics import YOLO
import zmq
import time
import json
import tkinter as tk
from threading import Thread

CONFIDENCE_THRESHOLD = 0.4
arrange_pos = [82, 188, 239]
color_pos = []
model = YOLO("/home/winkawin2552/CODE/INNOVEDEX-2025/best.pt")

context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5560")

def detect_objects():
    global color_pos
    color_pos.clear()  # Clear any previous detection

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_rate = 33  # n detections per second
    prev_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ ไม่สามารถอ่านภาพจากกล้องได้")
            break

        curr_time = time.time()
        if curr_time - prev_time > 1 / frame_rate:
            prev_time = curr_time

            # 👇 ตรวจจับ object แค่ n ครั้งต่อวินาที
            results = model(frame)[0]

            for box in results.boxes:
                conf = float(box.conf)

                if conf < CONFIDENCE_THRESHOLD:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                label = model.names[cls_id]

                if label not in color_pos and label in ["blue", "green", "red"]:
                    color_pos.append(label)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                text = f"{label} {conf:.2f}"
                cv2.putText(frame, text, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # ✅ แสดงกล้องทุกเฟรม
        cv2.imshow("YOLO Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if len(color_pos) == 3:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Send final object positions
    match = {}
    for i in range(len(color_pos)):
        match[color_pos[i]] = arrange_pos[i]
    use_pos = [match.get("blue"), match.get("green"), match.get("red")]

    topic = "jsondata"
    json_message = json.dumps(use_pos)
    full_message = f"{topic} {json_message}"
    print("📤 ส่งตำแหน่ง:", full_message)

    while True:
        publisher.send_string(full_message)
        time.sleep(2)

def start_detection():
    # Send trigger 1 first
    publisher.send_string("jsondata 1")
    print("📤 ส่งเริ่มทำงาน: jsondata 1")

    # Start object detection in a new thread
    Thread(target=detect_objects).start()
    root.destroy()

# GUI
root = tk.Tk()
root.title("Start Detection")

start_button = tk.Button(root, text="Start", command=start_detection, font=("Arial", 14), bg="green", fg="white")
start_button.pack(padx=100, pady=100)

root.mainloop()
