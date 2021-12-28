import os
import pygame
import math
import tkinter
import tkinter.filedialog
import tkinter.messagebox

pygame.init()


def touched(x1, weight1, x2, weight2, y1, height1, y2, height2):
    if (x1 <= x2 and x2 <= (x1 + weight1)
        and y1 <= y2 and y2 <= (y1 + height1)) \
            or (x1 <= (x2 + weight2) and (x1 + weight1) >= x2
                and y1 <= (y2 + height2) and (y1 + height1) >= y2):
        return True
    else:
        return False


class Button:
    def __init__(self, display_width, display_height, position=None, font_name='Berlin Sans FB Demi', custom_font_path='', font_size=40,
                 bold=False, smooth=True, color=(0, 0, 0), text='Button', background=None, depth=1, angle_depth=135, size=None):
        if position is None:
            self.position = [0, 0]
        else:
            self.position = position
        self.font_name = font_name
        self.font_size = font_size
        self.bold = bold
        self.smooth = smooth
        self.init_color = color
        self.color = list(self.init_color)
        self.background = background
        self.text = text
        self.WIDTH = display_width
        self.HEIGHT = display_height
        self.depth = depth
        self.angle_depth = angle_depth
        if custom_font_path:
            self.font = pygame.font.Font(custom_font_path, self.font_size)
        else:
            self.font = pygame.font.SysFont(self.font_name, self.font_size, self.bold)
        # self.font = pygame.font.SysFont(self.font_name, self.font_size, self.bold)
        self.surface = self.font.render(self.text, self.smooth, self.color, self.background)
        self.size = self.surface.get_size()
        self.button_clicked = False
        if size is not None:
            self.size = size
            self.surface = pygame.Surface(self.size)

    def update(self, display):
        self.color = list(self.color)
        if self.depth != 1:
            for i in range(self.depth):
                color = (255 - i * 10, 255 - i * 10, 255 - i * 10)
                font = pygame.font.SysFont(self.font_name, self.font_size, self.bold)
                surface = self.font.render(self.text, self.smooth, color, self.background)
                display.blit(surface, [self.position[0] + math.sin(deg_to_rad(self.angle_depth) * i),
                                       self.position[1] + math.cos(deg_to_rad(self.angle_depth)) * i])
        else:
            display.blit(self.surface, self.position)

    def change_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, self.smooth, self.color, self.background)
        self.size = self.surface.get_size()

    def clicked(self, mouse, mousePos):
        if touched(self.position[0], self.size[0], mousePos[0], 1,
                   self.position[1], self.size[1], mousePos[1], 1):
            if mouse[0]:
                self.button_clicked = True
            else:
                self.button_clicked = False
        else:
            self.button_clicked = False
        return self.button_clicked

    def create_pos(self, y):
        self.position = [(self.WIDTH - self.size[0]) / 2, y]


class Entry:
    def __init__(self, position=[0, 0], font_name='Courier', font_size=20, bold=True, smooth=True,
                 color=(150, 150, 150), text='', background=None, length=10, max_value=255, selected=False):
        self.position = position
        self.font_name = font_name
        self.font_size = font_size
        self.bold = bold
        self.smooth = smooth
        self.color = color
        self.text = text
        self.background = background
        self.length = length
        self.max_value = max_value
        self.font = pygame.font.SysFont(self.font_name, self.font_size, self.bold)
        self.surface = self.font.render(self.text, self.smooth, self.color, self.background)
        self.size = [self.length * (self.font_size - 8), self.font_size]
        self.selected = selected

    def enter_key(self, key='', all_keys=False):
        # print(self.__caps_lock, self.__shift)
        if self.selected:
            if key != 'backspace':
                if len(self.text) < self.length:
                    if not all_keys:
                        if key.isdigit():
                            self.text += key
                    else:
                        special_key = pygame.key.get_pressed()
                        print(special_key[pygame.K_LSHIFT])
                        self.text += key
            else:
                self.text = self.text[:-1]

    def update(self, display):
        mousePos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed(3)
        display.blit(self.surface, self.position)
        if touched(self.position[0], self.size[0], mousePos[0], 1,
                   self.position[1], self.size[1], mousePos[1], 1):
            pygame.draw.rect(display, (0, 255, 255),
                             pygame.Rect(self.position, [self.length * (self.font_size - 8), self.font_size]), 1)
            if mouse[0]:
                self.selected = True
        else:
            pygame.draw.rect(display, self.color,
                             pygame.Rect(self.position, [self.length * (self.font_size - 8), self.font_size]), 1)
            if mouse[0]:
                self.selected = False
        if self.selected:
            pygame.draw.rect(display, (0, 255, 255),
                             pygame.Rect(self.position, [self.length * (self.font_size - 8), self.font_size]), 1)

        if self.text:
            if int(self.text) > self.max_value:
                self.text = self.max_value
                self.text = str(self.text)

        self.__init__(self.position, self.font_name, self.font_size, self.bold, self.smooth, self.color, self.text,
                      self.background, self.length, self.max_value, self.selected)


