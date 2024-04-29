from game import *
from solver2 import *
import time
import random
from pathlib import Path
from pickle import dumps
from copy import deepcopy

import sys
sys.setrecursionlimit(500000)

sizex = 16
sizey = 16
countofmines = 40

game = Game(sizex, sizey, countofmines)
solved = Solve(game)

game_log:list[tuple[Game, tuple[Interaction, tuple[int, int]]]] = []

__here__ = Path(__file__).parent
data_dir = __here__ / "data"
def save_log():
    (data_dir / ("data" + str(len(list(data_dir.iterdir())) + 1))).with_suffix(".pkl").write_bytes(dumps(game_log))

def solve():
    global solved
    solved = Solve(game)
    solved.solve()

def startgame():
    global game
    game = Game(sizex, sizey, countofmines)
    game.open(random.randrange(1, sizex), random.randrange(1, sizey))
    play()

def play():
    solve()
    if len([i for i in solved.mineblocks if game.field[i[1]][i[0]].state == State.CLOSED]) + len(solved.safeblocks) > 0:
        for j in range(sizey):
            check = False
            for i in range(sizex):
                # if (i,j) in solved.validblocks:
                if (i, j) in solved.mineblocks and game.field[j][i].state == State.CLOSED:
                    game.flag(i, j)
                    game_log.append((deepcopy(game), (Interaction.FLAG, (i, j))))
                    check = True
                    break
                # if (i, j) in solved.minepredicts.keys():
                if (i,j) in solved.safeblocks and game.field[j][i].state == State.CLOSED:
                    game.open(i, j)
                    game_log.append((deepcopy(game), (Interaction.OPEN, (i, j))))
                    check = True
                    break
            if check: break
    else:
        print("wtf")
        startgame()
    print(str(game))
    print(solved.mineblocks)
    print(solved.safeblocks)
    
    # print(game.is_win)
    if game.is_win == True:
        print("yeah")
        save_log()
        startgame()
    elif game.gameover == True:
        print("lose")
        startgame()
    else:
        play()
    
    # solved.cleandatas()
    # for j in range(sizey):
    #     check = False
    #     for i in range(sizex):
    #         # if (i,j) in solved.validblocks:
    #         if (i, j) in solved.mineblocks and game.field[j][i].state == State.CLOSED:
    #             game.flag(i, j)
    #             game_log.append((deepcopy(game), (Interaction.FLAG, (i, j))))
    #             check = True
    #             break
    #         # if (i, j) in solved.minepredicts.keys():
    #         if (i,j) in solved.safeblocks and game.field[j][i].state == State.CLOSED:
    #             game.open(i, j)
    #             game_log.append((deepcopy(game), (Interaction.OPEN, (i, j))))
    #             check = True
    #             break
    #     if check: break
    # print()
    # print(str(game))
    # print(solved.mineblocks)
    # print(solved.safeblocks)
    
    # # print(game.is_win)
    # if game.is_win == True:
    #     print("yeah")
    #     save_log()
    #     time.sleep(1)
    #     startgame()
    # elif game.gameover == True:
    #     print("lose")
    #     time.sleep(1)
    #     startgame()
    
    # if not len([i for i in solved.mineblocks if not game.field[i[1]][i[0]].state == State.FLAGGED]) + len([i for i in solved.safeblocks if not game.field[i[1]][i[0]].state == State.OPENED]) > 0:
    #     solve()
    #     if len([i for i in solved.mineblocks if not game.field[i[1]][i[0]].state == State.FLAGGED]) + len([i for i in solved.safeblocks if not game.field[i[1]][i[0]].state == State.OPENED]) > 0 and len([i for i in solved.mineblocks if game.field[i[1]][i[0]].state == State.FLAGGED]) + len([i for i in solved.safeblocks if game.field[i[1]][i[0]].state == State.OPENED]) > 0:
    #         time.sleep(0.05)
    #         play()
    #     else:
    #         print("wtf")
    #         time.sleep(1)
    #         startgame()
    # else:
    #     time.sleep(0.05)
    #     play()
    
        

if __name__ == "__main__":
    startgame()