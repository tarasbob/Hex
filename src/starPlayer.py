import starLogic
import random

def playRandomly():
    g = starLogic.Game(10)
    legalmoves = g.getLegalMoves()
    numMoves = 0
    while len(legalmoves) > 0:
        move = random.choice(legalmoves)
        g.makeMove(g.curTurn, move)
        legalmoves = g.getLegalMoves()
        numMoves += 1
    return g.calculatePoints()

for i in range(10000):
    
    r = playRandomly()
    if r == (0, 0):
        print r
        break
print "done"