root = tkinter.Tk()
monitorWidth = root.winfo_screenwidth()
monitorHeight = root.winfo_screenheight()
root.destroy()

DISPLAY = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)
pygame.display.set_caption('Printer App by Egor Mironov @ved3v')
WIDTH, HEIGHT = pygame.display.get_window_size()
CLOCK = pygame.time.Clock()
FPS = 60
RUN = True
MODE = 'selecting image'

COLOR_KEY = None
INVERT = False

end_image = None

select_image_button = Button(WIDTH, HEIGHT, color=(50, 50, 50), font_name='Courier', bold=True, text='Upload Image')
select_image_button.create_pos((HEIGHT - select_image_button.size[1] - 50) / 2)
select_image_image_button = Button(WIDTH, HEIGHT, text='     ')
select_image_image_button.surface.blit(pygame.image.load('download.png').convert_alpha(), (0, 0))
select_image_image_button.surface.set_colorkey((75, 75, 75))
select_image_image_button.size = select_image_image_button.surface.get_size()
select_image_image_button.create_pos((HEIGHT - select_image_image_button.size[1] + 50) / 2)

image_settings_label = Button(WIDTH, HEIGHT, color=(50, 50, 50), font_name='Courier', bold=True, text='Image Settings')
image_settings_label.create_pos(10)
uploaded_label = Button(WIDTH, HEIGHT, color=(50, 50, 50), font_name='Courier', bold=True, text='Uploaded:', font_size=25)
will_be_printed_label = Button(WIDTH, HEIGHT, color=(50, 50, 50), font_name='Courier', bold=True, text='Will be printed:', font_size=25)

invert_colors_button = Button(WIDTH, HEIGHT, color=(50, 50, 50), font_name='Courier', bold=True, text='Invert colors')
print_button = Button(WIDTH, HEIGHT, color=(50, 50, 50), font_name='Courier', bold=True, text='Print Image           ', font_size=40)
invert_colors_button.position = [(WIDTH - (invert_colors_button.size[0] + print_button.size[0])) / 2, (HEIGHT - invert_colors_button.size[1]) / 2]
print_button.position = [(WIDTH - (invert_colors_button.size[0] - print_button.size[0])) / 2, (HEIGHT - invert_colors_button.size[1]) / 2]

