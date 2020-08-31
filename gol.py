#Imports
import pygame, sys, os, golColours, golConfig
from pygame.locals import *
import random, time
from collections import Counter
from golBoard import golBoard
 
#Initializing 
pygame.init()

settings = golConfig.config(zoom=10, pan_x=0, pan_y=0, isPaused=True)

BORN = [3]
SURVIVE = [2, 3]

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
  
#Create a white screen 
main_window = pygame.display.set_mode((0, 0), FULLSCREEN)
DISPLAYSURF = pygame.Surface(pygame.display.get_surface().get_size())
DISPLAYSURF.fill(golColours.WHITE)
pygame.display.set_caption("Conway's Game of Life")
 
game_surf = pygame.Surface(pygame.display.get_surface().get_size(), flags=SRCALPHA)

def resetPosition():
    w, h = pygame.display.get_surface().get_size()
    settings.pan_x, settings.pan_y = (w//2) // settings.zoom, (h//2) // settings.zoom

if __name__ == "__main__":
    settings.isPaused = True
    gb = golBoard(BORN, SURVIVE)

    pygame.key.set_repeat()
    resetPosition()
    frame_number, frames_per_update = 0, 1

    #Game Loop
    while True:
        frame_number += 1
        #Cycles through all events occurring  
        for event in pygame.event.get():     
            if event.type == KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_SPACE]:
                    settings.isPaused = not settings.isPaused      
                if pressed_keys[K_DOWN]:
                    settings.zoom = max(settings.zoom // 2, 1)
                if pressed_keys[K_UP]:
                    settings.zoom = min(settings.zoom * 2, 100)
                if pressed_keys[K_RIGHT]:
                    frames_per_update -= 1
                    frames_per_update = max(frames_per_update, 1)
                if pressed_keys[K_LEFT]:
                    frames_per_update += 1  
                    frames_per_update = min(FPS, frames_per_update)                              
                if pressed_keys[K_d]:
                    settings.pan_x -= 100 // settings.zoom
                if pressed_keys[K_a]:
                    settings.pan_x += 100 // settings.zoom
                if pressed_keys[K_w]:
                    settings.pan_y += 100 // settings.zoom
                if pressed_keys[K_s]:
                    settings.pan_y -= 100 // settings.zoom
                if pressed_keys[K_q]:
                    resetPosition()
                if pressed_keys[K_c]:
                    gb.clear()
                gb.draw(DISPLAYSURF, settings)   
                
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if not settings.isPaused:
            gb.draw(DISPLAYSURF, settings) 
            if frame_number >= frames_per_update:
                gb.update()   
                frame_number = 0
            FramePerSec.tick(FPS)
        
        x = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            gb.addItem(x, settings, DISPLAYSURF)
        elif pygame.mouse.get_pressed()[2]:
            gb.removeItem(x, settings, DISPLAYSURF)
        game_surf.fill(Color(0,0,0,0))
        gb.drawTemp(x, settings, game_surf)

        main_window.blit(DISPLAYSURF, (0, 0))
        main_window.blit(game_surf, (0, 0))
        pygame.display.update()
