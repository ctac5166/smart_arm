import math

from Ax12 import Ax12
import math as m

l1 = 0.17
l2 = 0.2
l3 = 0.135
l4 = 0.205
# l4 = 0.16
# l4 = 0.16

a1=0
a2=30
a3=30

alf1=a1*m.pi/180
alf2=a2*m.pi/180
alf3=a3*m.pi/180

x_targ = 0.3
z_targ = 0.03

def OZK_4(x,y,z):
    al1 = m.atan(y / abs(x))

    if x < 0:  # инверсия для углов более +-pi/4
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

    print(al1, al2, al3)
    return al1, al2, al3

def OZK_2(x,y,z):

    print("ON ENTER: ", x,y,z)

    a1 = m.atan(y / x)
    a5 = a1
    k = m.sqrt(x ** 2 + y ** 2)
    zp = z + l4 - l1
    d = m.sqrt(k ** 2 + zp ** 2)
    a2 = (m.pi / 2) - (m.atan(zp / k) + m.acos((d ** 2 + l2 ** 2 - l3 ** 2) / (2 * d * l2)))
    a3 = m.pi - m.acos((-d ** 2 + l2 ** 2 + l3 ** 2) / (2 * l2 * l3))
    a4 = m.pi - (a2 + a3)

    return a1, a2, a3, a4

    # return 0, Q1, Q2, 0


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

    print(al1, al2, al3)
    return al1, al2, al3


# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
Ax12.DEVICENAME = '/dev/ttyACM0'

Ax12.BAUDRATE = 1_000_000

# sets baudrate and opens com port
Ax12.connect()
# speed = int(input("enter motors speed, from 1 to 100 - "))
speed = 100
if speed > 100: speed = 99
elif speed < 10: speed = 11
# create AX12 instance with ID 10
motor_id = 1
my_dxl = Ax12(motor_id)
my_dxl.set_moving_speed(speed)
motor_id2 = 2
my_dxl2 = Ax12(motor_id2)
my_dxl2.set_moving_speed(speed)
motor_id3 = 3
my_dxl3 = Ax12(motor_id3)
my_dxl3.set_moving_speed(speed)
motor_id4 = 4
my_dxl4 = Ax12(motor_id4)
my_dxl4.set_moving_speed(speed)
motor_id5 = 5
my_dxl5 = Ax12(motor_id5)
my_dxl5.set_moving_speed(speed)
motor_id6 = 6
my_dxl6 = Ax12(motor_id6)
my_dxl6.set_moving_speed(speed)
last_coords = []
def user_input():
    """Check to see if user wants to continue"""
    ans = input('Continue? : y/n ')
    if ans == 'n':
        return False
    else:
        return True

_xyz = [0.1, 0, 0.27]

def coordinate_interpreter(data):
    global _xyz, _new_pos, last_coords, speed_mdx
    print(data, "datadatadata")

    last_coords = _xyz;
    print(data['xyz'], 'data xzy')
    _new_pos = (data['xyz'][0],data['xyz'][1],data['xyz'][2])
    _xyz = _new_pos

    my_dxl5.set_goal_position(int(820+data['rot']*(-620/180)))
    my_dxl6.set_goal_position(int(850+data['opened']*150))

    coof = 13.7
    zeros = 4096 / 2

    my_dxl4.set_goal_position(mathf_maxi(900, 2800, inst_to_coof(data['rot2'], zeros, coof)))

    if speed_mdx != data['speed']:
        speed_mdx = int(data['speed'])
        my_dxl.set_moving_speed(speed_mdx)
        my_dxl2.set_moving_speed(speed_mdx)
        my_dxl3.set_moving_speed(speed_mdx)
        my_dxl4.set_moving_speed(speed_mdx)
        my_dxl5.set_moving_speed(speed_mdx)

    exit_ = new_pos()
    return exit_

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

        print("ON ENTER DATA MANIP: ", m.degrees(Q1), m.degrees(Q2), m.degrees(Q3), m.degrees(Q4))

        motor_object.set_goal_position(inst_to_coof(Q1, zeros, coof))
        motor_object2.set_goal_position(mathf_maxi(1250, 2980, inst_to_coof(Q2, zeros, coof)))
        motor_object3.set_goal_position(mathf_maxi(1310, 3100, inst_to_coof(Q3 - (m.pi / 2), zeros, coof)))

        bool_test = False

