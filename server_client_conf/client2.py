import serial
import time
import serial.tools.list_ports

###PRINT ALL SERIAL PORTES
ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

#set up serial connection to Arduino
arduino = serial.Serial('COM3', 57600)  # Adjust the port name if needed
time.sleep(2)  

def send_command(speed, axis):
    command = f"{speed}{axis},"
    arduino.write(command.encode())
    print(f"Sent: {command}")

def set_led_intensity(intensity):
    command = f"{intensity}L,"
    arduino.write(command.encode())
    print(f"Sent: {command}")

def stop_motors():
    arduino.write(b'O,')
    print("Sent: O,")

if __name__ == "__main__":
    try:
        while True:
            print("Choose an option:")
            print("1. Move Stepper Motor")
            print("2. Set LED Intensity")
            print("3. Stop Motors")
            choice = input("Enter your choice (1/2/3): ").strip()

            if choice == '1':
                axis = input("Enter axis (X, Y, Z): ").strip().upper()
                if axis in ['X', 'Y', 'Z']:
                    speed = int(input("Run cloclwise or counter : ").strip())
                    send_command(speed, axis)
                else:
                    print("Invalid axis. Try again.")
            elif choice == '2':
                intensity = int(input("Enter LED intensity (0-20): ").strip())
                set_led_intensity(intensity)
            elif choice == '3':
                stop_motors()
            else:
                print("Invalid choice. Try again.")
    except KeyboardInterrupt:
        print("Program terminated.")
    finally:
        arduino.close()
