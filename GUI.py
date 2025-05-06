import random

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
#maze.DFS()
#maze.resetMaze()
def drawGridPath():
    pygame.draw.line(screen,"red",(length/2,0),(length/2,length/2))
    for y in range(size):
        for x in range (size):
            drawLink(maze.grid[x][y])
def drawLink(cell):
    x=cell.x
    y=cell.y
    centerX=x*length+length/2
    centerY=y*length+length/2
    if cell.links["left"]: pygame.draw.line(screen,"red",(centerX,centerY),(centerX-length,centerY))
    if cell.links["right"]: pygame.draw.line(screen,"red",(centerX,centerY),(centerX+length,centerY))
    if cell.links["top"]: pygame.draw.line(screen,"red",(centerX,centerY),(centerX,centerY-length))
    if cell.links["bottom"]: pygame.draw.line(screen,"red",(centerX,centerY),(centerX,centerY+length))

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
bfs = None
phase = "dfs"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("grey")
    if phase == "dfs":
        try:
            next(dfs)
        except StopIteration:
            bfs = maze.BFS()
            phase = "bfs"
    elif phase == "bfs":
        try:
            next(bfs)
        except StopIteration:
            phase = "done"

    drawGrid()
    if phase in ("bfs", "done"):
        drawGridPath()
    pygame.display.flip()
    clock.tick(60)  # control the animation speed (FPS)

pygame.quit()