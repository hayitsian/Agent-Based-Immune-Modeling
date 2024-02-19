
from cell import BaseCell
from itertools import chain
from copy import deepcopy


    
class Grid():
    """
    The Grid stores the 2d array of environmental information, including the cells present. 
    TODO abstract this class to be a generic grid that can hold any information
    make specialized subclasses for cell grids or protein grids, if necessary
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gridCells = [[None for i in range(width)] for j in range(height)]


    def loadCells(self, _cells: list[BaseCell]):
        for _cell in _cells:
            assert _cell.x >= 0 and _cell.x < self.width, f"Cell x-pos {_cell.x} greater than gameState width {self.width}"
            assert _cell.y >= 0 and _cell.y < self.height, f"Cell y-pos {_cell.y} greater than gameState height {self.height}"
            assert self.gridCells[_cell.x][_cell.y] is None, f"Cell at {_cell.x}, {_cell.y} already exists"
            self.gridCells[_cell.x][_cell.y] = _cell


    def addCell(self, x, y, cell: BaseCell):
        assert cell.x == x and cell.y == y, f"Trying to add cell with position {cell.x}, {cell.y} at grid position {x, y}"
        if self.gridCells[x][y] == None:
            self.gridCells[x][y] = cell
        # else there is already a cell (throw an exception?)

    def removeCell(self, x, y):
        if self.gridCells[x][y] is not None:
            self.gridCells[x][y] = None

    def get(self, x, y):
        return self.gridCells[x][y]
    
    def getAllCells(self):
        return [cell for cell in list(chain(*self.gridCells)) if cell is not None]


    def moveCell(self, cell, window):
        localCells = self.getLocalCells(cell.x, cell.y, window) # movement direction gets full endocrine signal
        oldX = cell.x
        oldY = cell.y
        newx, newy = cell.move(localCells, self.width, self.height) # TODO i do not like this calculation being performed in cell
        

        if oldX != newx or oldY != newy:
            if self.gridCells[newx][newy] is not None:
                oldCell = self.gridCells[newx][newy]
                self.removeCell(newx, newy)
                self.removeCell(oldX, oldY)

                oldCell.x = oldX
                oldCell.y = oldY
                self.addCell(oldX, oldY, oldCell)

                cell.x = newx
                cell.y = newy
                self.addCell(newx, newy, cell)
                return -2 # swap
            # if self.gridCells[oldX][oldY] is None: # ????????????????????? we are passing in a cell at these coordinates
            #     return 0
            else: 
                self.removeCell(oldX, oldY)
                cell.x = newx
                cell.y = newy
                self.addCell(newx, newy, cell)
                return -1 # plain old move
        return 0




    def getLocalArea(self, x, y, radius):
        lowerX = x-radius
        if lowerX < 0: lowerX = 0

        higherX = x+radius
        if higherX >= self.width: higherX = self.width - 1

        lowerY = y-radius
        if lowerY < 0: lowerY = 0

        higherY = y+radius
        if higherY >= self.height: higherY = self.height - 1

        lowerX = int(lowerX)
        lowerY = int(lowerY)
        higherX = int(higherX)
        higherY = int(higherY)

        return lowerX, lowerY, higherX, higherY


    def getLocalCells(self, x, y, radius): 
        # NOTE keep in mind this radius
        # NOTE removes the given cell from local cells
        lowerX, lowerY, higherX, higherY = self.getLocalArea(x, y, radius)


        subGrid = self.gridCells[lowerY:higherY+1] # NOTE: +1 for slicing
        subGrid = [row[lowerX:higherX+1] for row in subGrid]
        noNoneCells = [cell for cell in list(chain(*subGrid)) if cell is not None and (cell.x != x or cell.y != y)]
        return noNoneCells


    def getEmptyNeighbors(self, x, y):
        neighbors = []
        if y+1 < self.height and self.gridCells[x][y+1] is None:
            neighbors.append((x, y+1))
        if y-1 >= 0 and self.gridCells[x][y-1] is None:
            neighbors.append((x, y-1))
        if x-1 >= 0 and self.gridCells[x-1][y] is None:
            neighbors.append((x-1, y))
        if x+1 < self.width and self.gridCells[x+1][y] is None:
            neighbors.append((x+1, y))
        return neighbors


    def getNeighbors(self, x, y, includeEmpty=0) -> list[BaseCell]:
        #returns list of neighbor Cell objects
        neighbors = []
        if y+1 < self.height:
            neighbors.append(self.gridCells[x][y+1])
        if y-1 >= 0:
            neighbors.append(self.gridCells[x][y-1])
        if x+1 < self.width:
            neighbors.append(self.gridCells[x+1][y])
        if x-1 >= 0:
            neighbors.append(self.gridCells[x-1][y])
        if not includeEmpty: return [neigh for neigh in neighbors if neigh is not None]
        return neighbors
    

    def getNeighborPos(self, x, y):
        neighbors = []
        if y+1 < self.height:
            neighbors.append((x, y+1))
        if y-1 >= 0:
            neighbors.append((x, y-1))
        if x+1 < self.width:
            neighbors.append((x-1, y))
        if x-1 >= 0:
            neighbors.append((x+1, y))
        return neighbors
    

    def __str__(self):
        out = [[str(self.gridCells[x][y]) for x in range(self.width)]
               for y in range(self.height)]
        out = [[s.replace("None", " ") for s in line ] for line in out]
        out.reverse()
        return '\n'.join([''.join(x) for x in out])