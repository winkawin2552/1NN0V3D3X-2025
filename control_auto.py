from pyfirmata2 import Arduino
import time
 
import zmq
import json
 
board = Arduino('/dev/ttyACM0')
 
board.samplingOn()
 
servo_pins = [4, 5, 6, 7, 8]
 
servos = {}

class Servo:
 
    def __init__(self, pin):
 
        self.servo_pin = board.get_pin(f'd:{pin}:s')

        self.pin = pin
 
        self.current_angle = 90  # start at 90
 
        self.servo_pin.write(self.current_angle)
 
    def write(self, target_angle, step_delay=0.0075):
        if self.pin ==4:
            target_angle = target_angle * (180/270)
 
        step = 1 if target_angle > self.current_angle else -1
 
        for angle in range(int(self.current_angle), int(target_angle) + step, step):
 
            self.servo_pin.write(angle)
 
            time.sleep(step_delay)
 
        self.current_angle = target_angle
 
power_gripper = 93
off_gripper = 35
 
def setup(servo_pins = servo_pins):
    for pin in servo_pins:
        servos[pin] = Servo(pin)
 
def set90():
    pos(pos = [135,90,90,90,90])
 
def pos(pos = [], pin = servo_pins, servos = servos, step_delay = 0.008):
    for i in range(len(pos)):
        servos[pin[i]].write(pos[i], step_delay = step_delay)
 
def check():
    servos[8].write(0)
    pos(pos = [40,99,150,0,0])
    time.sleep(3)
    pos(pos = [242,99,150,0,0])
 


def st1(base = 125):
    time.sleep(0.5)
    servos[8].write(0)
    servos[7].write(180)
    pos(pos = [135,90,90,180,0], ) # up
    pos(pos = [base,90,180,163,0]) #bit up
    pos(pos = [base,13,162,163,power_gripper]) # down

def st2(base = 125):
    servos[6].write(90)
    pos(pos = [135,90,90,180,power_gripper], ) # up
    pos(pos = [base,35,180,167,off_gripper]) # down
    pos(pos = [base,60,180,167,off_gripper]) # down
    time.sleep(1)
    pos(pos = [base,60,180,163,off_gripper]) #bit up
    pos(pos = [base,13,162,163,power_gripper]) # down
 
def st3(base = 125):
    servos[6].write(90)
    pos(pos = [135,90,90,180,power_gripper], ) # up
    pos(pos = [base,35,180,167,off_gripper]) # down
    pos(pos = [base,60,180,167,off_gripper]) # down
    time.sleep(1)
    pos(pos = [base,60,180,163,off_gripper]) #bit up
    pos(pos = [base,13,162,163,power_gripper]) # down

def drop(base = 30):
    servos[6].write(162)
    servos[5].write(90)
    pos(pos = [base,90,162,180,power_gripper]) # down
    servos[5].write(10)
    time.sleep(1)
    servos[8].write(off_gripper)

def grab(base = 40):
    servos[8].write(off_gripper)
    time.sleep(1)
    servos[7].write(155)
    servos[6].write(136)
    servos[4].write(144, step_delay = 0.01)
    servos[6].write(110)
    servos[8].write(10)
    servos[4].write(135)

    
setup()
servos[8].write(0)
pos(pos = [40,99,150,0,0])

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5560")
subscriber.setsockopt_string(zmq.SUBSCRIBE, "jsondata")

while 1:
    message = subscriber.recv_string()
    topic, json_payload = message.split(' ', 1)
    num = json.loads(json_payload)
    if num == 1:
        break

check()

# now wait for next real JSON list
message = subscriber.recv_string()
topic, json_payload = message.split(' ', 1)
use_pos = json.loads(json_payload)

message = subscriber.recv_string()
topic, json_payload = message.split(' ', 1)
use_pos = json.loads(json_payload)
print(f"blue {use_pos[0]}, green {use_pos[1]}, red {use_pos[2]}")

 
time.sleep(1)
a = 100
b = 175
c = 242 #245
base_= 35
 
 
st1(base=use_pos[0])
st2(base=use_pos[1])
st3(base=use_pos[2])
drop(base = base_)
grab()
 
 
# set90()
 
 