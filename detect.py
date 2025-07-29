import cv2
from ultralytics import YOLO

model = YOLO("best.pt")

cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

CONFIDENCE_THRESHOLD = 0.4
arrange_pos = [60, 125, 156]
color_pos = []

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ ไม่สามารถอ่านภาพจากกล้องได้")
        break

    results = model(frame)[0]

    for box in results.boxes:
        conf = float(box.conf)

        if conf < CONFIDENCE_THRESHOLD:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        color = (0, 255, 0)  
        if label not in color_pos:
            color_pos.append(label)
        print(color_pos)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        text = f"{label} {conf:.2f}"

        cv2.putText(frame, text, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Custom YOLOv8 Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # if len(color_pos) == 3:
    #     break
match = {}
for i in range(len(color_pos)):
    match[color_pos[i]] = arrange_pos[i]
use_pos = [match["red"], match["green"], match["blue"]]

cap.release()
cv2.destroyAllWindows()