import time

import pygame
from Character import Character
from Button import Button

from Maze import Maze
from timer import Timer
pygame.init()
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()
running = True
length=25
size=10
trials=0
maze=Maze(size,length)
character=Character(maze,length/2,length/2)
#DIMENSIONS
screenWidth = maze.width + 200
screenHeight = maze.width + 70
screen = pygame.display.set_mode((screenWidth, screenHeight))
font = pygame.font.SysFont("timesnewroman", 25,True)  # Font name is case-insensitive

timer=Timer(20,screen,length*2.5,maze.width+length*2)
pygame.time.set_timer(pygame.USEREVENT, 1000)



#BUTTONS
#generateMazeDFS=Button(screen,maze.width+length,10,"Generate Maze: DFS",screenWidth-maze.width-3*length/2)
clearMaze=Button(screen,maze.width+length,185,"Clear Maze",screenWidth-maze.width-3*length/2)
solveBFS=Button(screen,maze.width+length,80,"Solve Maze: BFS",screenWidth-maze.width-3*length/2)
solveGreedy = Button(screen, maze.width +length, 45, "Solve Maze: GBFS",screenWidth-maze.width-3*length/2) ###
reset=Button(screen,maze.width+length,220,"Reset Maze",screenWidth-maze.width-3*length/2)
solveAstar=Button(screen,maze.width+length,150,"Solve Maze: A star",screenWidth-maze.width-3*length/2)
solveDFS=Button(screen,maze.width+length,115,"Solve Maze: DFS",screenWidth-maze.width-3*length/2)
startGame=Button(screen,maze.width+length,10,"Start Game",screenWidth-maze.width-3*length/2)
restartGame=Button(screen,maze.width+length,255,"Restart Game",screenWidth-maze.width-3*length/2)


#MESSAGES
win_msg = font.render("You Won!", True, (130, 112, 129))
time_msg = font.render("Time is UP!", True, (130, 112, 129))

def drawGridPath():
    #pygame.draw.line(screen,"red",(length/2,0),(length/2,length/2), 5)
    for y in range(size):
        for x in range (size):
            drawLink(maze.grid[x][y])

def drawLink(cell):
    x=cell.x
    y=cell.y
    centerX=x*length+length
    centerY=y*length+length
    if cell.links["left"]: pygame.draw.line(screen,(227, 208, 216),(centerX,centerY),(centerX-length,centerY),3)
    if cell.links["right"]: pygame.draw.line(screen,(227, 208, 216),(centerX,centerY),(centerX+length,centerY),3)
    if cell.links["top"]: pygame.draw.line(screen,(227, 208, 216),(centerX,centerY),(centerX,centerY-length),3)
    if cell.links["bottom"]: pygame.draw.line(screen,(227, 208, 216),(centerX,centerY),(centerX,centerY+length),3)

def drawGrid():
    for y in range(size):
        for x in range (size):
            drawCell(maze.grid[x][y])

def drawCell(cell):
    x=cell.x
    y=cell.y
    if cell.walls["top"]:
        pygame.draw.line(screen, (231, 230, 247), (x*length+length/2, y*length+length/2), ((x+1)*length+length/2, y*length+length/2))
    if cell.walls["bottom"]:
        pygame.draw.line(screen, (231, 230, 247), (x*length+length/2, (y+1) *length+length/2), ((x+1)*length+length/2, (y+1)*length+length/2))

    if cell.walls["left"]:
        pygame.draw.line(screen, (231, 230, 247), (x*length+length/2, y*length+length/2), (x*length+length/2, (y+1)*length+length/2))

    if cell.walls["right"]:
        pygame.draw.line(screen, (231, 230, 247), ((x+1)*length+length/2, y*length+length/2), ((x+1)*length+length/2, (y+1)*length+length/2))

