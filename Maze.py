import random
import heapq
from itertools import count
from Cell import Cell
import time
class Maze:
    def __init__(self,size,length):
        self.size=size
        self.grid=[[Cell(x,y) for y in range(size)] for x in range(size)]
        self.grid[0][0].walls["top"]=False
        self.generateNeighbours()
        self.size=size
        self.length=length
        self.width=self.size*self.length

    def generateNeighbours(self):
      #  print("GENERATING NEIGHBOURS")
        for y in range(self.size):
       #     print("NEIGHBOURS:",y)
            for x in range(self.size):
                cell=self.grid[x][y]
                #print(cell.x,cell.y)
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
                unvisited=[]
                for neighbour in cell.neighbours:
                    if neighbour.visited==False:
                        unvisited.append(neighbour)
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

        #print("next cell to the right:", result)
        return dx==1

    def isToTheLeft(self,currCell,adjacentCell):
        dx =  adjacentCell.x-currCell.x
        result = dx == -1

        #print("next cell to the left:",result)

        return dx==-1

    def isToTheBottom(self,currCell,adjacentCell):
        dy =  adjacentCell.y-currCell.y
        result = dy == 1

        #print("next cell to the bottom:",result)

        return dy ==1
    def isToTheTop(self,currCell,adjacentCell):
        dy =  adjacentCell.y-currCell.y
        result = dy == -1

        #print("next cell to the top:",result)

        return dy==-1
    def thereIsPath(self,currCell,adjacentCell):
        if self.isToTheRight(currCell,adjacentCell) and not currCell.walls["right"]:
         #   print (" there is a path to the right ")

            return True #returns true if the adjacent cell is to the right of current cell, and there is no wall between them
        if self.isToTheLeft(currCell,adjacentCell) and not currCell.walls["left"]:
         #   print (" there is a path to the left ")
            return True

        if self.isToTheBottom(currCell,adjacentCell) and not currCell.walls["bottom"]:
          #  print (" there is a path to the bottom ")

            return True

        if self.isToTheTop(currCell,adjacentCell) and not currCell.walls["top"]:
           # print (" there is a path to the top ")
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
        self.resetLinks()
        self.markAllAsUnvisited()
        cell=self.grid[0][0]
        queue=[]
        #queue.append((cell,None))
        queue.append(cell)
        cell.visited=True
        while len(queue)>0:
            cell=queue.pop(0)
            for neighbour in cell.neighbours:
                if neighbour.visited==False and self.thereIsPath(cell,neighbour):
                    neighbour.visited=True
                    self.createLink(cell,neighbour)
                    if neighbour.x == self.size - 1 and neighbour.y == self.size - 1:
                        neighbour.links["bottom"] = True
                        return #returns if its the end of the maze
                    yield
                    queue.append(neighbour)
    def resetLinks(self):
        for x in range(self.size):
            for y in range(self.size):
                for link in self.grid[x][y].links:
                    self.grid[x][y].links[link] = False

    def gbfs(self):
        # Reset the visited and links information
        self.resetLinks()
        self.markAllAsUnvisited()

        # Priority queue to store cells to be explored
        open_list = []
        counter = count()
        pastCell=None

        # Define a simple heuristic: Manhattan distance to the goal (bottom-right corner)
        def heuristic(cell):
            return abs(cell.x - (self.size - 1)) + abs(cell.y - (self.size - 1))

        # Start from the initial cell (top-left corner)
        start_cell = self.grid[0][0]
        start_cell.visited = True
        # Push the start cell into the priority queue with its heuristic
        heapq.heappush(open_list, (heuristic(start_cell), next(counter), start_cell, pastCell))

        while open_list:
            # Pop the cell with the lowest heuristic value
            _,  _, current_cell, pastCell = heapq.heappop(open_list)

            if pastCell is not None:
                self.createLink(current_cell, pastCell)
                yield

            # If we reached the goal, stop
            if current_cell.x == self.size - 1 and current_cell.y == self.size - 1:
                current_cell.links["bottom"] = True
                return

            # Explore each neighbor
            for neighbour in current_cell.neighbours:
                if not neighbour.visited and self.thereIsPath(current_cell, neighbour):
                    neighbour.visited = True
                    # Push the neighbour into the open list with its heuristic value
                    heapq.heappush(open_list, (heuristic(neighbour), next(counter), neighbour,current_cell))

        # Yield after processing each cell to allow for visualization/animation

    def AStar(self):
        self.resetLinks()
        self.markAllAsUnvisited()
        def is_destination(cell):
            return cell.x == self.size - 1 and cell.y == self.size - 1
        def calculate_h_value(cell):
            return ((cell.x - (self.size - 1)) ** 2 + (cell.y - (self.size - 1)) ** 2) ** 0.5
        def calculate_g_value(cell,next_cell):
            return ((cell.x - next_cell.x) **2 + (cell.y- next_cell.y) **2) ** 0.5
        def calculate_f_value(next_cell,cell):
            return calculate_h_value(next_cell)+calculate_g_value(cell,next_cell)


        counter = count()
        open_list = []
        came_from = {}
        cell= self.grid[0][0]
        start_cell = self.grid[0][0]
        start_cell.visited=False
        past_cell=self.grid[0][0]
        heapq.heappush(open_list, (calculate_f_value(start_cell,start_cell),next(counter),start_cell,past_cell))

        while open_list:
            f, counting, current, cell = heapq.heappop(open_list)
            self.createLink(current, cell)
            yield
            for next_cell in current.neighbours:

               # print(calculate_g_value(current,next_cell))
                if next_cell.visited == False and self.thereIsPath(current, next_cell):
                    current.visited = True
                    came_from[next_cell] = current

                    if is_destination(next_cell):
                        self.createLink(current, next_cell)
                       # print("you made it")
                        path=[]

                        temp=next_cell
                        while temp in came_from and temp !=start_cell:
                            path.append(temp)
                            temp=came_from.get(temp)
                            #print(temp)
                       # print(temp , "gggggg")
                        path.append(start_cell)
                        path.reverse()
                        self.resetLinks()
                        for i in range(len(path)-1):
                            self.createLink(path[i],path[i+1])
                            yield
                        next_cell.links["bottom"] = True

                        return
                    heapq.heappush(open_list, (calculate_f_value(next_cell,current),next(counter), next_cell, current))
                    #yield next_cell


    def solvingDFS(self):
        self.markAllAsUnvisited()
        self.resetLinks()
        stack=[]
        pastCell=None
        cell=self.grid[0][0]
        stack.append((cell,pastCell))
        while len(stack)>0:
            pair=stack.pop()
            cell, pastCell = pair

            if cell.visited==False:
                cell.visited=True
                if pastCell!=None and self.thereIsPath(cell, pastCell):
                    self.createLink(cell, pastCell)
                    yield
                if cell.x == self.size - 1 and cell.y == self.size - 1:
                    cell.links["bottom"] = True
                    return
                pastCell=cell
                unvisited=[]
                for neighbour in cell.neighbours:
                    if self.thereIsPath(cell, neighbour) and neighbour.visited==False:
                        #stack.append((neighbour,pastCell)) #comment out
                        unvisited.append(neighbour)
                random.shuffle(unvisited)
                for n in unvisited:
                    stack.append((n,pastCell))

#code for testing empirical analysis
#
# testMaze=Maze(100,10) #created maze with 100*100 cells
# startTime=time.time()
# testMaze.DFS()
# endTime=time.time()
# print(f"Time for DFS algorithm: {endTime-startTime :.6f}seconds")
# startTime=time.time()
# testMaze.BFS()
# endTime=time.time()
# print(f"Time for BFS solving algorithm: {endTime-startTime :.6f}seconds")
# startTime=time.time()
# testMaze.solvingDFS()
# endTime=time.time()
# print(f"Time for DFS maze solving algorithm: {endTime-startTime :.6f}seconds")
# startTime=time.time()
# testMaze.gbfs()
# endTime=time.time()
# print(f"Time for Greedy algorithm: {endTime-startTime :.6f}seconds")
# startTime=time.time()
# testMaze.AStar()
# endTime=time.time()
# print(f"Time for A star algorithm: {endTime-startTime :.6f}seconds")