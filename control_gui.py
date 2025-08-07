from tkinter import Tk, Scale, HORIZONTAL, Label, Button, Entry
from pyfirmata2 import Arduino

# Auto-detect the board or specify port
board = Arduino('/dev/ttyACM0')
board.samplingOn()

servo_pins = [4, 5, 6, 7, 8]
servos = {}
sliders = {}
entries = {}

# Attach servos
for pin in servo_pins:
    servos[pin] = board.get_pin(f'd:{pin}:s')

root = Tk()
root.title("Servo Control GUI")


def update_servo(angle, pin):
    try:
        angle = int(float(angle))
    except ValueError:
        return
    
    if pin == 4:
        angle = min(angle, 270)
        angle = angle * (180 / 270)
    else:
        angle = min(angle, 180)

    servos[pin].write(angle)

    # Update Entry to match slider
    if pin in entries:
        entries[pin].delete(0, 'end')
        entries[pin].insert(0, str(int(float(sliders[pin].get()))))


def on_entry_change(event, pin):
    try:
        val = float(entries[pin].get())
        sliders[pin].set(val)
        update_servo(val, pin)
    except ValueError:
        pass  # Ignore invalid input


def reset_servos():
    servos[8].write(169)
    pos = [82, 0, 156, 169, 0]
    for i, pin in enumerate(servo_pins):
        servos[pin].write(pos[i])
        sliders[pin].set(pos[i])
        entries[pin].delete(0, 'end')
        entries[pin].insert(0, str(pos[i]))


# Create sliders + entries
for idx, pin in enumerate(servo_pins):
    max_angle = 270 if pin == 4 else 180

    Label(root, text=f"Servo on Pin {pin}").grid(row=idx, column=0, padx=10, pady=5)

    slider = Scale(
        root,
        from_=0,
        to=max_angle,
        orient=HORIZONTAL,
        length=200,
        command=lambda value, p=pin: update_servo(value, p)
    )
    slider.grid(row=idx, column=1, padx=10, pady=5)
    sliders[pin] = slider

    entry = Entry(root, width=5)
    entry.grid(row=idx, column=2)
    entry.insert(0, "0")
    entry.bind("<Return>", lambda event, p=pin: on_entry_change(event, p))
    entries[pin] = entry

reset_button = Button(root, text="Reset All to Default", command=reset_servos)
reset_button.grid(row=len(servo_pins), column=0, columnspan=3, pady=10)

root.mainloop()