# pass in AX12 object

speed_mdx = 25
last_key = ""
def new_pos():
    global _xyz, last_key, _new_pos, last_coords
    # print('Введите X')
    # x_targ = float(input())
    # print('Введите Z')
    # z_targ = float(input())
    # print('Введите Y')
    # y_targ = float(input())
    # print(_xyz)
    # grip = int(input())
    _xyz_new = _xyz
    print(_xyz, "xyz")
    # try:
        # if last_key == "y+" and _xyz_new[1] < 0.1 and _xyz_new[0] < 0.1 and _xyz_new[0] > -0.1: _xyz_new[1] = 0.2
        # elif last_key == "y-" and _xyz_new[1] < 0.1 and _xyz_new[0] < 0.1 and _xyz_new[0] > -0.1: _xyz_new[1] = -0.2
        # if _xyz[0] < 0.1 and _xyz[0] > -0.1:
        #     if last_key == "x+":
        #         _xyz[0] = -0.1
        #     else: _xyz[0] = 0.1
    alf4 = 0
    alf1, alf2, alf3, alf4 = OZK_2(_xyz[0],_xyz[1],_xyz[2])
    if _xyz[0] < 0:
        alf1 += 1.57*2
    print(alf1, alf2, alf3, alf4)
    main(my_dxl, my_dxl2, my_dxl3, my_dxl4, alf1, alf2, alf3, alf4)
    # error = sim.simxSetJointTargetPosition(clientID, J_01, alf1, sim.simx_opmode_oneshot_wait)
    # error = sim.simxSetJointTargetPosition(clientID, J_12, alf2, sim.simx_opmode_oneshot_wait)
    # error = sim.simxSetJointTargetPosition(clientID, J_13, alf3, sim.simx_opmode_oneshot_wait)
    # error = sim.simxSetJointTargetPosition(clientID, J_23, alf4, sim.simx_opmode_oneshot_wait)
    # GRIP(0, 0.03)
    # _xyz_new[1] = 0
    return ["ok", alf1, alf2, alf3, alf4]
    # except Exception:
    #     try:
    #         _xyz = last_coords
    #         _new_pos = last_coords
    #         alf1, alf2, alf3, alf4 = OZK_2(_xyz[0],_xyz[1],_xyz[2])
    #         print(alf1, alf2, alf3, alf4)
    #         main(my_dxl, my_dxl2, my_dxl3, my_dxl4, alf1, alf2, alf3, alf4)
    #         # my_dxl.set_torque_enable(0)
    #         # my_dxl2.set_torque_enable(0)
    #         # my_dxl3.set_torque_enable(0)
    #         # my_dxl4.set_torque_enable(0)
    #         # my_dxl5.set_torque_enable(0)
    #         # # my_dxl2.set_torque_enable(0)
    #         # Ax12.disconnect()
    #         return ["tomuch", alf1, alf2, alf3, alf4]
    #     except Exception:
    #         print("координаты сброшены до: [0.3,0,0.3]")
    #         _xyz = [0.2,0,0.3]
    #         _new_pos = [0.2,0,0.3,0,0]
    #         alf1, alf2, alf3, alf4 = 0,0,0,0
    #         try:
    #             alf1, alf2, alf3, alf4 = OZK_2(_xyz[0],_xyz[1],_xyz[2])
    #             print(alf1, alf2, alf3, alf4)
    #             main(my_dxl, my_dxl2, my_dxl3, my_dxl4, alf1, alf2, alf3, alf4)
    #         except Exception:
    #             print('error coords')
    #         # error = sim.simxSetJointTargetPosition(clientID, J_01, alf1, sim.simx_opmode_oneshot_wait)
    #         # error = sim.simxSetJointTargetPosition(clientID, J_12, alf2, sim.simx_opmode_oneshot_wait)
    #         # error = sim.simxSetJointTargetPosition(clientID, J_13, alf3, sim.simx_opmode_oneshot_wait)
    #         # error = sim.simxSetJointTargetPosition(clientID, J_23, alf4, sim.simx_opmode_oneshot_wait)
    #         # my_dxl.set_torque_enable(0)
    #         # my_dxl2.set_torque_enable(0)
    #         # my_dxl3.set_torque_enable(0)
    #         # my_dxl4.set_torque_enable(0)
    #         # my_dxl5.set_torque_enable(0)
    #         # # my_dxl2.set_torque_enable(0)
    #         # Ax12.disconnect()
    #         return ["error", alf1, alf2, alf3, alf4]


