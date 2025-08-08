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
 
power_gripper = 95
off_gripper = 38
 
def setup(servo_pins = servo_pins):
    for pin in servo_pins:
        servos[pin] = Servo(pin)
 
def set90():
    pos(pos = [135,90,90,90,90])
 
def pos(pos = [], pin = servo_pins, servos = servos, step_delay = 0.015):
    for i in range(len(pos)):
        servos[pin[i]].write(pos[i], step_delay = step_delay)
 
def check():
    servos[8].write(0)
    pos(pos = [40,99,150,0,0])
    pos(pos = [242,99,150,0,0])

setup()
pos(pos = [40,99,150,0,0], step_delay = 0.005)
while 1:
    check()