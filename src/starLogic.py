import itertools
import math

class Node:
    def __init__(self, col, coord):
        self.color = col
        self.coordinates = coord
        self.group = -10

    def __str__(self):
        return self.color

class Game:
    def __init__(self, radius):
        self.radius = radius
        self.grid = dict()
        self.neigh = dict()
        self.movesPerTurn = 1
        self.curTurn = 'b'
        self.movesLeft = 1

        for (x, y, z) in itertools.product(range(-self.radius, self.radius+1), repeat=3):
            if x + y + z == 0:
                self.grid[(x, y, z)] = Node('e', (x, y, z))

    def getNeighbors(self, coord):
        (x, y, z) = coord
        if (x, y, z) not in self.grid: return []
        out = [(i + x, j + y, k + z) for (i, j, k)
              in itertools.permutations((0, 1, -1))
              if (i + x, j + y, k + z) in self.grid]
        if (x, y, z) in list(itertools.permutations((0, 1, -1))):
            out.extend(list(itertools.permutations((0, 1, -1))))
            return list(set(out))
        else:
            return out

    def makeMove(self, col, coord):
        if self.curTurn == 'col' and self.grid[coord].color == 'e':
            self.grid[coord].color = col
            self.movesLeft -= 1
        if self.movesLeft < 1:
            #change current player's color
            self.curTurn = 'w' if self.curTurn == 'b' else 'b'
            self.movesLeft = self.movesPerTurn
            
    def calculatePoints(self):
        for coord in self.grid:
            self.grid[coord].tmpCol = self.grid[coord].color

        finished = False
        iters = 0
        while iters < 2 and not finished:
            iters += 1
            numWhiteGroups = 0
            numBlackGroups = 0
            
            #set all nodes to group -10
            for coord in self.grid:
                self.grid[coord].group = -10

            #add all white and black nodes to a group
            fin = False
            while fin == False:
                fin = True
                for coord in self.grid:
                    if self.grid[coord].group == -10:
                        if self.grid[coord].tmpCol == 'w':
                            self.explore(coord, numWhiteGroups)
                            numWhiteGroups += 1
                            fin = False
                        elif self.grid[coord].tmpCol == 'b':
                            self.explore(coord, numBlackGroups)
                            numBlackGroups += 1
                            fin = False
                        

            #count how many edge nodes are in each group               
            numEdgeNodesInWGroup = []
            numEdgeNodesInBGroup = []
            edgeNodes = self.getEdgeNodes()
            
            #set counters to zero
            for i in range(numWhiteGroups):
                numEdgeNodesInWGroup.append(0)
            for j in range(numBlackGroups):
                numEdgeNodesInBGroup.append(0)

            #go through all the edge nodes and increment the number of edgeNodes for the respective group
            for edge in edgeNodes:
                if self.grid[edge].tmpCol == 'w':
                    numEdgeNodesInWGroup[self.grid[edge].group] += 1
                elif self.grid[edge].tmpCol == 'b':
                    numEdgeNodesInBGroup[self.grid[edge].group] += 1

            #turn all white groups with less than two edge nodes into a black group
            finished = True
            for i in range(len(numEdgeNodesInWGroup)):
                if numEdgeNodesInWGroup[i] < 2:
                    finished = False
                    for coord in self.grid:
                        if self.grid[coord].group == i and self.grid[coord].tmpCol == 'w':
                            self.grid[coord].tmpCol = 'b'

            #turn all black groups into white (similar to above)                
            for i in range(len(numEdgeNodesInBGroup)):
                if numEdgeNodesInBGroup[i] < 2:
                    #color group i as white
                    finished = False
                    for coord in self.grid:
                        if self.grid[coord].group == i and self.grid[coord].tmpCol == 'b':
                            self.grid[coord].tmpCol = 'w'

        #calculate final score
        if finished:
            #game ramains stable after two iterations
            whiteScore = 0
            blackScore = 0
            edgeNodes = self.getEdgeNodes()
            print len(edgeNodes)
            print len(self.grid)
            for edge in edgeNodes:
                if self.grid[edge].tmpCol == 'w':
                    whiteScore += 1
                elif self.grid[edge].tmpCol == 'b':
                    blackScore += 1
                else:
                    #edges not filled, not finished
                    return (0, 0)
            blackReward = (numWhiteGroups - numBlackGroups)*2
            whiteReward = -blackReward
            return(blackScore + blackReward, whiteScore + whiteReward)
        else:
            #colors keep on swapping after two iterations, game unfinished
            return (0, 0)

    def getEdgeNodes(self):
        return [(x, y, z) for (x, y, z) in self.grid if max(abs(x), abs(y), abs(z)) == self.radius]

    def explore(self, coord, num):
        col = self.grid[coord].tmpCol
        stack = [coord]
        while len(stack) > 0:
            coord = stack.pop()
            self.grid[coord].group = num
            neigh = self.getNeighbors(coord)
            for n in neigh:
                if self.grid[n].group == -10 and self.grid[n].tmpCol == col: stack.append(n)


g = Game(2)
g.makeMove('b', (1, -1, 0))
g.makeMove('b', (1, 0, -1))
g.makeMove('b', (0, 1, -1))
g.makeMove('b', (-1, 1, 0))
g.makeMove('b', (-1, 0, 1))
g.makeMove('b', (0, -1, 1))
print g.calculatePoints()
