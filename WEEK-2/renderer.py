import pygame
from constants import *
import numpy as np
def draw_grid(screen,game):
    colors=np.zeros((ROWS,COLS,3),dtype=int)
    colors[game.grid == 1] = RED
    colors[game.grid == 2] = BLUE
    colors[game.grid == -1] = FADERED
    colors[game.grid == -2] = FADEBLUE
    surface=pygame.Surface((COLS,ROWS))
    pygame.surfarray.blit_array(surface,colors.swapaxes(0,1))
    surface=pygame.transform.scale(surface,(WIDTH,HEIGHT))
    screen.blit(surface,(0,0))

def draw_player(screen, player):
    x=player.pos[1]*CELL_SIZE + CELL_SIZE//2
    y=player.pos[0]*CELL_SIZE + CELL_SIZE//2
    pygame.draw.circle(screen,player.color,(x,y),CELL_SIZE//2)