import sys

import pygame
from pygame.locals import *

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
# screen = pygame.display.set_mode((width, height))

font = pygame.font.Font(None, 20)

import sys

# Import non-standard modules.
import pygame
from pygame.locals import *

_new_pos = [0.4,0,0.3,0,0]

class ui_slider(object):
    def __init__(self, pose, scale, dir, cof):
        self.start_slide = False
        self.is_down = False
        self.slider_pos1 = pose
        self.slider_scale1 = scale
        self.slider_rad1 = self.slider_scale1[1]/2
        self.ce_pos = [self.slider_pos1[0] + self.slider_scale1[0] / 2, self.slider_pos1[1] + self.slider_scale1[1] / 2]
        self.direction = dir
        self.cof = cof

    def update_pos(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.is_down = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_down = False
                self.ce_pos[0] = self.slider_pos1[0] + self.slider_scale1[0] / 2
                self.start_slide = False

        if self.is_down:
            pos = pygame.mouse.get_pos()
            if pos[0] > self.slider_pos1[0] + self.slider_rad1 and pos[0] < self.slider_pos1[0] + self.slider_scale1[0] - self.slider_rad1 or self.start_slide:
                if pos[1] > self.slider_pos1[1] and pos[1] < self.slider_pos1[1] + self.slider_scale1[1] or self.start_slide:
                    self.start_slide = True
                    if pos[0] > self.slider_pos1[0] + self.slider_rad1 and pos[0] < self.slider_pos1[0] + self.slider_scale1[
                        0] - self.slider_rad1:
                        self.ce_pos[0] = (pos[0])
                    elif pos[0] < self.slider_pos1[0] + self.slider_rad1:
                        self.ce_pos[0] = self.slider_pos1[0] + self.slider_rad1
                    else:
                        self.ce_pos[0] = self.slider_pos1[0] + self.slider_scale1[0] - self.slider_rad1


    def draw_ui(self, screen):
        global _new_pos
        for i in range(3):
            _new_pos[i] += self.direction[i] * ((self.ce_pos[0] - (self.slider_pos1[0] + self.slider_scale1[0] / 2)) / (
                        self.slider_scale1[0] / 2 - self.slider_rad1)) / self.cof

        pygame.draw.rect(screen, (0, 0, 0),
                         (int(self.slider_pos1[0]), int(self.slider_pos1[1]), int(self.slider_scale1[0]), int(self.slider_scale1[1])), 2)
        pygame.draw.circle(screen, (0, 0, 0),
                           (int(self.ce_pos[0]), int(self.ce_pos[1])), int(self.slider_rad1), 2)

ui_slider1 = ui_slider([100,100],[300,50], [1,0,0,0,0], 125)
ui_slider2 = ui_slider([100,175],[300,50], [0,1,0,0,0], 125)
ui_slider3 = ui_slider([100,250],[300,50], [0,0,1,0,0], 125)
# ui_slider4 = ui_slider([100,325],[300,50], [0,0,0,0,1], -200)

def update(dt):
    global ui_slider1

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            return

        ui_slider1.update_pos(event)
        ui_slider2.update_pos(event)
        ui_slider3.update_pos(event)
        # ui_slider4.update_pos(event)

def draw(screen):
    global _xyz

    screen.fill((255, 255, 255))
    text1 = font.render(str([round(v,3) for v in _new_pos]), 1, (0, 0, 0))
    screen.blit(text1, (215, 75))

    _xyz = [_new_pos[0], _new_pos[1], _new_pos[2]]
    new_pos()

    ui_slider1.draw_ui(screen)
    ui_slider2.draw_ui(screen)
    ui_slider3.draw_ui(screen)
    # ui_slider4.draw_ui(screen)

    pygame.display.flip()


def runPyGame():
    pygame.init()
    fps = 25.0
    fpsClock = pygame.time.Clock()

    # Set up the window.
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))

    # screen is the surface representing the window.
    # PyGame surfaces can be thought of as screen sections that you can draw onto.
    # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.

    # Main game loop.
    dt = 1 / fps  # dt is the time since last frame.
    while True:  # Loop forever!
        update(dt)  # You can update/draw here, I've just moved the code for neatness.
        draw(screen)

        print([round(v,3) for v in _new_pos])
        dt = fpsClock.tick(fps)

