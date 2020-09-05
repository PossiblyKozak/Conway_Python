import time, golColours, pygame, sys
from collections import Counter

def onBoard(r, w, h, settings):
    return (r[0] < w and r[0] + settings.zoom > - settings.pan_x) and (r[1] < h and r[1] + settings.zoom > - settings.pan_y)

def mouseToPZ(pos, settings):
    return ((pos[0] // settings.zoom) - settings.pan_x, (pos[1] // settings.zoom) - settings.pan_y)

def pzToRect(ps, settings):
    return pygame.Rect(((ps[0] + settings.pan_x) * settings.zoom, (ps[1] + settings.pan_y) * settings.zoom), (settings.zoom, settings.zoom))

class golBoard():
    def __init__(self, born, survive):
        self.BORN = born
        self.SURVIVE = survive
        self.all_items = set()
        
    def draw(self, DISPLAYSURF, settings):
        #before = time.time()
        DISPLAYSURF.fill(golColours.WHITE if settings.isPaused else golColours.BLACK)
        w, h = mouseToPZ(pygame.display.get_surface().get_size(), settings)
        tt = 0
        for i in self.all_items:
            if onBoard(i, w, h, settings):
                tt += 1
                pygame.draw.rect(DISPLAYSURF, golColours.BLACK if settings.isPaused else golColours.WHITE, pzToRect(i, settings))
        #print("DRAW: %f seconds (%d/%d items)" % (time.time() - before, tt, len(self.all_items)))

    def update(self):
        #before = time.time()
        stat = Counter()
        for i in self.all_items:
            for x in range(i[0]-1, i[0]+2):
                for y in range(i[1]-1, i[1]+2):
                    if not (x == i[0] and y == i[1]):
                        stat[(x, y)] += 1
        nm = set()
        for i in stat:
            if stat[i] in self.SURVIVE and i in self.all_items:
                nm.add(i)
            elif stat[i] in self.BORN:
                nm.add(i)
        self.all_items = nm
        #print("UPDATE: %f seconds (size: %d)" % (time.time() - before, sys.getsizeof(self.all_items)))
            
    def addItem(self, pos, settings, surface, shape = [(0, 0)], toAdd = True):
        pz = mouseToPZ(pos, settings)
        for coordinate in shape:
            pygame.draw.rect(surface, golColours.BLACK if settings.isPaused else golColours.WHITE, pzToRect((pz[0] + coordinate[0], pz[1] + coordinate[1]), settings))
            if toAdd: 
                self.all_items.add((pz[0] + coordinate[0], pz[1] + coordinate[1]))

    def drawTemp(self, pos, settings, surface, shape = [(0, 0)]):
        pz = mouseToPZ(pos, settings)
        for coordinate in shape:
            pygame.draw.rect(surface, golColours.RED, pzToRect((pz[0] + coordinate[0], pz[1] + coordinate[1]), settings))

    def removeItem(self, pos, settings, surface):
        pz = mouseToPZ(pos, settings)
        self.all_items.discard(pz)
        pygame.draw.rect(surface, golColours.WHITE if settings.isPaused else golColours.BLACK, pzToRect(pz, settings))

    
    def clear(self):
        self.all_items = set()