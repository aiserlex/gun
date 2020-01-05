import sys
import copy
import time
import pygame
import random
import string
import numpy as np

# size of one cell in pixels
CSIZE = (20, 20)

# number of cells along x and y axis
NSIZE = (55, 40)



def numNeib(area, x, y):
    """ count all neighbours of given cell in area array """
    sum = -area[x, y]  # initialize sum and neutralize one repeated summand
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if x + i < 0 or x + i >= NSIZE[0] or y + j < 0 or y + j >= NSIZE[1]:
                # out of bounds of array
                continue
            sum += area[x + i, y + j]
    return sum


# array of cells (0: dead, 1: alive)
area = np.zeros(NSIZE, dtype=np.int)

# screen size
scrSize = (CSIZE[0]*NSIZE[0], CSIZE[1]*NSIZE[1])

# initialaze pygame
pygame.init()
screen = pygame.display.set_mode(scrSize)
pygame.display.set_caption("Game of Life")

fps = 5
clock = pygame.time.Clock()

one_step = False
is_running = False

while True:    
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button1, *_ = pygame.mouse.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            xdata = mouse_x // CSIZE[0]
            ydata = mouse_y // CSIZE[1]
            if button1:
                area[xdata, ydata] = 1
            else:
                area[xdata, ydata] = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                # manual step-by-step iterations
                one_step = True
                is_running = False
            elif event.key == pygame.K_SPACE:
                # automatic iterations
                is_running = not is_running
            elif event.key == pygame.K_COMMA:
                # decrease speed
                fps = fps / 1.5
            elif event.key == pygame.K_PERIOD:
                # increase speed
                fps = fps * 1.5
            elif event.key == pygame.K_l:
                # load state from file "gun"
                file_name = "gun2"
                with open(file_name, 'r') as f:
                    data = list(map(int, f.read().split()))
                    area = np.zeros(NSIZE, dtype=np.int)
                    for i in range(int(len(data)/2)):
                        try:
                            area[data[2*i], data[2*i+1]] = 1
                        except:
                            pass
            elif event.key == pygame.K_s:
                # save current state in file
                time_from_begin_in_sec = time.time()
                strut_time = time.gmtime(time_from_begin_in_sec)
                file_name = time.strftime("%Y-%m-%d-%H-%M-%S", strut_time)
                with open(file_name, 'w') as f:
                    data = []
                    for i in range(NSIZE[0]):
                        for j in range(NSIZE[1]):
                            if area[i, j] == 1:
                                data.append(str(i))
                                data.append(str(j))
                    strData = " ".join(data)
                    f.write(strData)
                    print("saved in: ", file_name)

    for i in range(NSIZE[0]):
        pygame.draw.line(screen, (0, 0, 0), (i*CSIZE[0], 0), (i*CSIZE[0],
                                                              scrSize[1]))

    for i in range(NSIZE[1]):
        pygame.draw.line(screen, (0, 0, 0), (0, i*CSIZE[1]), (scrSize[0],
                                                              i*CSIZE[1]))
    
    for i in range(NSIZE[0]):
        for j in range(NSIZE[1]):
            if area[i, j] == 1:
                pygame.draw.rect(screen, (0, 0, 0),
                                 pygame.Rect(i*CSIZE[0],
                                             j*CSIZE[1], CSIZE[0], CSIZE[1]))

    if one_step:
        areaCurr = np.zeros(NSIZE, dtype=np.int)
        for i in range(NSIZE[0]):
            for j in range(NSIZE[1]):
                if numNeib(area, i, j) == 3:
                    areaCurr[i, j] = 1
                elif numNeib(area, i, j) == 2:
                    areaCurr[i, j] = area[i, j]
                else:
                    areaCurr[i, j] = 0
    
        area = copy.deepcopy(areaCurr)
        one_step = False
        
    if is_running:
        one_step = True
#        print("fps = ", fps)
        clock.tick(fps)
        
    pygame.display.flip()
