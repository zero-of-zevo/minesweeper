import tkinter
from game import *
from pathlib import Path
from pickle import dumps
from copy import deepcopy
import tkinter.messagebox as msgbox
import tkinter.font
import time
import sys

sys.setrecursionlimit(10000)

from exsolver import *
from solver2 import *

__here__ = Path(__file__).parent
data_dir = __here__ / "data"


game = Game(16, 16, 40)
solved: Solve = Solve(game)

sizex, sizey = game.size

# [(game, (interaction, (x, y)))]
game_log:list[tuple[Game, tuple[Interaction, tuple[int, int]]]] = []


def flag(x, y):
    if len(game_log) > 0 and not game_log[-1][0] == game:
        game_log.append((deepcopy(game), (Interaction.FLAG, (x, y))))
    game.flag(x,y)

def open(x, y):
    if len(game_log) > 0 and not game_log[-1][0] == game:
        game_log.append((deepcopy(game), (Interaction.OPEN, (x, y))))
    game.open(x,y)

def solve():
    global solved
    solved = Solve(game)
    solved.solve()

def reset_game():
    # print("======================================")
    global game_log
    game_log = list()
    global game
    game = Game(16, 16, 40)
    global solved
    solved = Solve(game)

def update_game():
    print("===============================")
    print(str(game))
    if game.gameover:
        # msgbox.showinfo("Game Over", "You lose!")
        close(False)
    if game.is_win:
        # msgbox.showinfo("Game Over", "You win!")
        close(True)
    
    time.sleep(0.1)
    play()

highbuf:tuple[offset, float] = tuple()
lowbuf:tuple[offset, float] = tuple()

def play():
    if not game.isbuilt:
        open(random.randrange(0, 16), random.randrange(0, 16))
        update_game()
        return 0
    else:
        solve()
        if len(solved.mineblocks) + len(solved.safeblocks) > 0:
            for j in range(sizey):
                for i in range(sizex):
                    if (i, j) in solved.mineblocks:
                        flag(i, j)
                        update_game()
                        return 0
                    elif (i, j) in solved.safeblocks:
                        open(i, j)
                        update_game()
                        return 0
                    
        else:
            global highbuf
            global lowbuf
            for j in range(sizey):
                for i in range(sizex):
                    if (i, j) in solved.minepredicts.keys():
                        print(i, j, solved.minepredicts[(i, j)])
                        if len(highbuf) == 0 or solved.minepredicts[(i, j)] > highbuf[1]:
                            highbuf = ((i, j), solved.minepredicts[(i, j)])
                        if len(lowbuf) == 0 or solved.minepredicts[(i, j)] < lowbuf[1]:
                            lowbuf = ((i, j), solved.minepredicts[(i, j)])
            print(solved.minepredicts)
            print(highbuf)
            print(lowbuf)
            # if (1 - highbuf[1]) >= lowbuf[1]:
            #     open(lowbuf[0][0], lowbuf[0][1])
            # else:
            #     open(highbuf[0][0], highbuf[0][1])
            # update_game()
            return 0

def save_log():
    (data_dir / ("data" + str(len(list(data_dir.iterdir())) + 1))).with_suffix(".pkl").write_bytes(dumps(game_log))

def close(save):
    if save: save_log()
    reset_game()

play()