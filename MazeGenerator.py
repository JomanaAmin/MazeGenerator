import random


from Cell import Cell


class MazeGenerator:
    def __init__(self,size,length):
        self.size=size
        self.grid=[[Cell(x,y) for y in range(size)] for x in range(size)]
        self.grid[0][0].walls["top"]=False
        self.generateNeighbours()
        self.size=size
        self.length=length
        self.width=self.size*self.length

    def showGrid(self):
        #just prints the grid
        for y in range(self.size):
            for x in range(self.size):
                print("X:",x,"Y:",y)
                print("CELL: ", self.grid[x][y].x, self.grid[x][y].y)

    def generateNeighbours(self):
      #  print("GENERATING NEIGHBOURS")
        for y in range(self.size):
       #     print("NEIGHBOURS:",y)
            for x in range(self.size):
                cell=self.grid[x][y]
                print(cell.x,cell.y)
                if y-1>=0 :#top neighbour
                    cell.neighbours.append(self.grid[x][y-1])
        #            print("top neighbour: ",self.grid[x][y-1].x,self.grid[x][y-1].y)
                if y+1<self.size: #bottom neighbour
                    cell.neighbours.append(self.grid[x][y+1])
         #           print("bottom neighbour: ",self.grid[x][y+1].x,self.grid[x][y+1].y)

                if x-1>=0: #left neighbour
                    cell.neighbours.append(self.grid[x-1][y])
          #          print("left neighbour: ",self.grid[x-1][y].x,self.grid[x-1][y].y)

                if x+1<self.size: #right neighbour
                    cell.neighbours.append(self.grid[x+1][y])
           #         print("right neighbour: ",self.grid[x+1][y].x,self.grid[x+1][y].y)


    def removeWall(self, currentCell, pastCell):

        if self.isToTheRight(currentCell, pastCell): #if the past cell is to the right of current cell
            currentCell.walls["right"]=False
            pastCell.walls["left"]=False
        elif self.isToTheLeft(currentCell,pastCell): #if the past cell is to the left of current cell
            currentCell.walls["left"]=False
            pastCell.walls["right"]=False
        elif self.isToTheBottom(currentCell, pastCell):#if the past cell is at the bottom of current cell
            currentCell.walls["bottom"]=False
            pastCell.walls["top"]=False
        elif self.isToTheTop(currentCell, pastCell):#if the past cell is to the top of current cell
            currentCell.walls["top"]=False
            pastCell.walls["bottom"]=False

    def DFS(self):
        self.grid[self.size-1][self.size-1].walls["bottom"]=False

        stack=[]
        pastCell=None
        cell=self.grid[0][0]
        stack.append((cell,pastCell))
        while len(stack)>0:
            pair=stack.pop()
            cell, pastCell = pair
            if cell.visited==False:
                cell.visited=True
                if pastCell!=None:
                    self.removeWall(cell, pastCell)
                yield
                pastCell=cell
                unvisited=[neighbour for neighbour in cell.neighbours]
                random.shuffle(unvisited)
                for neighbour in unvisited:
                    stack.append((neighbour,pastCell))
        self.markAllAsUnvisited()
    def resetMaze(self):
        for y in range(self.size):
            for x in range(self.size):
                self.grid[x][y].visited=False
                for side,status in self.grid[x][y].walls.items():
                    self.grid[x][y].walls[side]=True
                    self.grid[x][y].links[side]=False

        self.grid[0][0].walls["top"] = False
    def markAllAsUnvisited(self):
        for y in range(self.size):
            for x in range(self.size):
                self.grid[x][y].visited=False


    def isToTheRight(self,currCell,adjacentCell):
        dx =  adjacentCell.x-currCell.x
        result = dx == 1

        print("next cell to the right:", result)
        return dx==1

    def isToTheLeft(self,currCell,adjacentCell):
        dx =  adjacentCell.x-currCell.x
        result = dx == -1

        print("next cell to the left:",result)

        return dx==-1

    def isToTheBottom(self,currCell,adjacentCell):
        dy =  adjacentCell.y-currCell.y
        result = dy == 1

        print("next cell to the bottom:",result)

        return dy ==1
    def isToTheTop(self,currCell,adjacentCell):
        dy =  adjacentCell.y-currCell.y
        result = dy == -1

        print("next cell to the top:",result)

        return dy==-1
    def thereIsPath(self,currCell,adjacentCell):
        if self.isToTheRight(currCell,adjacentCell) and not currCell.walls["right"]:
            print (" there is a path to the right ")

            return True #returns true if the adjacent cell is to the right of current cell, and there is no wall between them
        if self.isToTheLeft(currCell,adjacentCell) and not currCell.walls["left"]:
            print (" there is a path to the left ")

            return True

        if self.isToTheBottom(currCell,adjacentCell) and not currCell.walls["bottom"]:
            print (" there is a path to the bottom ")

            return True

        if self.isToTheTop(currCell,adjacentCell) and not currCell.walls["top"]:
            print (" there is a path to the top ")
            return True

        return False #There is no path because a wall exists between the cell and its adjacent cell
    def createLink(self,cell,adjacentCell):
        if self.isToTheTop(cell,adjacentCell):
            cell.links["top"]=True
            adjacentCell.links["bottom"]=True

        if self.isToTheBottom(cell, adjacentCell):
            cell.links["bottom"] = True
            adjacentCell.links["top"] = True

        if self.isToTheRight(cell,adjacentCell):
            cell.links["right"] = True
            adjacentCell.links["left"] = True

        if self.isToTheLeft(cell,adjacentCell):
            cell.links["left"] = True
            adjacentCell.links["right"] = True


    def BFS (self):
        cell=self.grid[0][0]
        queue=[]
        #queue.append((cell,None))
        queue.append(cell)
        cell.visited=True
        while len(queue)>0:
           # pair=queue.pop(0)
           # cell, pastCell = pair
            cell=queue.pop(0)

            for neighbour in cell.neighbours:
                if neighbour.visited==False and self.thereIsPath(cell,neighbour):
                    if neighbour.x==self.size-1 and neighbour.y==self.size-1:
                        self.createLink(cell, neighbour)

                        #cell.links["bottom"]=True
                        return
                    neighbour.visited=True
                    self.createLink(cell,neighbour)
                    yield
                    #queue.append((neighbour,cell))
                    queue.append(neighbour)
        self.resetLinks()
    def resetLinks(self):
        for y in self.grid:
            for x in self.grid:
                for link,status in self.grid[x][y].links.items():
                    self.grid[x][y].links[link]=False
