
import pygame
class Character:
    def __init__(self, maze,x,y):
        self.maze = maze
        self.x=x
        self.y=y
        self.vel=maze.length
        self.direction={
            "up":False,
            "down":False,
            "left":False,
            "right":False
        }
        self.walkRight = [
            pygame.image.load(r"sprite/right/right1.png"),
            pygame.image.load(r"sprite/right/right2.png"),
            pygame.image.load(r"sprite/right/right3.png"),
            pygame.image.load(r"sprite/right/right4.png"),
        ]

        self.walkLeft = [
            pygame.image.load(r"sprite/left/left1.png"),
            pygame.image.load(r"sprite/left/left2.png"),
            pygame.image.load(r"sprite/left/left3.png"),
            pygame.image.load(r"sprite/left/left4.png"),
        ]

        self.walkUp = [
            pygame.image.load(r"sprite/up/up1.png"),
            pygame.image.load(r"sprite/up/up2.png"),
            pygame.image.load(r"sprite/up/up3.png"),
            pygame.image.load(r"sprite/up/up4.png")
        ]

        self.walkDown = [
            pygame.image.load(r"sprite/down/down1.png"),
            pygame.image.load(r"sprite/down/down2.png"),
            pygame.image.load(r"sprite/down/down3.png"),
            pygame.image.load(r"sprite/down/down4.png")
        ]
        self.idle=[pygame.image.load(r"sprite/idle/idle1.png"),
                   pygame.image.load(r"sprite/idle/idle2.png"),
                   pygame.image.load(r"sprite/idle/idle3.png")]
        self.walkCount=0

    def mazeSolved(self,maze):
        currCellX = int(self.x // maze.length)
        currCellY = int(self.y // maze.length)
        if currCellX == maze.size-1 and currCellY == maze.size-1:
            return True
        return False

    def canPass(self,maze,key):
        currCellX = int(self.x // maze.length)
        currCellY = int(self.y // maze.length)

        nextCellX, nextCellY = currCellX, currCellY

        if key[pygame.K_LEFT]:
            nextCellX -= 1  # move left
        elif key[pygame.K_RIGHT]:
            nextCellX += 1  # move right
        elif key[pygame.K_UP]:
            nextCellY -= 1  # move up
        elif key[pygame.K_DOWN]:
            nextCellY += 1  # move down

        # ensuring next cell is within the grid limits
        if not (0 <= nextCellX < maze.size and 0 <= nextCellY < maze.size):
            return False  # next cell is out of bounds

        # get the current and next cell objects from the grid
        currCell = maze.grid[currCellX][currCellY]
        nextCell = maze.grid[nextCellX][nextCellY]
        print(f"Current cell: [{currCellX},{currCellY}]")
        print(f"next cell: [{nextCellX},{nextCellY}]")
        print(f"Cell walls: {maze.grid[currCellX][currCellY].walls}")
        # check if there is a valid path between the current and next cell
        return maze.thereIsPath(currCell, nextCell)
    def animate(self,screen):
        if self.walkCount>=26:
            self.walkCount=0
        if self.direction["up"]:
            screen.blit(self.walkUp[self.walkCount%4],(self.x,self.y))
        elif self.direction["down"]:
            screen.blit(self.walkDown[self.walkCount%4],(self.x,self.y))
        elif self.direction["left"]:
            screen.blit(self.walkLeft[self.walkCount%4],(self.x,self.y))
        elif self.direction["right"]:
            screen.blit(self.walkRight[self.walkCount%4],(self.x,self.y))
        else:
            screen.blit(self.idle[self.walkCount%3],(self.x,self.y))
    def reset(self):
        self.x = 0
        self.y = 0
    def characterMovement(self,keys,maze):

        if keys[pygame.K_LEFT] and self.x > 0 and self.canPass(maze, keys):
            self.direction["left"] = True
            self.direction["right"] = False
            self.direction["up"] = False
            self.direction["down"] = False
            self.x -= self.vel
            self.walkCount+=1
        elif keys[pygame.K_RIGHT] and self.x < maze.width - maze.length  and self.canPass(maze, keys):
            self.direction["right"] = True
            self.direction["left"] = False
            self.direction["up"] = False
            self.direction["down"] = False
            self.x += self.vel
            self.walkCount+=1

        elif keys[pygame.K_UP] and self.y > 0 and self.canPass(maze, keys):
            self.direction["up"] = True
            self.direction["left"] = False
            self.direction["right"] = False
            self.direction["down"] = False
            self.y -= self.vel
            self.walkCount+=1

        elif keys[pygame.K_DOWN] and self.y < maze.width - maze.length  and self.canPass(maze, keys):
            self.direction["down"] = True
            self.direction["left"] = False
            self.direction["right"] = False
            self.direction["up"] = False
            self.y += self.vel
            self.walkCount+=1

        else:
            self.direction["left"] = False
            self.direction["right"] = False
            self.direction["up"] = False
            self.direction["down"] = False
            self.walkCount =0

    def resetDirections(self):
        self.direction={
            "up":False,
            "down":False,
            "left":False,
            "right":False
        }