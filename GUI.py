import pygame
from pygame import Rect

from MazeGenerator import MazeGenerator
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
length=20
size=10
maze=MazeGenerator(size)
maze.DFS()
def drawGrid():
    for y in range(size):
        for x in range (size):
            drawCell(maze.grid[x][y])
def drawCell(cell):
    x=cell.x+20
    y=cell.y+15
    if cell.walls["top"]:
        pygame.draw.line(screen, (255,255,255), (x*length, y*length), ((x+1)*length, y*length))
    if cell.walls["bottom"]:
        pygame.draw.line(screen, (255,255,255), (x*length, (y+1) *length), ((x+1)*length, (y+1)*length))

    if cell.walls["left"]:
        pygame.draw.line(screen, (255,255,255), (x*length, y*length), (x*length, (y+1)*length))

    if cell.walls["right"]:
        pygame.draw.line(screen, (255,255,255), ((x+1)*length, y*length), ((x+1)*length, (y+1)*length))



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    # RENDER YOUR GAME HERE
    drawGrid()
    pygame.display.flip()

    clock.tick(60)

pygame.quit()