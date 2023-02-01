import pygame
import time
import maestro
import numpy as np


class Player(object):

    def __init__(self, x_range, y_range, width, height):
        self.x_range = x_range
        self.y_range = y_range
        self.width = width
        self.height = height
        self.x_center = (x_range[0] + x_range[1])/2
        self.y_center = (y_range[0] + y_range[1])/2
        self.player = pygame.rect.Rect((self.x_center, self.y_center, self.width, self.height))
        self.color = "white"

    def move(self, x_joystick, y_joystick):
        self.player.move_ip((x_joystick, y_joystick))

    def change_color(self, color):
        self.color = color

    def center(self):
        self.player.update(self.x_center, self.y_center, self.width, self.height)

    def draw(self, game_screen):
        pygame.draw.rect(game_screen, self.color, self.player)


if __name__ == "__main__":
    print('joystick demo:')
    print('- control rectangle position with joystick axis motion')
    print('- button 0 - change color')
    print('- button 1 - recenter')

    servo = maestro.Controller()

    screen_height = 600
    screen_width = 800

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    print(joysticks)

    player = Player([0, screen_width], [0, screen_height], 70, 50)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Joystick demo')

    # print(pygame.joystick.Joystick(0).get_numhats())
    pygame.font.init()
    font_color = (0, 150, 250)
    font_obj = pygame.font.Font('freesansbold.ttf', 25)
    botton_counter = 0

    servo_target = 6000
    # servo_target = int(4000)
    # servo.setAccel(0, 10)  # set servo 0 acceleration to 4
    # servo.setTarget(0, servo_target)  # set servo to move to center position
    # servo.setSpeed(0, 30)  # set speed of servo 1
    time.sleep(5)

    max_angular_speed = 60/0.18  # deg/sec
    pwm_2_deg = 700/8000         # deg/(quarter msec)
    deg_2_pwm = 1/pwm_2_deg
    loop_time_step = 1  # sec
    max_pwm_per_step = (loop_time_step * max_angular_speed*deg_2_pwm) / 3

    joystick_motion_axis_max = 5
    r = max_pwm_per_step/joystick_motion_axis_max
    r = 70
    print('----- ready!')

    while True:

        events = pygame.event.get()

        if len(events) > 0:
            event = events[-1]
            # for event in pygame.event.get():

            if event.type == pygame.QUIT:
                break

            # joystick axis is between [-1,1]  on each axis
            x_joystick = round(pygame.joystick.Joystick(0).get_axis(0)*5)
            y_joystick = round(pygame.joystick.Joystick(0).get_axis(1)*5)
            # print('{},{}'.format(x_joystick,y_joystick))

            if np.abs(y_joystick) > 1:

                servo_target_diff = y_joystick*r

                servo_target += int(servo_target_diff)
                servo_target = np.max([servo_target, 4000])
                servo_target = np.min([servo_target, 8000])
                # print(servo_target)
                print('{}:{},{}'.format(servo_target,servo_target_diff, y_joystick))

                if y_joystick>0:
                    servo_speed = 9
                else:
                    servo_speed = 15

                servo.setAccel(0, 10)      #set servo 0 acceleration to 4
                servo.setTarget(0, servo_target)  #set servo to move to center position
                servo.setSpeed(0, servo_speed)     #set speed of servo 1

                exec_time = (0.03/500)*np.abs(servo_target_diff)
                print('t={}'.format(exec_time))
                time.sleep(exec_time)

                # player.move(x_joystick=x_joystick, y_joystick=y_joystick)
                # # print(event)
                #
                # if event.type == pygame.JOYBUTTONDOWN:
                #     # print(event)
                #     if pygame.joystick.Joystick(0).get_button(0):
                #         if player.color == "white":
                #             player.color = "red"
                #         elif player.color == "red":
                #             player.color = "white"
                #
                #         botton_counter += 1
                #
                #     if pygame.joystick.Joystick(0).get_button(1):
                #         player.center()

        screen.fill((0, 0, 0))
        # text_disp = '{}'.format(botton_counter)
        # text_obj = font_obj.render(text_disp, True, font_color)
        # screen.blit(text_obj, (22, 0))
        #
        player.draw(screen)
        pygame.display.update()
        clock.tick(50)
