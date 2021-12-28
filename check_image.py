def touched(x1, weight1, x2, weight2, y1, height1, y2, height2):
    if (x1 <= x2 and x2 <= (x1 + weight1)
        and y1 <= y2 and y2 <= (y1 + height1)) \
            or (x1 <= (x2 + weight2) and (x1 + weight1) >= x2
                and y1 <= (y2 + height2) and (y1 + height1) >= y2):
        return True
    else:
        return False

a = open('C:/Users/Egor/Desktop/ev3_python/printer/some_text.txt', 'r')
opened_file = a.read()
a.close()
l = opened_file.split('\n')
robot_list = []
for y in range(len(l)):
    l1 = l[y].split(' ')
    l1.pop(-1)
    robot_list.append(l1)
robot_list.pop(-1)
for y in range(len(robot_list)):
    for x in range(len(robot_list[y])):
        robot_list[y][x] = int(robot_list[y][x])

print(*robot_list, sep='\n')

import pygame

pygame.init()

DISPLAY = pygame.display.set_mode((600, 600))
WIDTH, HEIGHT = DISPLAY.get_size()
RUN = True
CLOCK = pygame.time.Clock()
FPS = 60
for y in range(len(robot_list)):
    for x in range(len(robot_list[y])):
        pygame.draw.rect(DISPLAY, (robot_list[y][x], robot_list[y][x], robot_list[y][x]), pygame.Rect([x * 6, y * 6], [6, 6]))

while RUN:
    pygame.display.set_caption(str(int(CLOCK.get_fps())))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    pygame.display.update()
    CLOCK.tick(FPS)
