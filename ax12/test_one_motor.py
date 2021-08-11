from Ax12 import Ax12


# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
Ax12.DEVICENAME = '/dev/ttyACM0'

Ax12.BAUDRATE = 1_000_000

# sets baudrate and opens com port
Ax12.connect()
speed = int(input("enter motors speed, from 1 to 100 - "))
if speed > 100: speed = 99
elif speed < 10: speed = 11
# create AX12 instance with ID 10
motor_id = int(input("motor id set - "))
my_dxl = Ax12(motor_id)
my_dxl.set_moving_speed(speed)

print("Position of dxl ID: %d is now: %d " %
      (my_dxl.id, my_dxl.get_present_position()))
# print("Tempreche of dxl ID: %d is now: %d " %
#       (my_dxl.id, my_dxl.get_temperature()))
# print("Speed of dxl ID: %d is now: %d " %
#       (my_dxl.id, my_dxl.get_present_speed()))

my_dxl.set_goal_position(int(input("new dx rotation, from 1 to 1023 - ")))

# print("Position of dxl ID: %d is now: %d " %
#       (my_dxl.id, my_dxl.get_present_position()))
# print("Tempreche of dxl ID: %d is now: %d " %
#       (my_dxl.id, my_dxl.get_temperature()))
# print("Speed of dxl ID: %d is now: %d " %
#       (my_dxl.id, my_dxl.get_present_speed()))

import time
time.sleep(5)

my_dxl.set_torque_enable(0)
Ax12.disconnect()