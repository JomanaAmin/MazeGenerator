import pygame
from pygame import Rect

from MazeGenerator import MazeGenerator
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
length=10
maze=MazeGenerator(8)
def drawCells():
    for cell in maze.grid:
        


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    # RENDER YOUR GAME HERE
  """  for y in range(8):
        yCoord=y*10
        for x in range(8):
            xCoord=x*10
            pygame.draw.rect(screen, "white", Rect(x,y,length,length))
    for cell in maze.grid:
        pygame.draw.rect(screen, "white", Rect(cell.x*10, y*10, length, length))
"""
    pygame.display.flip()

    clock.tick(60)

pygame.quit()