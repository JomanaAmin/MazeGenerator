import random
from os import remove

from Cell import Cell
class MazeGenerator:
    def __init__(self,size):
        self.grid=[[Cell(x,y) for x in range(size)] for y in range(size)]
        self.grid[0][0].walls["top"]=False
        self.size=size
        pass
 #   def gridGenerator(self):
 #       for y in range(self.size):
 #           for x in range(self.size):
 #               print("CELL: ", self.grid[x][y].x, self.grid[x][y].y)
    def generateNeighbours(self):
        
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
        stack=[]
        pastCell=None
        cell=self.grid[0][0]
        stack.append(cell)
        while len(stack)>0:
            cell=stack.pop()
            if not cell.visited:
                cell.visited=True
                if pastCell!=None:
                    self.removeWall(cell, pastCell)
                pastCell=cell
                unvisited=[neighbour for neighbour in cell.neighbours]
                random.shuffle(unvisited)
                for neighbour in unvisited:
                    stack.append(neighbour)

#maze=MazeGenerator(5)
#maze.gridGenerator();