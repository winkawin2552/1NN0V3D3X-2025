import cv2
from ultralytics import YOLO
import time
from pyfirmata2 import Arduino
import threading
import tkinter as tk

# ---------------- SERVO SETUP ----------------
model = YOLO(r"C:\innovedex\best (2).pt")

board = Arduino('COM5')
board.samplingOn()
servo_pins = [4, 5, 6, 7, 8]
servos = {}

stop_detection_event = threading.Event()  # Event to stop detection thread

ready = False

class Servo:
    def __init__(self, pin):
        self.servo_pin = board.get_pin(f'd:{pin}:s')
        self.pin = pin
        self.current_angle = 90  # start at 90
        self.servo_pin.write(self.current_angle)

    def write(self, target_angle, step_delay=0.01):
        # Special scaling for pin 4
        if self.pin == 4:
            target_angle = target_angle * (180 / 270)

        step = 1 if target_angle > self.current_angle else -1
        for angle in range(int(self.current_angle), int(target_angle) + step, step):
            self.servo_pin.write(angle)
            self.current_angle = angle
            time.sleep(step_delay)

def pos(target_angles=[], pins=servo_pins, servos=servos, step_delay=0.006):
    """
    Moves all servos together towards the given target angles.
    """
    # Store starting angles
    start_angles = [servos[p].current_angle for p in pins]

    # Calculate target angles (adjust pin 4 if needed)
    adjusted_targets = []
    for i, p in enumerate(pins):
        if p == 4:
            adjusted_targets.append(target_angles[i] * (180 / 270))
        else:
            adjusted_targets.append(target_angles[i])

    # Find maximum steps needed
    max_steps = max(abs(int(t) - int(s)) for s, t in zip(start_angles, adjusted_targets))

    # Step-by-step move
    for step in range(1, max_steps + 1):
        for i, p in enumerate(pins):
            start = start_angles[i]
            target = adjusted_targets[i]
            if start != target:
                # Calculate next intermediate position
                direction = 1 if target > start else -1
                new_angle = start + (step * direction)
                # Clamp if overshoot
                if (direction == 1 and new_angle > target) or (direction == -1 and new_angle < target):
                    new_angle = target
                servos[p].servo_pin.write(new_angle)
                servos[p].current_angle = new_angle
        time.sleep(step_delay)

def setup(servo_pins=servo_pins):
    for pin in servo_pins:
        servos[pin] = Servo(pin)

def check():
    pos([30, 79, 118, 0, 0])
    pos([242, 79, 118, 0, 0], step_delay=0.052)

color_pos = {"red": 0, "green": 0, "blue": 0}
get_curVal = []

# ---------------- YOLO DETECTION LOOP ----------------
def detection_loop(n = 2):
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    CONFIDENCE_THRESHOLD = 0.7
    global color_pos
    global ready

    while not stop_detection_event.is_set():
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

            # ----------------------- get position ------------------------------------
            if label in list(color_pos.keys()) and color_pos[label] == 0 and ready:
                get_curVal.append(label)
                color_pos[label] = (round(servos[4].current_angle * (27/18))+ n)

            print(f"Detected: {label} ({conf:.2f})")
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            text = f"{label} {conf:.2f}"
            cv2.putText(frame, text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        print(servos[4].current_angle)
        print(color_pos)
        cv2.imshow("Custom YOLOv8 Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_detection_event.set()
            break

        if all(list(color_pos.values())):
            print("All positions found:", color_pos)
            stop_detection_event.set()
            break

    cap.release()
    cv2.destroyAllWindows()

power_gripper = 92
off_gripper = 35

def grab(base):
    pos(target_angles=[base, 64, 168, 153, off_gripper]) # down1
    pos(target_angles=[base, 27, 180, 180, off_gripper]) # down2
    # time.sleep(0.2)
    pos(target_angles=[base, 0, 108, 138, off_gripper]) # push
    servos[8].write(power_gripper) # grab

def drop(base = 38):
    servos[6].write(90)
    time.sleep(0.3)
    pos(target_angles=[135, 64, 168, 153, power_gripper])
    time.sleep(0.3)
    pos(target_angles=[base, 64, 168, 153, power_gripper], step_delay=0.004)
    time.sleep(0.3)
    pos(target_angles=[base, 49, 168, 167, power_gripper])
    time.sleep(0.5)
    pos(target_angles=[base, 64, 168, 153, off_gripper])



def st1(base):
    pos(target_angles=[base, 64, 168, 153, off_gripper])
    grab(base)
    drop()

def st2(base):
    pos(target_angles=[base, 64, 168, 153, off_gripper])
    grab(base)
    drop()

def st3(base):
    pos(target_angles=[base, 64, 168, 153, off_gripper])
    grab(base)
    drop()
def mid(base = 33):
    pos(target_angles=[base, 40, 175, 168, off_gripper])
    pos(target_angles=[base, 0, 135, 168, off_gripper])
    servos[8].write(power_gripper)
    pos(target_angles=[base, 25, 174, 180, power_gripper])
    servos[4].write(144)
    servos[8].write(10)
    servos[7].write(150)
    # ?
    pos(target_angles=[147,31,69,45,0], step_delay= 0.01)

# GUI
def on_button_click():
    global color_pos
    color_pos = {"red": 0, "green": 0, "blue": 0}
    root.destroy()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    setup()
    pos([30, 79, 118, 0, 0],step_delay=0.01)  # Initial servo position

    # Start detection immediately
    detection_thread = threading.Thread(target=detection_loop, daemon=True)
    detection_thread.start()

    # GUI to trigger check()
    def on_button_click():
        global ready
        ready = True
        root.destroy()  

    root = tk.Tk()
    root.title("Start Moving")
    start_button = tk.Button(root, text="Start", command=on_button_click,
                             font=("Arial", 14), bg="green", fg="white")
    start_button.pack(padx=100, pady=100)
    root.mainloop()  

    threading.Thread(target=check, daemon=True).start()

    detection_thread.join()

    use_pos = [color_pos["red"], color_pos["green"], color_pos["blue"]]
    pos(target_angles=[use_pos[0], 90, 90, 90, off_gripper])
    st1(base=use_pos[0])
    st2(base=use_pos[1])
    st3(base=use_pos[2])
    mid()
    input("off")
    board.exit()

