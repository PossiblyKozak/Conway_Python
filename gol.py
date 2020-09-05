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

shapes = {"Single": [(0, 0)]}

def resetPosition():
    w, h = pygame.display.get_surface().get_size()
    settings.pan_x, settings.pan_y = (w//2) // settings.zoom, (h//2) // settings.zoom

def change_index(change, curr_index, max_index):
    res = curr_index + change
    if res > max_index: 
        res = 0
    elif res < 0: 
        res = max_index
    return res

if __name__ == "__main__":
    settings.isPaused = True
    gb = golBoard(BORN, SURVIVE)

    pygame.key.set_repeat()
    resetPosition()
    frame_number, frames_per_update = 0, 1

    for i in os.listdir("shapes"):
        f = open("shapes/%s" % i, 'r').readlines()
        shape = []
        for index_x in range(len(f)):
            for index_y in range(len(f[index_x])):
                if f[index_x][index_y] == 'O':
                    shape.append((index_x, index_y))
        shapes[i.split('.')[0]] = shape
    shape_list = list(shapes.keys())
    shape_index = 0

    xy = pygame.display.get_surface().get_size()
    font = pygame.font.Font('fonts/eight-bit-dragon.otf', 50) 
    
    text = font.render(shape_list[shape_index], True, golColours.BLACK) 
    textRect = text.get_rect()  
    textRect.center = (xy[0]//2, xy[1]-50) 

    #Game Loop
    while True:
        frame_number += 1
        #Cycles through all events occurring  
        for event in pygame.event.get():     
            if event.type == KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_SPACE]:
                    settings.isPaused = not settings.isPaused
                    text = font.render(shape_list[shape_index], True, golColours.BLACK if settings.isPaused else golColours.WHITE) 
                    textRect = text.get_rect()
                    textRect.center = (xy[0]//2, xy[1]-50)                    
                elif pressed_keys[K_DOWN]:
                    settings.zoom = max(settings.zoom // 2, 1)
                elif pressed_keys[K_UP]:
                    settings.zoom = min(settings.zoom * 2, 100)
                elif pressed_keys[K_RIGHT]:
                    frames_per_update -= 1
                    frames_per_update = max(frames_per_update, 1)
                elif pressed_keys[K_LEFT]:
                    frames_per_update += 1  
                    frames_per_update = min(FPS, frames_per_update)                              
                elif pressed_keys[K_d]:
                    settings.pan_x -= 100 // settings.zoom
                elif pressed_keys[K_a]:
                    settings.pan_x += 100 // settings.zoom
                elif pressed_keys[K_w]:
                    settings.pan_y += 100 // settings.zoom
                elif pressed_keys[K_s]:
                    settings.pan_y -= 100 // settings.zoom
                elif pressed_keys[K_q]:
                    resetPosition()
                elif pressed_keys[K_c]:
                    gb.clear()
                gb.draw(DISPLAYSURF, settings)   
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4 or event.button == 5:
                    shape_index = change_index((event.button * 2) - 9, shape_index, len(shape_list) - 1)
                    text = font.render(shape_list[shape_index], True, golColours.BLACK if settings.isPaused else golColours.WHITE) 
                    textRect = text.get_rect()
                    textRect.center = (xy[0]//2, xy[1]-50)
                

        if not settings.isPaused:
            gb.draw(DISPLAYSURF, settings) 
            if frame_number >= frames_per_update:
                gb.update()   
                frame_number = 0
            FramePerSec.tick(FPS)
        
        x = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            gb.addItem(x, settings, DISPLAYSURF, shapes[shape_list[shape_index]])
        elif pygame.mouse.get_pressed()[2]:
            gb.removeItem(x, settings, DISPLAYSURF)
        game_surf.fill(Color(0,0,0,0))
        gb.drawTemp(x, settings, game_surf, shapes[shape_list[shape_index]])
    
        main_window.blit(DISPLAYSURF, (0, 0))
        main_window.blit(game_surf, (0, 0))
        main_window.blit(text, textRect)
        pygame.display.update()
