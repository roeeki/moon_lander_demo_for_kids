import pygame


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

    def move(self, x_speed, y_speed):
        self.player.move_ip((x_speed, y_speed))

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
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                break

            # joystick axis is between [-1,1]  on each axis
            x_speed = round(pygame.joystick.Joystick(0).get_axis(0)*5)
            y_speed = round(pygame.joystick.Joystick(0).get_axis(1)*5)
            player.move(x_speed=x_speed, y_speed=y_speed)
            # print(event)

            if event.type == pygame.JOYBUTTONDOWN:
                # print(event)
                if pygame.joystick.Joystick(0).get_button(0):
                    if player.color == "white":
                        player.color = "red"
                    elif player.color == "red":
                        player.color = "white"

                    botton_counter += 1

                if pygame.joystick.Joystick(0).get_button(1):
                    player.center()

        screen.fill((0, 0, 0))
        text_disp = '{}'.format(botton_counter)
        text_obj = font_obj.render(text_disp, True, font_color)
        screen.blit(text_obj, (22, 0))

        player.draw(screen)
        pygame.display.update()
        clock.tick(50)
