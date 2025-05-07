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
#DIMENSIONS
screenWidth = maze.width + 200
screenHeight = maze.width + 70
screen = pygame.display.set_mode((screenWidth, screenHeight))
font=pygame.font.Font('freesansbold.ttf',20)
#BUTTONS
generateMazeDFS=Button(screen,maze.width+5,10,"Generate Maze: DFS")
solveBFS=Button(screen,maze.width+5,45,"Solve Maze: BFS")
reset=Button(screen,maze.width+5,80,"Reset Maze")
solveAstar=Button(screen,maze.width+5,115,"Solve Maze: A star")
solveDFS=Button(screen,maze.width+5,150,"Solve Maze: DFS")
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


dfs = maze.DFS()
bfs = None
phase = ""
dfs_done = False
bfs_done = False
won=False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if user clicks on the X
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if generateMazeDFS.isClicked():
                maze.resetMaze() #resets maze to original gird
                dfs = maze.DFS() #calls the function and "yield" stops when a wall gets removed
                dfs_done = False #since we are starting a new dfs maze, set dfs_done to false, this ensures that player cant move yet and that bfs wont run yet
                character.reset() #return character to start position
                won = False #set won to false since we are JUST starting a new maze
                phase = "dfs" #set phase to dfs, since we are currently generating

            elif solveBFS.isClicked() and dfs_done : #if user wants to solve with BFS AND the dfs generation is done a\
                bfs = maze.BFS() #calls the method for the first time and yield causes it to return once a link is created between two cells
                phase = "bfs"

            elif reset.isClicked():
                phase = "reset"



    keys = pygame.key.get_pressed() #returns a list of keys with t or f for each key indicating if it is pressed rn

    if not won and dfs_done: #character can move ONLY when dfs is done and when they did not win yet
        character.characterMovement(keys, maze) #this method processes movement of character
        won=character.mazeSolved(maze) #as player keeps moving, keep checking whether they won yet, if they did the condition will break, they wint be able to move.

    if phase == "dfs": #this is true when you click the generateMazeDFS button
        try:
            next(dfs) #runs the next iteration of DFS generator method till a wall is removed then returns (when it returns it runs through the rest of the code and renders this on the screen then goes through the condition again, removed next wall, and so on till the stack is empty and method/generator  stops)
        except StopIteration: #if the stack is empty, the DFS generation method ended
            dfs_done = True #dfs_done is true now, now the player can move
            phase = ""  # set phase to idle which just waits for controls

    elif phase == "bfs" : #same as dfs generator
        try:
            next(bfs)
        except StopIteration:
            phase = "bfs_done"
    elif phase=="reset":
        maze.resetMaze()
        dfs = maze.DFS()
        bfs = None
        dfs_done = False
        character.reset()
        won = False
        phase = ""

    screen.fill("grey")  # Clear screen
    #drawing buttons
    generateMazeDFS.drawButton(screen)
    solveBFS.drawButton(screen)
    reset.drawButton(screen)
    solveAstar.drawButton(screen)
    solveDFS.drawButton(screen)
    #draw grid
    drawGrid()
    if won:
        # if the user won, draw win msg
        screen.blit(win_msg,(screenWidth/2-50,maze.width+20) )
   # if phase in ("bfs", "bfs_done"):
    drawGridPath()
    #draw character
    character.animate(screen)


    #updates screen each frame
    pygame.display.update()
    clock.tick(20)
pygame.quit()
