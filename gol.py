#Imports
import pygame, sys
from pygame.locals import *
import random, time
from collections import Counter
 
#Initializing 
pygame.init()
 
zoom = 10
pan_x, pan_y = 0, 0

BORN = [3]
SURVIVE = [2, 3]

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
  
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Conway's Game of Life")
 
#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

def resetPosition():
    global pan_x, pan_y
    w, h = pygame.display.get_surface().get_size()
    pan_x, pan_y = (w//2) // zoom, (h//2) // zoom

class golBoard():
    def __init__(self):
        self.all_items = set()
        
    def draw(self):
        DISPLAYSURF.fill(WHITE if isPaused else BLACK)
        for i in self.all_items:
            pygame.draw.rect(DISPLAYSURF, BLACK if isPaused else WHITE, pygame.Rect(((i[0] + pan_x) * zoom, (i[1] + pan_y) * zoom), (zoom,zoom)))

    def update(self):
        stat = Counter()
        for i in self.all_items:
            for x in range(i[0]-1, i[0]+2):
                for y in range(i[1]-1, i[1]+2):
                    if not (x == i[0] and y == i[1]):
                        stat[(x, y)] += 1
        nm = set()
        for i in stat:
            if stat[i] in SURVIVE and i in self.all_items:
                nm.add(i)
            elif stat[i] in BORN:
                nm.add(i)
        self.all_items = nm
            
    def addItem(self, pos):
        ps = ((pos[0] // zoom) - pan_x, (pos[1] // zoom) - pan_y)
        self.all_items.add(ps)
        pygame.draw.rect(DISPLAYSURF, BLACK if isPaused else WHITE, pygame.Rect(((ps[0] + pan_x) * zoom, (ps[1] + pan_y) * zoom), (zoom,zoom)))

    def removeItem(self, pos):
        ps = ((pos[0] // zoom) - pan_x, (pos[1] // zoom) - pan_y)
        self.all_items.discard(ps)
        pygame.draw.rect(DISPLAYSURF, WHITE if isPaused else BLACK, pygame.Rect(((ps[0] + pan_x) * zoom, (ps[1] + pan_y) * zoom), (zoom,zoom)))

    
    def clear(self):
        self.all_items = set()

isPaused = True
gb = golBoard()

pygame.key.set_repeat()
resetPosition()
frame_number, frames_per_update = 0, 1

#Game Loop
while True:
    frame_number += 1
    #Cycles through all events occurring  
    for event in pygame.event.get():     
        if event.type == pygame.KEYDOWN:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_SPACE]:
                isPaused = not isPaused      
            if pressed_keys[K_DOWN]:
                zoom = max(zoom // 2, 1)
            if pressed_keys[K_UP]:
                zoom += zoom
            if pressed_keys[K_RIGHT]:
                frames_per_update -= 1
                frames_per_update = max(frames_per_update, 1)
            if pressed_keys[K_LEFT]:
                frames_per_update += 1  
                frames_per_update = min(FPS, frames_per_update)                              
            if pressed_keys[K_d]:
                pan_x -= 100 // zoom
            if pressed_keys[K_a]:
                pan_x += 100 // zoom
            if pressed_keys[K_w]:
                pan_y += 100 // zoom
            if pressed_keys[K_s]:
                pan_y -= 100 // zoom
            if pressed_keys[K_q]:
                resetPosition()
            if pressed_keys[K_c]:
                gb.clear()
            gb.draw()   
            
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if not isPaused:
        gb.draw() 
        if frame_number >= frames_per_update:
            gb.update()   
            frame_number = 0
        FramePerSec.tick(FPS)

    if pygame.mouse.get_pressed()[0]:
        gb.addItem(pygame.mouse.get_pos())
    if pygame.mouse.get_pressed()[2]:
        gb.removeItem(pygame.mouse.get_pos())

    pygame.display.update()
