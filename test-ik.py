from Ax12 import Ax12
import math as m

l1 = 0.188
l2 = 0.4
l3 = 0.32
l4 = 0.68
# l4 = 0.16

a1=0
a2=30
a3=30

alf1=a1*m.pi/180
alf2=a2*m.pi/180
alf3=a3*m.pi/180

x_targ = 0.01
z_targ = 0.03

def OZK_2(x,y,z):

    # z=z-l1
    # B = m.sqrt(x**2 + z**2)
    # q1 = m.atan2(z, x)
    # q2 = m.acos((l2**2 - l3**2 + B**2)/(2*B*l2))
    # Q1 = q1+q2
    # Q2 = m.pi-m.acos((l2**2 + l3**2 - B**2)/(2*l2*l3))

    # al2 = m.pi/2 - Q1
    # al3 = Q2
    #
    # al4 = m.atan(y/x)

    a1 = m.atan(y/x)
    a5 = a1
    k = m.sqrt(x ** 2 + y ** 2)
    zp = z + l4 - l1
    d = m.sqrt(k ** 2 + zp ** 2)
    a2 = (m.pi / 2) - (m.atan(zp / k) + m.acos((d ** 2 + l2 ** 2 - l3 ** 2) / (2 * d * l2)))
    a3 = m.pi - m.acos((-d ** 2 + l2 ** 2 + l3 ** 2) / (2 * l2 * l3))
    a4 = m.pi - (a2 + a3)

    return a1, a2, a3, a4

    # return 0, Q1, Q2, 0


# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
Ax12.DEVICENAME = '/dev/ttyACM0'

Ax12.BAUDRATE = 1_000_000

# sets baudrate and opens com port
Ax12.connect()

# create AX12 instance with ID 10
motor_id = 3
my_dxl = Ax12(motor_id)  
my_dxl.set_moving_speed(10)
motor_id2 = 4
my_dxl2 = Ax12(motor_id2)
my_dxl2.set_moving_speed(10)
motor_id2 = 5
my_dxl2 = Ax12(motor_id2)
my_dxl2.set_moving_speed(10)

def user_input():
    """Check to see if user wants to continue"""
    ans = input('Continue? : y/n ')
    if ans == 'n':
        return False
    else:
        return True


def main(motor_object, motor_object2, motor_object3, Q1, Q2, Q3, Q4):
    """ sets goal position based on user input """
    bool_test = True
    while bool_test:
        print("Position of dxl ID: %d is now: %d " %
              (motor_object.id, motor_object.get_present_position()))
        print("Position of dxl ID: %d is now: %d " %
              (motor_object2.id, motor_object2.get_present_position()))
        print("Position of dxl ID: %d is now: %d " %
              (motor_object3.id, motor_object3.get_present_position()))

        motor_object.set_goal_position(Q2)
        motor_object2.set_goal_position(Q3)
        motor_object3.set_goal_position(Q4)

        print("Position of dxl ID: %d is now: %d " %
              (motor_object.id, motor_object.get_present_position()))
        print("Position of dxl ID: %d is now: %d " %
              (motor_object2.id, motor_object2.get_present_position()))
        print("Position of dxl ID: %d is now: %d " %
              (motor_object3.id, motor_object3.get_present_position()))
        bool_test = False

# pass in AX12 object
main(my_dxl, my_dxl2, my_dxl3)

