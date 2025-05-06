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
        dx=currentCell.x-pastCell.x
        dy=currentCell.y-pastCell.y
        if dx!=0:
            if dx<0:
                currentCell.walls["right"]=False
                pastCell.walls["left"]=False
            else:
                currentCell.walls["left"]=False
                pastCell.walls["right"]=False
        else:
            if dy<0:
                currentCell.walls["bottom"]=False
                pastCell.walls["top"]=False
            else:
                currentCell.walls["top"]=False
                pastCell.walls["bottom"]=False
    def DFS(self):
        print("INSIDE DFS")
        stack=[]
        pastCell=None
        cell=self.grid[0][0]
        stack.append((cell,pastCell))
        while len(stack)>0:
            pair=stack.pop()
            cell, pastCell = pair
            if cell.visited==False:
                cell.visited=True
                print(cell.x,cell.y)
                if pastCell!=None:
                    self.removeWall(cell, pastCell)
                pastCell=cell
                unvisited=[neighbour for neighbour in cell.neighbours]
                random.shuffle(unvisited)
                for neighbour in unvisited:
                    stack.append((neighbour,pastCell))
        self.grid[self.size-1][self.size-1].walls["bottom"]=False
maze=MazeGenerator(4)
maze.DFS()