dfs = maze.DFS()
canMove=False
solvingDFS=None
bfs = None
greedy = None
Astar=None
phase = ""
dfs_done = False
bfs_done = False
won=False
timerStarted=False
while running:
    screen.fill((174, 163, 176))
    events=pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: #if user clicks on the X
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if startGame.isClicked() and not timerStarted: #and not canMove and dfs_done
                # print("startGame clicked")
                # canMove = True
                # timer.activateTimer()
                # timerStarted = True
                maze.resetMaze() #resets maze to original grid
                dfs = maze.DFS() #calls the function and "yield" stops when a wall gets removed
                dfs_done = False #since we are starting a new dfs maze, set dfs_done to false, this ensures that player cant move yet and that bfs wont run yet
                character.reset(length/2) #return character to start position
                won = False #set won to false since we are JUST starting a new maze
                phase = "dfs" #set phase to dfs, since we are currently generating


            elif solveBFS.isClicked() and dfs_done : #if user wants to solve with BFS AND the dfs generation is done a\
                bfs = maze.BFS() #calls the method for the first time and yield causes it to return once a link is created between two cells
                phase = "bfs"

            elif solveGreedy.isClicked() and dfs_done:
                greedy = maze.gbfs()
                phase = "greedy"

            elif solveAstar.isClicked() and dfs_done:
                Astar = maze.AStar()
                phase = "Astar"
            elif solveDFS.isClicked() and dfs_done:
                solvingDFS=maze.solvingDFS()
                phase="solvingDFS"
            elif clearMaze.isClicked() and phase not in ["dfs","bfs","Astar","solvingDFS", "greedy"]:
                maze.resetLinks()
            elif timerStarted and restartGame.isClicked():
                timer.activateTimer()
                timerStarted = True
                character.reset(length/2)
                won=False
                canMove=True
                timer.timeUp = False
            elif reset.isClicked():
                phase = "reset"
        elif event.type == pygame.USEREVENT and timer.timerActive and dfs_done :
            timer.currentSeconds -= 1
            if timer.currentSeconds == 0:
                timer.timeUp=True
                timer.deactivateTimer()


    keys = pygame.key.get_pressed() #returns a list of keys with t or f for each key indicating if it is pressed rn



    if phase == "dfs": #this is true when you click the generateMazeDFS button
        try:
            next(dfs) #runs the next iteration of DFS generator method till a wall is removed then returns (when it returns it runs through the rest of the code and renders this on the screen then goes through the condition again, removed next wall, and so on till the stack is empty and method/generator  stops)
        except StopIteration: #if the stack is empty, the DFS generation method ended
            dfs_done = True #dfs_done is true now, now the player can move
            phase = "idle"  # set phase to idle which just waits for controls
            canMove = True
            timer.activateTimer()
            timerStarted = True

    elif phase == "bfs" : #same as dfs generator
        try:
            next(bfs)
        except StopIteration:
            phase = "idle"
            
    elif phase == "greedy":
        try:
            next(greedy)
        except StopIteration:
            phase = "idle"
    elif phase == "Astar":
        try:
            next(Astar)
        except StopIteration:
            phase = "idle"
    elif phase == "solvingDFS":
        try:
            next(solvingDFS)
        except StopIteration:
            phase = "idle"
    elif phase=="reset":
        maze.resetMaze()
        dfs = maze.DFS()
        bfs = None
        dfs_done = False
        character.reset(length/2)
        won = False
        phase = "idle"
        canMove=False
        timer.resetTimer()
        timerStarted = False

    if timer.timeUp:
        canMove=False
        screen.blit(time_msg, (screenWidth / 2 - 70, maze.width + 40))
    if not won and canMove:  # character can move ONLY when dfs is done and when they did not win yet
        character.characterMovement(keys, maze)  # this method processes movement of character
        won = character.mazeSolved(maze)  # as player keeps moving, keep checking whether they won yet, if they did the condition will break, they wint be able to move.

    # elif not won and phase in ["bfs", "greedy", "Astar","solvingDFS"] :  # Allow movement during BFS or Greedy phases
    #     character.characterMovement(keys, maze)  # Process character movement
    #     won = character.mazeSolved(maze) # as player keeps moving, keep checking whether they won yet, if they did the condition will break, they wint be able to move.
    #
    elif won:
        # if the user won, draw win msg
        character.resetDirections()
        canMove=False
        timer.deactivateTimer()
        screen.blit(win_msg, (screenWidth / 2 - 60, maze.width + 40))
    #timer.updateTimer()
    timer.drawTimer()
    #drawing buttons
    #generateMazeDFS.drawButton(screen)
    clearMaze.update(events)
    solveBFS.update(events)
    solveGreedy.update(events)
    solveAstar.update(events)
    solveDFS.update(events)
    startGame.update(events)
    reset.update(events)
    restartGame.update(events)
    ##
    clearMaze.drawButton(screen)
    solveBFS.drawButton(screen)
    reset.drawButton(screen)
    solveAstar.drawButton(screen)
    solveDFS.drawButton(screen)
    solveGreedy.drawButton(screen)
    startGame.drawButton(screen)
    if timerStarted:
        restartGame.drawButton(screen)
    drawGrid()#draw grid


   # if phase in ("bfs", "bfs_done"):   useless line
    drawGridPath()#draws maze solution
    character.animate(screen)#draw character

    pygame.display.update()#updates screen each frame

    clock.tick(20)
pygame.quit()
