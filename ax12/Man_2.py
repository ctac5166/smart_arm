import math as m
import sys
from Ax12 import Ax12


# def initial():
#     sim.simxFinish(-1)  # just in case, close all opened connections
#
#     clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
#
#     if clientID != -1:  # check if client connection successful
#         print('Connected to remote API server')
#
#     else:
#         print('Connection not successful')
#         sys.exit('Could not connect')
#     return clientID

# clientID=initial()


# error,J_01=sim.simxGetObjectHandle(clientID,'Joint_01', sim.simx_opmode_oneshot_wait)
# error,J_12=sim.simxGetObjectHandle(clientID,'Joint_12', sim.simx_opmode_oneshot_wait)
# error,J_23=sim.simxGetObjectHandle(clientID,'Joint_23', sim.simx_opmode_oneshot_wait)
# error,GJ_1=sim.simxGetObjectHandle(clientID,'Grip_joint_1', sim.simx_opmode_oneshot_wait)
# error,GJ_2=sim.simxGetObjectHandle(clientID,'Grip_joint_2', sim.simx_opmode_oneshot_wait)
# error,G_P=sim.simxGetObjectHandle(clientID,'Grip_point', sim.simx_opmode_oneshot_wait)
# error,L=sim.simxGetObjectHandle(clientID,'Load', sim.simx_opmode_oneshot_wait)

l1 = 0.165
l2 = 0.285
l3 = 0.230
l4 = 0.210

a1=0
a2=30
a3=30

alf1=a1*m.pi/180
alf2=a2*m.pi/180
alf3=a3*m.pi/180

pos = [0.2, 0.15, 0.2]

# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
Ax12.DEVICENAME = '/dev/ttyACM0'

Ax12.BAUDRATE = 1_000_000

# sets baudrate and opens com port
Ax12.connect()
# speed = int(input("enter motors speed, from 1 to 100 - "))
speed_mdx = 20
if speed_mdx > 100: speed = 99
elif speed_mdx < 10: speed = 11
# create AX12 instance with ID 10
motor_id = 1
my_dxl = Ax12(motor_id)
my_dxl.set_moving_speed(speed_mdx)
motor_id2 = 2
my_dxl2 = Ax12(motor_id2)
my_dxl2.set_moving_speed(speed_mdx)
motor_id3 = 3
my_dxl3 = Ax12(motor_id3)
my_dxl3.set_moving_speed(speed_mdx)
motor_id4 = 4
my_dxl4 = Ax12(motor_id4)
my_dxl4.set_moving_speed(speed_mdx)
motor_id5 = 5
my_dxl5 = Ax12(motor_id5)
my_dxl5.set_moving_speed(speed_mdx)
motor_id6 = 6
my_dxl6 = Ax12(motor_id6)
my_dxl6.set_moving_speed(speed_mdx)


def OZK_3(x, y, z):
    al1 = m.atan(y / abs(x))
    if x < 0: # инверсия для углов более +-pi/4
        al1 = m.pi - al1
    x = m.sqrt(x ** 2 + y ** 2)
    z = z - l1
    B = m.sqrt(x ** 2 + z ** 2)
    q1 = m.atan2(z, x)
    q2 = m.acos((l2 ** 2 - l3 ** 2 + B ** 2) / (2 * B * l2))
    Q1 = q1 + q2
    Q2 = m.pi - m.acos((l2 ** 2 + l3 ** 2 - B ** 2) / (2 * l2 * l3))

    al2 = m.pi / 2 - Q1
    al3 = Q2

    print(m.degrees(al1), m.degrees(al2), m.degrees(al3))
    return al1, al2, al3


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


# def GRIP(g,gr):
#     if (g == 1):
#         error = sim.simxSetJointTargetPosition(clientID, GJ_1, gr, sim.simx_opmode_oneshot_wait)
#         error = sim.simxSetJointTargetPosition(clientID, GJ_2, -gr, sim.simx_opmode_oneshot_wait)
#         # error = sim.simxSetObjectPosition(clientID, L, G_P, (0,0,0), sim.simx_opmode_oneshot_wait)
#         # error = sim.simxSetObjectOrientation(clientID, L, G_P, (0, 0, 0), sim.simx_opmode_oneshot_wait)
#         print('Схватил!')
#     elif (g == 0):
#         error = sim.simxSetJointTargetPosition(clientID, GJ_1, 0, sim.simx_opmode_oneshot_wait)
#         error = sim.simxSetJointTargetPosition(clientID, GJ_2, 0, sim.simx_opmode_oneshot_wait)
#         print('Не схватил!')


# def setMotorPos(targ_pos, targ_vel, JH):
#     pos_reached=0
#
#     while pos_reached == 0:
#         err, pos = sim.simxGetJointPosition(clientID, JH, sim.simx_opmode_oneshot_wait)
#         if ((pos-targ_pos)>(0.5*m.pi/180)):
#             error = sim.simxSetJointTargetVelocity(clientID, JH, -targ_vel, sim.simx_opmode_oneshot_wait)
#         elif ((pos-targ_pos)<(-0.5*m.pi/180)):
#             error = sim.simxSetJointTargetVelocity(clientID, JH, targ_vel, sim.simx_opmode_oneshot_wait)
#         elif ((-0.5*m.pi/180)<=(pos-targ_pos)<=(0.5*m.pi/180)):
#             error = sim.simxSetJointTargetVelocity(clientID, JH, 0, sim.simx_opmode_oneshot_wait)
#             pos_reached = 1


