import serial
import sys
from pynput.keyboard import Key, KeyCode, Listener

# Set up serial communication
###PRINT ALL SERIAL PORTES
#ports = serial.tools.list_ports.comports()
#for port, desc, hwid in sorted(ports):
#        print("{}: {} [{}]".format(port, desc, hwid))

#set up serial connection to Arduino
ser = serial.Serial('COM3', 57600)  # Adjust the port name if needed
#ser = serial.Serial('/dev/ttyACM0', 57600)

# Initial settings
speed = 550  # Speed for stepper motors
LEDintensity = 0  # LED intensity
state = 'O'  # Initial state

def send_data(command):
    ser.write(command.encode())

def on_press(key):
    global speed, LEDintensity, state
    
    # Motor control
    if key == Key.right:
        send_data(f"{speed}X,")
        state = 'X'
    elif key == Key.left:
        send_data(f"{-speed}X,")
        state = 'X'
    elif key == Key.up:
        send_data(f"{speed}Y,")
        state = 'Y'
    elif key == Key.down:
        send_data(f"{-speed}Y,")
        state = 'Y'
    elif key == KeyCode(char='u'):
        send_data(f"{speed}Z,")
        state = 'Z'
    elif key == KeyCode(char='d'):
        send_data(f"{-speed}Z,")
        state = 'Z'
    
    # LED control
    elif key == KeyCode(char='L'):
        if LEDintensity < 236:
            LEDintensity += 20
        send_data(f"{LEDintensity}L,")
    elif key == KeyCode(char='l'):
        if LEDintensity > 21:
            LEDintensity -= 20
        send_data(f"{LEDintensity}L,")
    
def on_release(key):
    global state
    # Stop motors when keys are released
    if key in [Key.up, Key.down, Key.left, Key.right, KeyCode(char='u'), KeyCode(char='d')]:
        send_data("0O,")
        state = 'O'
    
    # Exit on ESC
    if key == Key.esc:
        ser.close()
        sys.exit()

# Collect keyboard events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
