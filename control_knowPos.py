from pyfirmata2 import Arduino
import time
 
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
 
power_gripper = 95
off_gripper = 47
 
def setup(servo_pins = servo_pins):
    for pin in servo_pins:
        servos[pin] = Servo(pin)
 
def set90():
    pos(pos = [135,90,90,90,90])
 
def pos(pos = [], pin = servo_pins, servos = servos, step_delay = 0.007):
    for i in range(len(pos)):
        servos[pin[i]].write(pos[i], step_delay = step_delay)
 
def check():
    servos[8].write(0)
    pos(pos = [40,99,150,0,0])
    time.sleep(3)
    pos(pos = [242,99,150,0,0], step_delay=0.01)
 
def grab_normal(base):
    pos(pos = [base,0,156,169,power_gripper])

def grab_ad(base):
    servos[6].write(146)
    servos[7].write(154)
    pos(pos = [base,10,146,154,power_gripper])

def drop_normal(base):
    pos(pos = [base,13,156,180,off_gripper])
def drop_ad(base):
    pos(pos = [base,15,151,165,off_gripper])

def st1(base = 125):
    time.sleep(0.5)
    servos[8].write(off_gripper)
    servos[7].write(180)
    pos(pos = [base,90,90,180,0], ) # up
    pos(pos = [base,90,180,163,0]) #bit up
    grab_ad(base)if base == use_pos[2] else grab_normal(base)

def st2(base = 125):
    servos[6].write(120) # 130
    drop_ad(base) if base == use_pos[2] else drop_normal(base)
    time.sleep(0.2)
    grab_ad(base) if base == use_pos[2] else grab_normal(base)

 
def st3(base = 125):
    servos[6].write(120) 
    drop_ad(base) if base == use_pos[2] else drop_normal(base)
    servos[5].write(40)
    time.sleep(0.2)
    pos(pos = [135,90,90,90,off_gripper])
    # servos[7].write(180)
    # grab_ad(base) if base == use_pos[2] else grab_normal(base)
    time.sleep(0.5)
    servos[8].write(off_gripper)
    servos[7].write(180)
    pos(pos = [base,90,180,180,0], ) # up
    pos(pos = [base,90,180,163,0]) #bit up
    input()
    grab_ad(base)if base == use_pos[2] else grab_normal(base, n = 0)

def drop(base = 30):
    time.sleep(0.3)
    servos[5].write(90)
    servos[7].write(90)
    pos(pos = [base,90,162,90,power_gripper]) # down
    servos[7].write(180)
    pos(pos = [base,10,162,180,power_gripper], step_delay=0.01)

def grab(base = 40):
    time.sleep(0.3)
    servos[7].write(155)
    servos[6].write(136)
    servos[4].write(135, step_delay = 0.01)
    servos[8].write(10)
    servos[7].write(145)
    servos[6].write(110)
    servos[4].write(135)

    
setup()
servos[8].write(0)
 
a = 82
b = 184
c = 239
base_= 33
use_pos = [b,c,a]
st1(base=use_pos[0])
st2(base=use_pos[1])
st3(base=use_pos[2])
drop(base = base_)
grab()
 
 