def mathf_maxi(min, max, val):
    if val < min:
        return min
    if val > max:
        return max
    return val


def inst_to_coof(Qcopy, zero_coof, coof):
    Q_new = int(zero_coof - (m.degrees(Qcopy))*coof)
    return Q_new


def main(motor_object, motor_object2, motor_object3, motor_object4, Q1, Q2, Q3, Q4):

    bool_test = True
    while bool_test:
        coof = 13.7
        zeros = 4096 / 2

        # print("ON ENTER DATA MANIP: ", m.degrees(Q1), m.degrees(Q2), m.degrees(Q3), m.degrees(Q4))

        motor_object.set_goal_position(inst_to_coof(Q1, zeros, coof))
        print(inst_to_coof(Q1, zeros, coof), math.degrees(Q1))
        motor_object2.set_goal_position(mathf_maxi(1000, 3000, int(2000-(math.degrees(Q2)*coof))))
        print(int(2000-(math.degrees(Q2)*coof)), math.degrees(Q2))
        motor_object3.set_goal_position(int(700-(math.degrees(Q3-(m.pi/2))*coof)))
        print(int(700-(math.degrees(Q3-(m.pi/2))*coof)), math.degrees(Q3))

        bool_test = False


def new_pos():
    global pos

    print(pos, 'POS')

    try:
        alf4 = 0
        alf1, alf2, alf3 = OZK_3(pos[0], pos[1], pos[2])

        print(math.degrees(alf1), math.degrees(alf2), math.degrees(alf3), "ROTS")
        main(my_dxl, my_dxl2, my_dxl3, my_dxl4, alf1, alf2, alf3, alf4)

        return ["ok", alf1, alf2, alf3, alf4]

    except Exception:
        return ["error", 0, 0, 0, 0]

    return ["fatal error", alf1, alf2, alf3, alf4]


def coordinate_interpreter(data):
    global pos, speed_mdx

    print(data['xyz'], 'data xzy')
    pos = (data['xyz'][0],data['xyz'][1],data['xyz'][2])

    my_dxl5.set_goal_position(int(820+data['rot']*(-620/180)))
    my_dxl6.set_goal_position(int(850+data['opened']*150))

    coof = 13.7
    zeros = 4096 / 2

    my_dxl4.set_goal_position(mathf_maxi(900, 2800, inst_to_coof(data['rot2'], zeros, coof)))

    print("NEW SPEED", data['speed'])

    if speed_mdx != data['speed']:
        speed_mdx = int(data['speed'])
        my_dxl.set_moving_speed(speed_mdx)
        my_dxl2.set_moving_speed(speed_mdx)
        my_dxl3.set_moving_speed(speed_mdx)
        my_dxl4.set_moving_speed(speed_mdx)
        my_dxl5.set_moving_speed(speed_mdx)

    exit_ = new_pos()
    return exit_


import threading
import math
import requests
import time


def loop():
    while True:
        url = 'http://192.168.1.161:5000//get_info'
        data = {'userid': '0.0.0.0'}
        return_data = requests.post(url, json=data)
        if return_data.ok:
            data_json = return_data.json()
            if data_json != 404:
                return_ = coordinate_interpreter(data_json)
                # print(return_, "return_")
                # print(math.degrees(return_[1]), math.degrees(return_[2]), math.degrees(return_[3]), math.degrees(return_[4]), "return_")
                coof = 13.7
                # zeros = 2049.5
                zeros = 4096 / 2
                # print(inst_to_coof(return_[1], zeros, coof), inst_to_coof(return_[2], zeros, coof), inst_to_coof(return_[3], zeros, coof), inst_to_coof(return_[4], zeros, coof), "return_")
                new_data = {'userid': '0.0.0.0', "return": str(return_[0]),
                            "table_rot": return_[1],
                            "alf_rots": [return_[2], return_[3], return_[4]],
                            "rotInfo": [return_[1], return_[2], return_[3], return_[4]]}

                url = 'http://192.168.1.161:5000//set_info_manip'
                data = new_data
                return_data = requests.post(url, json=data)
            if return_data.ok:
                print(return_data.text)
        else:
            time.sleep(0.1)
        time.sleep(0.1)


threading.Thread(target=loop, daemon=True).start()
input('Press <Enter> to exit.')


my_dxl.set_torque_enable(0)
my_dxl2.set_torque_enable(0)
my_dxl3.set_torque_enable(0)
my_dxl4.set_torque_enable(0)
my_dxl5.set_torque_enable(0)
Ax12.disconnect()



# error = sim.simxSetJointTargetPosition (clientID, J_01, 0, sim.simx_opmode_oneshot_wait)




# while 0:
#     print('Введите X')
#     x_targ = float(input())
#     print('Введите Y')
#     y_targ = float(input())
#     print('Введите Z')
#     z_targ = float(input())
#     print('Схватить ли обьект')
#     grip = int(input())
#
#     alf2, alf3, alf4, alf5 = OZK_2(x_targ, y_targ, z_targ)
#
#
#     error = sim.simxSetJointTargetPosition(clientID, J_01, alf2, sim.simx_opmode_oneshot_wait)
#     error = sim.simxSetJointTargetPosition(clientID, J_12, alf3, sim.simx_opmode_oneshot_wait)
#     error = sim.simxSetJointTargetPosition(clientID, J_23, alf4, sim.simx_opmode_oneshot_wait)
#     GRIP(grip, 0.03)

# print(error)






















# setMotorPos(alf1, 0.05, J_01)
# setMotorPos(alf2, 0.05, J_12)
# setMotorPos(alf3, 0.05, J_23)