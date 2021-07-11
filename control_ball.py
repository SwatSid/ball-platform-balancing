import pygame, sys, time, random
from pygame.locals import *
from time import *

pygame.init()
windowSurface = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption("Bounce")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

info = pygame.display.Info()
sw = info.current_w
sh = info.current_h
y= 0
yy= sh

while True:
    windowSurface.fill(BLACK)
    pygame.draw.circle(windowSurface, GREEN , (250,y), 13, 0)
    sleep(.006)
    y+= 1
    if y>sh:
        pygame.draw.circle(windowSurface, GREEN , (250,yy), 13, 0)
        sleep(.0001)
        yy +=-1
    if yy<-.00001:
        y=0
        y+= 1
        pygame.draw.circle(windowSurface, GREEN , (250,y), 13, 0)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
