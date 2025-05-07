import random
import pygame
from pygame import Rect, key
from Character import Character
from Button import Button

from MazeGenerator import MazeGenerator
pygame.init()
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()
running = True


length=25
size=10

maze=MazeGenerator(size,length)
character=Character(maze,0,0)
screenWidth = maze.width + 200
screenHeight = maze.width + 70
screen = pygame.display.set_mode((screenWidth, screenHeight))

#DIMENSIONS

screenWidth=maze.width+200
screenHeight=maze.width+70
screen = pygame.display.set_mode((screenWidth, screenHeight))


font=pygame.font.Font('freesansbold.ttf',20)

#text=font.render("Welcome to our maze game!", True, (0,0,0))


#BUTTONS
generateMazeDFS=Button(screen,maze.width+5,10,"Generate Maze: DFS")
solveBFS=Button(screen,maze.width+5,45,"Solve Maze: BFS")
reset=Button(screen,maze.width+5,80,"Reset Maze")
solveAstar=Button(screen,maze.width+5,115,"Solve Maze: A star")
#MESSAGES
win_msg = font.render("You Won!", True, "Black")


def drawGridPath():
    pygame.draw.line(screen,"red",(length/2,0),(length/2,length/2), 5)
    for y in range(size):
        for x in range (size):
            drawLink(maze.grid[x][y])
def drawLink(cell):
    x=cell.x
    y=cell.y
    centerX=x*length+length/2
    centerY=y*length+length/2
    if cell.links["left"]: pygame.draw.line(screen,"red",(centerX,centerY),(centerX-length,centerY),5)
    if cell.links["right"]: pygame.draw.line(screen,"red",(centerX,centerY),(centerX+length,centerY),5)
    if cell.links["top"]: pygame.draw.line(screen,"red",(centerX,centerY),(centerX,centerY-length),5)
    if cell.links["bottom"]: pygame.draw.line(screen,"red",(centerX,centerY),(centerX,centerY+length),5)

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
phase = ""
dfs_done = False
bfs = None
bfs_triggered = False
won=character.mazeSolved(maze)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if generateMazeDFS.isClicked():
                maze.resetMaze()
                dfs = maze.DFS()
                dfs_done = False
                bfs_triggered = False
                character = Character(maze, 0, 0)
                won = False
                phase = "dfs"
            elif solveBFS.isClicked() and dfs_done and not bfs_triggered:
                bfs = maze.BFS()
                bfs_triggered = True
                phase = "bfs"

            elif reset.isClicked():
                phase = "reset"



    keys = pygame.key.get_pressed()
    # Allow character movement only after DFS is done
    if not won and dfs_done:

        character.characterMovement(keys, maze)
        won=character.mazeSolved(maze)

    if phase == "dfs":
        try:
            next(dfs)
        except StopIteration:
            dfs_done = True
            phase = "idle"  # Wait for button press
    elif phase == "bfs" and bfs is not None:
        try:
            next(bfs)
        except StopIteration:
            phase = "done"
    elif phase=="reset":
        maze.resetMaze()
        dfs = maze.DFS()
        bfs = None
        dfs_done = False
        bfs_triggered = False
        character = Character(maze, 0, 0)
        won = False
        phase = ""

    screen.fill("grey")  # Clear screen
    #drawing buttons
    generateMazeDFS.drawButton(screen)
    solveBFS.drawButton(screen)
    reset.drawButton(screen)
    solveAstar.drawButton(screen)

    #draw grid
    drawGrid()

    if phase in ("bfs", "done"):
        drawGridPath()
    #draw character
    character.animate(screen)

    if won:
        # if the user won, draw win msg
        screen.blit(win_msg,(screenWidth/2-50,maze.width+20) )
    #updates screen each frame
    pygame.display.update()
    clock.tick(27)
pygame.quit()
