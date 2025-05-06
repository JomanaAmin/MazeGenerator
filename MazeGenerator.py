import random


from Cell import Cell
class MazeGenerator:
    def __init__(self,size):
        self.size=size
        self.grid=[[Cell(x,y) for y in range(size)] for x in range(size)]
        self.grid[0][0].walls["top"]=False
        self.generateNeighbours()

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
        self.grid[self.size-1][self.size-1].walls["bottom"]=False
    def resetMaze(self):
        for y in range(self.size):
            for x in range(self.size):
                self.grid[x][y].visited=False
                for side,status in self.grid[x][y].walls.items():
                    self.grid[x][y].walls[side]=True
        self.grid[0][0].walls["top"] = False

    def isToTheRight(self,currCell,pastCell):
        dx=currCell.x-pastCell.x
        return dx<0

    def isToTheLeft(self,currCell,pastCell):
        dx = currCell.x - pastCell.x
        return dx > 0

    def isToTheBottom(self,currCell,pastCell):
        dy = currCell.y - pastCell.y
        return dy < 0
    def isToTheTop(self,currCell,pastCell):
        dy = currCell.y - pastCell.y
        return dy > 0
maze=MazeGenerator(4)
maze.DFS()