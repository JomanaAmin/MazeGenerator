import random

import pygame
from pygame import Rect

from MazeGenerator import MazeGenerator
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
length=20
size=35
maze=MazeGenerator(size)
#maze.DFS()
#maze.resetMaze()
def drawGrid():
    for y in range(size):
        for x in range (size):
            drawCell(maze.grid[x][y])
def drawCell(cell):
    x=cell.x
    y=cell.y
    if cell.walls["top"]:
        pygame.draw.line(screen, (255,255,255), (x*length, y*length), ((x+1)*length, y*length))
    if cell.walls["bottom"]:
        pygame.draw.line(screen, (255,255,255), (x*length, (y+1) *length), ((x+1)*length, (y+1)*length))

    if cell.walls["left"]:
        pygame.draw.line(screen, (255,255,255), (x*length, y*length), (x*length, (y+1)*length))

    if cell.walls["right"]:
        pygame.draw.line(screen, (255,255,255), ((x+1)*length, y*length), ((x+1)*length, (y+1)*length))


def generateNewMaze(maze):

    maze.resetMaze()
    maze.DFS()


maze.resetMaze()
dfs = maze.DFS()

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("grey")

    try:
        next(dfs)  # advance one DFS step per frame
    except StopIteration:
        pass  # DFS finished

    drawGrid()
    pygame.display.flip()
    clock.tick(60)  # control the animation speed (FPS)

pygame.quit()