# runPyGame() #запуск приложения для ручного упарвления


# from flask import Flask, request, render_template
# from flask import render_template, request, jsonify
#
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def index():
#     return "🌵 . . |=~this-is-empty~=| .. . 🌵"
#
#
# @app.route('/coords/info/get', methods=['POST', 'GET'])
# def get_info():
#     print("start")
#     data = request.json
#     print(data)
#     return_ = coordinate_interpreter(data)
#     print(return_, "return_")
#     print(math.degrees(return_[1]), math.degrees(return_[2]), math.degrees(return_[3]), math.degrees(return_[4]), "return_")
#     coof = 13.7
#     # zeros = 2049.5
#     zeros = 4096 / 2
#     print(inst_to_coof(return_[1], zeros, coof), inst_to_coof(return_[2], zeros, coof), inst_to_coof(return_[3], zeros, coof), inst_to_coof(return_[4], zeros, coof), "return_")
#     return jsonify({"return": str(return_[0]), "rotInfo": [return_[1],return_[2],return_[3],return_[4]]})
#
#
# @app.route('/get_temperature', methods=['GET, POST'])
# def get_temp():
#     global my_dxl, my_dxl2, my_dxl3, my_dxl4, my_dxl5
#
#     temperature_list = list()
#
#     temperature_list.append(my_dxl.get_temperature())
#     temperature_list.append(my_dxl2.get_temperature())
#     temperature_list.append(my_dxl3.get_temperature())
#     temperature_list.append(my_dxl4.get_temperature())
#     temperature_list.append(my_dxl5.get_temperature())
#
#     return jsonify({"temperature": temperature_list})
#
#
# @app.route('/get_speed', methods=['GET, POST'])
# def get_speed():
#     global my_dxl, my_dxl2, my_dxl3, my_dxl4, my_dxl5
#
#     speed_list = list()
#
#     speed_list.append(my_dxl.get_present_speed())
#     speed_list.append(my_dxl2.get_present_speed())
#     speed_list.append(my_dxl3.get_present_speed())
#     speed_list.append(my_dxl4.get_present_speed())
#     speed_list.append(my_dxl5.get_present_speed())
#
#     return jsonify({"speed": speed_list})
#
#
# if __name__ == "__main__":
#     app.run(host="192.168.0.23", debug=True, port=8080)


import threading
import requests
import time


def loop():
    while True:
        url = 'http://192.168.120.79:5000//get_info'
        data = {'userid': '0.0.0.0'}
        return_data = requests.post(url, json=data)
        if return_data.ok:
            data_json = return_data.json()
            if data_json != 404:
                return_ = coordinate_interpreter(data_json)
                print(return_, "return_")
                print(math.degrees(return_[1]), math.degrees(return_[2]), math.degrees(return_[3]), math.degrees(return_[4]), "return_")
                coof = 13.7
                # zeros = 2049.5
                zeros = 4096 / 2
                print(inst_to_coof(return_[1], zeros, coof), inst_to_coof(return_[2], zeros, coof), inst_to_coof(return_[3], zeros, coof), inst_to_coof(return_[4], zeros, coof), "return_")
                new_data = {'userid': '0.0.0.0', "return": str(return_[0]),
                            "table_rot": return_[1],
                            "alf_rots": [return_[2], return_[3], return_[4]],
                            "rotInfo": [return_[1], return_[2], return_[3], return_[4]]}

                url = 'http://192.168.120.79:5000//set_info_manip'
                data = new_data
                return_data = requests.post(url, json=data)
            if return_data.ok:
                print(return_data.text)
        else:
            time.sleep(0.1)
        time.sleep(0.1)


threading.Thread(target=loop, daemon=True).start()
input('Press <Enter> to exit.')


# disconnect
my_dxl.set_torque_enable(0)
my_dxl2.set_torque_enable(0)
my_dxl3.set_torque_enable(0)
my_dxl4.set_torque_enable(0)
my_dxl5.set_torque_enable(0)
#my_dxl2.set_torque_enable(0)
Ax12.disconnect()
