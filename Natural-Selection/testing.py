import math, pywinauto
import pygame, sys, time
from pygame.constants import K_SPACE, K_ESCAPE, K_w, K_a, K_s, K_d
pygame.init()

size = width, height =  800, 800
# size = width, height = pygame.display.get_window_size()
cycle_time = 0.025

screen = pygame.display.set_mode(size)
# screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)


x, y = 400, 400

while 1:
    now = time.time()
    screen.fill((160, 160, 160))
    keys=pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        quit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mos_x, mos_y = pygame.mouse.get_pos()
            degrees = math.degrees(math.atan2((mos_y-y),(mos_x-x)))
            print(degrees)
    
    pygame.draw.ellipse(screen, (0, 0, 0), pygame.Rect(x-5, y-5, 10, 10))

    
    
    

    
    pygame.display.flip()
    elapsed = time.time()-now
    if elapsed < cycle_time:
        time.sleep(cycle_time-elapsed)