while RUN:
    DISPLAY.fill((90, 90, 90))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
    mouse_buttons = pygame.mouse.get_pressed(3)
    mouse_position = pygame.mouse.get_pos()

    if MODE == 'selecting image':
        pygame.draw.rect(DISPLAY, (75, 75, 75),
                         pygame.Rect([select_image_button.position[0] - 20, select_image_button.position[1] - 20], [select_image_button.size[0] + 40, select_image_button.size[1] + 40 + 50]))
        select_image_button.change_text(select_image_button.text)
        select_image_button.update(DISPLAY)
        select_image_image_button.update(DISPLAY)
        if select_image_button.clicked(mouse_buttons, mouse_position):
            root = tkinter.Tk()
            root.withdraw()
            try:
                opened_file_path = tkinter.filedialog.askopenfilename()
                start_image = pygame.image.load(opened_file_path)
                img_width, img_height = start_image.get_size()
                max_size = max(img_width, img_height)
                min_size = min(img_width, img_height)
                size_difference = max_size / min_size
                if img_width == img_height:
                    start_image = pygame.transform.scale(start_image, [100, 100])
                else:
                    if True:
                        start_image = pygame.transform.scale(start_image, [100, int(100 / size_difference)])
                    if max_size == img_height:
                        start_image = pygame.transform.scale(start_image, [int(100 / size_difference), 100])
                end_image = pygame.Surface(start_image.get_size())
                end_image.fill((255, 255, 255))
                black_white_list = []
                for y in range(start_image.get_size()[1]):
                    for x in range(start_image.get_size()[0]):
                        start_color = start_image.get_at((x, y))
                        c = (start_color[0] + start_color[1] + start_color[2]) / 3
                        black_white_list.append(c)
                min_color, max_color = min(black_white_list), max(black_white_list)
                for y in range(start_image.get_size()[1]):
                    for x in range(start_image.get_size()[0]):
                        start_color = start_image.get_at((x, y))
                        c = (start_color[0] + start_color[1] + start_color[2]) / 3
                        if c > (min_color + ((max_color - min_color) / 2)):
                            c = 0
                        else:
                            c = 255
                        pygame.draw.rect(end_image, (c, c, c), pygame.Rect((x, y), [1, 1]))
                uploaded_label.position = [10, HEIGHT - start_image.get_size()[1] - uploaded_label.size[1] - 10]
                will_be_printed_label.position = [WIDTH - will_be_printed_label.size[0] - 10, HEIGHT - start_image.get_size()[1] - will_be_printed_label.size[1] - 10]
                MODE = 'image settings'
            except ValueError:
                pass
            except pygame.error:
                pass
            select_image_button.button_clicked = False
            root.destroy()

    if MODE == 'image settings':
        DISPLAY.blit(start_image, [10, HEIGHT - start_image.get_size()[1]])
        DISPLAY.blit(end_image, [WIDTH - end_image.get_size()[0] - 10, HEIGHT - start_image.get_size()[1]])
        image_settings_label.update(DISPLAY)
        uploaded_label.update(DISPLAY)
        will_be_printed_label.update(DISPLAY)

        invert_colors_button.update(DISPLAY)
        if invert_colors_button.clicked(mouse_buttons, mouse_position):
            invert_colors_button.color = (0, 255, 255)
            if not INVERT:
                INVERT = True
            else:
                INVERT = False
            if INVERT:
                for y in range(start_image.get_size()[1]):
                    for x in range(start_image.get_size()[0]):
                        start_color = start_image.get_at((x, y))
                        c = (start_color[0] + start_color[1] + start_color[2]) / 3
                        if c > (min_color + ((max_color - min_color) / 2)):
                            c = 255
                        else:
                            c = 0
                        pygame.draw.rect(end_image, (c, c, c), pygame.Rect((x, y), [1, 1]))
            else:
                for y in range(start_image.get_size()[1]):
                    for x in range(start_image.get_size()[0]):
                        start_color = start_image.get_at((x, y))
                        c = (start_color[0] + start_color[1] + start_color[2]) / 3
                        if c > (min_color + ((max_color - min_color) / 2)):
                            c = 0
                        else:
                            c = 255
                        pygame.draw.rect(end_image, (c, c, c), pygame.Rect((x, y), [1, 1]))
            pygame.time.wait(500)
        else:
            invert_colors_button.color = (50, 50, 50)
        invert_colors_button.change_text(invert_colors_button.text)

        if not INVERT:
            pygame.draw.rect(DISPLAY, (0, 0, 0), pygame.Rect(((WIDTH - 300) / 2, 100), (100, 100)))
            pygame.draw.rect(DISPLAY, (255, 255, 255), pygame.Rect(((WIDTH + 100) / 2, 100), (100, 100)))
        else:
            pygame.draw.rect(DISPLAY, (255, 255, 255), pygame.Rect(((WIDTH - 300) / 2, 100), (100, 100)))
            pygame.draw.rect(DISPLAY, (0, 0, 0), pygame.Rect(((WIDTH + 100) / 2, 100), (100, 100)))

        print_button.update(DISPLAY)
        if print_button.clicked(mouse_buttons, mouse_position):
            robot_list = []
            if not INVERT:
                for y in range(start_image.get_size()[1]):
                    robot_list.append([])
                    for x in range(start_image.get_size()[0]):
                        start_color = start_image.get_at((x, y))
                        c = (start_color[0] + start_color[1] + start_color[2]) / 3
                        if c > (min_color + ((max_color - min_color) / 2)):
                            c = 0
                        else:
                            c = 255
                        robot_list[y].append(c)
            else:
                for y in range(start_image.get_size()[1]):
                    robot_list.append([])
                    for x in range(start_image.get_size()[0]):
                        start_color = start_image.get_at((x, y))
                        c = (start_color[0] + start_color[1] + start_color[2]) / 3
                        if c > (min_color + ((max_color - min_color) / 2)):
                            c = 255
                        else:
                            c = 0
                        robot_list[y].append(c)
            # os.system('code C:/Users/Egor/Desktop/ev3_python/printer/')
            l = ''
            for y in range(len(robot_list)):
                for x in range(len(robot_list[y])):
                    l += str(robot_list[y][x]) + ' '
                l += '\n'
            print(l)
            file = open('C:/Users/Egor/Desktop/ev3_python/printer/some_text.txt', 'w')
            file.write(l)
            file.close()

    pygame.display.update()
    CLOCK.tick(FPS)