_xyz = [0.3,0,0.3]
last_key = ""
def new_pos():
    global _xyz, last_key
    # print('Введите X')
    # x_targ = float(input())
    # print('Введите Z')
    # z_targ = float(input())
    # print('Введите Y')
    # y_targ = float(input())
    # print(_xyz)
    # grip = int(input())
    _xyz_new = _xyz
    try:
        # if last_key == "y+" and _xyz_new[1] < 0.1 and _xyz_new[0] < 0.1 and _xyz_new[0] > -0.1: _xyz_new[1] = 0.2
        # elif last_key == "y-" and _xyz_new[1] < 0.1 and _xyz_new[0] < 0.1 and _xyz_new[0] > -0.1: _xyz_new[1] = -0.2
        # if _xyz[0] < 0.1 and _xyz[0] > -0.1:
        #     if last_key == "x+":
        #         _xyz[0] = -0.1
        #     else: _xyz[0] = 0.1
        alf1, alf2, alf3, alf4 = OZK_2(_xyz[0],_xyz[1],_xyz[2])
        if _xyz[0] < 0:
            alf1 += 1.57*2
        print(alf1, alf2, alf3, alf4)
        # error = sim.simxSetJointTargetPosition(clientID, J_01, alf1, sim.simx_opmode_oneshot_wait)
        # error = sim.simxSetJointTargetPosition(clientID, J_12, alf2, sim.simx_opmode_oneshot_wait)
        # error = sim.simxSetJointTargetPosition(clientID, J_13, alf3, sim.simx_opmode_oneshot_wait)
        # error = sim.simxSetJointTargetPosition(clientID, J_23, alf4, sim.simx_opmode_oneshot_wait)
        # GRIP(0, 0.03)
        _xyz_new[1] = 0
    except Exception:
        try:
            if last_key == "x+": _xyz[0] -= -0.05
            elif last_key == "x-": _xyz[0] += -0.05
            elif last_key == "y+": _xyz[1] -= -0.05
            elif last_key == "y-": _xyz[1] += -0.05
            elif last_key == "z+": _xyz[2] -= -0.05
            elif last_key == "z-": _xyz[2] += -0.05
            print(f"координаты возвращеныиз {_xyz_new} до: {_xyz} с состоянием {last_key}")
            alf1, alf2, alf3, alf4 = OZK_2(_xyz[0], _xyz[1], _xyz[2])
            print(alf1, alf2, alf3, alf4)
            # error = sim.simxSetJointTargetPosition(clientID, J_01, alf1, sim.simx_opmode_oneshot_wait)
            # error = sim.simxSetJointTargetPosition(clientID, J_12, alf2, sim.simx_opmode_oneshot_wait)
            # error = sim.simxSetJointTargetPosition(clientID, J_13, alf3, sim.simx_opmode_oneshot_wait)
            # error = sim.simxSetJointTargetPosition(clientID, J_23, alf4, sim.simx_opmode_oneshot_wait)
        except Exception:
            print("координаты сброшены до: [0.3,0,0.3]")
            _xyz = [0.3,0,0.3]
            alf1, alf2, alf3, alf4 = OZK_2(_xyz[0], _xyz[1], _xyz[2])
            print(alf1, alf2, alf3, alf4)
            # error = sim.simxSetJointTargetPosition(clientID, J_01, alf1, sim.simx_opmode_oneshot_wait)
            # error = sim.simxSetJointTargetPosition(clientID, J_12, alf2, sim.simx_opmode_oneshot_wait)
            # error = sim.simxSetJointTargetPosition(clientID, J_13, alf3, sim.simx_opmode_oneshot_wait)
            # error = sim.simxSetJointTargetPosition(clientID, J_23, alf4, sim.simx_opmode_oneshot_wait)


# print(error)

from tkinter import *
new_pos()
def x_zer():
    global last_key
    _xyz[0] += 0.05
    root.title([round(v,2) for v in _xyz])
    new_pos()
    last_key = "x-"
def x_plus():
    global last_key
    _xyz[0] -= 0.05
    root.title([round(v,2) for v in _xyz])
    new_pos()
    last_key = "x+"
def y_zer():
    global last_key
    _xyz[1] += 0.05
    root.title([round(v,2) for v in _xyz])
    new_pos()
    last_key = "y-"
def y_plus():
    global last_key
    _xyz[1] -= 0.05
    root.title([round(v,2) for v in _xyz])
    new_pos()
    last_key = "y+"
def z_zer():
    global last_key
    _xyz[2] += 0.05
    root.title([round(v,2) for v in _xyz])
    new_pos()
    last_key = "z-"
def z_plus():
    global last_key
    _xyz[2] -= 0.05
    root.title([round(v,2) for v in _xyz])
    new_pos()
    last_key = "z+"

root = Tk()
root.title("joistick")
root.geometry("250x350")
btn = Button(text="x+", background="#555", foreground="#ccc",
             padx="15", pady="7.5", font="16", command=x_zer)
btn2 = Button(text="x-", background="#555", foreground="#ccc",
             padx="16", pady="7.5", font="16", command=x_plus)
btn3 = Button(text="y+", background="#555", foreground="#ccc",
             padx="15", pady="7.5", font="16", command=y_zer)
btn4 = Button(text="y-", background="#555", foreground="#ccc",
             padx="16", pady="7.5", font="16", command=y_plus)
btn5 = Button(text="z+", background="#555", foreground="#ccc",
             padx="15", pady="7.5", font="16", command=z_zer)
btn6 = Button(text="z-", background="#555", foreground="#ccc",
             padx="16", pady="7.5", font="16", command=z_plus)

btn.pack()
btn2.pack()
btn3.pack()
btn4.pack()
btn5.pack()
btn6.pack()

root.mainloop()

# disconnect
my_dxl.set_torque_enable(0)
my_dxl2.set_torque_enable(0)
#my_dxl2.set_torque_enable(0)
Ax12.disconnect()
