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
speed = int(input("enter motors speed, from 1 to 100 - "))
if speed > 100: speed = 99
elif speed < 10: speed = 11
# create AX12 instance with ID 10
motor_id = 2
my_dxl = Ax12(motor_id)  
my_dxl.set_moving_speed(speed)
motor_id2 = 3
my_dxl2 = Ax12(motor_id2)
my_dxl2.set_moving_speed(speed)
motor_id3 = 4
my_dxl3 = Ax12(motor_id3)
my_dxl3.set_moving_speed(speed)
motor_id4 = 5
my_dxl4 = Ax12(motor_id4)
my_dxl4.set_moving_speed(speed)
motor_id5 = 6
my_dxl5 = Ax12(motor_id5)
my_dxl5.set_moving_speed(speed)
def user_input():
    """Check to see if user wants to continue"""
    ans = input('Continue? : y/n ')
    if ans == 'n':
        return False
    else:
        return True

def coordinate_interpreter(data):
    global _xyz, _new_pos
    _xyz = (data['x'],data['y'],data['z'])
    _new_pos = (data['x'],data['y'],data['z'])

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

        motor_object.set_goal_position(int(512-m.degrees(Q2)*2.84))
        motor_object2.set_goal_position(int(512-m.degrees(Q3)*2.84))
        motor_object3.set_goal_position(int(512-m.degrees(Q4)*2.84))
        motor_object4.set_goal_position(int(512-m.degrees(Q4)*2.84))
        motor_object5.set_goal_position(int(512-m.degrees(Q4)*2.84))

        print("Position of dxl ID: %d is now: %d " %
              (motor_object.id, motor_object.get_present_position()))
        print("Position of dxl ID: %d is now: %d " %
              (motor_object2.id, motor_object2.get_present_position()))
        print("Position of dxl ID: %d is now: %d " %
              (motor_object3.id, motor_object3.get_present_position()))
        bool_test = False

# pass in AX12 object

_xyz = [0.1,0,0.1]
last_key = ""
def new_pos():
    global _xyz, last_key, _new_pos
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
        main(my_dxl, my_dxl2, my_dxl3, alf1, alf2, alf3, alf4)
        # error = sim.simxSetJointTargetPosition(clientID, J_01, alf1, sim.simx_opmode_oneshot_wait)
        # error = sim.simxSetJointTargetPosition(clientID, J_12, alf2, sim.simx_opmode_oneshot_wait)
        # error = sim.simxSetJointTargetPosition(clientID, J_13, alf3, sim.simx_opmode_oneshot_wait)
        # error = sim.simxSetJointTargetPosition(clientID, J_23, alf4, sim.simx_opmode_oneshot_wait)
        # GRIP(0, 0.03)
        # _xyz_new[1] = 0
    except Exception:
        print("координаты сброшены до: [0.3,0,0.3]")
        _xyz = [0.1,0,0.1]
        _new_pos = [0.1,0,0.1,0,0]
        alf1, alf2, alf3, alf4 = OZK_2(_xyz[0], _xyz[1], _xyz[2])
        print(alf1, alf2, alf3, alf4)
        main(my_dxl, my_dxl2, my_dxl3, alf1, alf2, alf3, alf4)
        # error = sim.simxSetJointTargetPosition(clientID, J_01, alf1, sim.simx_opmode_oneshot_wait)
        # error = sim.simxSetJointTargetPosition(clientID, J_12, alf2, sim.simx_opmode_oneshot_wait)
        # error = sim.simxSetJointTargetPosition(clientID, J_13, alf3, sim.simx_opmode_oneshot_wait)
        # error = sim.simxSetJointTargetPosition(clientID, J_23, alf4, sim.simx_opmode_oneshot_wait)






import sys

import pygame
from pygame.locals import *

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

font = pygame.font.Font(None, 20)

import sys

# Import non-standard modules.
import pygame
from pygame.locals import *

_new_pos = [0.1,0,0.1,0,0]

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
ui_slider2 = ui_slider([100,175],[300,50], [0,0,1,0,0], 125)
ui_slider3 = ui_slider([100,250],[300,50], [0,0,0,1,0], -200)
ui_slider4 = ui_slider([100,325],[300,50], [0,0,0,0,1], -200)

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
        ui_slider4.update_pos(event)

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
    ui_slider4.draw_ui(screen)

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

runPyGame()







# disconnect
my_dxl.set_torque_enable(0)
my_dxl2.set_torque_enable(0)
my_dxl3.set_torque_enable(0)
my_dxl4.set_torque_enable(0)
my_dxl5.set_torque_enable(0)
#my_dxl2.set_torque_enable(0)
Ax12.disconnect()
