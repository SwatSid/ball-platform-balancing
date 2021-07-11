import pygame, sys, time, random
from pygame.locals import *
from time import *

pygame.init()
windowSurface = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption("Bounce")

BLACK = (0, 0, 0)
WHITE = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

info = pygame.display.Info()
sw = info.current_w
sh = info.current_h

radius = 10
velocity = 0
acceleration = 9.8
y= radius
down_direction_flag = True
del_t = 0.005

def simulate_physics(position, velocity, acceleration, delta_time):

    position = position + (velocity * delta_time) + (acceleration * delta_time**2)/2
    velocity = velocity + (acceleration * delta_time)
    return position, velocity

windowSurface.fill(WHITE)
win_orig = windowSurface

while True:
    windowSurface = win_orig
    pygame.draw.circle(windowSurface, BLACK , (250,y), radius, 0)

    y, velocity = simulate_physics(y, velocity, acceleration, del_t)
    
    if (y > sh - radius) or (y < radius):
        velocity = - velocity

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
