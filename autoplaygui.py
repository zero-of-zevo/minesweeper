import tkinter
from game import *
from pathlib import Path
from pickle import dumps
from copy import deepcopy
import tkinter.messagebox as msgbox
import tkinter.font
import time

from exsolver import *
from solver2 import *

__here__ = Path(__file__).parent
data_dir = __here__ / "data"

window=tkinter.Tk()

window.title("ZERO Minesweeper V.0.0.1")
window.resizable(False, False)

font=tkinter.font.Font(family="Pretendard Black", size=12)
boldfont=tkinter.font.Font(family="Pretendard Black", size=16)
lightfont=tkinter.font.Font(family="Pretendard Semibold", size=12)

frame1=tkinter.Frame(window, relief="solid", bd=0, height=1)
frame1.pack(side="top", fill="both")

label=tkinter.Label(window, text="ZERO Minesweeper V.0.0.1", fg="black", relief="solid", bd=0, font=boldfont)
label.pack()

frame1=tkinter.Frame(window, relief="solid", bd=0, height=1)
frame1.pack(side="top", fill="both")

label2=tkinter.Label(window, text="남은 지뢰 갯수 : ", fg="black", relief="solid", bd=0, font=lightfont)
label2.pack()

game = Game(16, 16, 40)
solved: Solve = Solve(game)

sizex, sizey = game.size

frame2=tkinter.Frame(window, relief="solid", bd=0, padx=20, pady=20)
frame2.pack(side="top", fill="both", expand=True)

grid: list[list[tkinter.Button]] = []

for j in range(sizey):
    row = []
    for i in range(sizex):
        # b = tkinter.Button(frame2, overrelief="solid", width=2, height=1, padx=0, pady=0, repeatdelay=1000, repeatinterval=100, text= str(game.field[j][i]), command=lambda x=i, y=j: open(x, y), font=font, fg="gray")
        b = tkinter.Button(frame2, overrelief="solid", width=2, height=1, padx=0, pady=0, repeatdelay=1000, repeatinterval=100, text= str(game.field[j][i]), font=font, fg="gray")
        # b.bind("<Button-3>", lambda e, x=i, y=j: flag(x, y))
        b.grid(row=j, column=i)
        row.append(b)
    grid.append(row)

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

color = ["#D2D2FF", "#B4B4FF", "#A0A0FF", "#6E6EFF", "#2828CD", "#E27DFB", "#BC28FB", "#960a96", "#FF5050", "#EB0000", "#CD0000"]


def update_game():
    label2.config(text="남은 지뢰 갯수 : " + str(game.leftmine))
    for j in range(sizey):
        for i in range(sizex):
            block = game.field[j][i]
            btn = grid[j][i]
            btn.config(text = str(block))
            if block.state == State.CLOSED:
                btn.config(fg="gray")
            if block.state == State.OPENED:
                btn.config(fg=["#2828CD", "#2E8B57", "#B90000", "#1E3269", "#800000", "#008080", "black", "gray"][block.around-1])
            if block.state is State.FLAGGED:
                    btn.config(fg="red")

    testlist = []

    for i in solved.minepredictsets:
        for j in i[0]:
            testlist.append(j)

    for j in range(sizey):
        for i in range(sizex):
            grid[j][i].config(bg="white")
            if game.field[j][i].state == State.CLOSED:
                # if (i, j) in testlist:
                #     # grid[j][i].config(bg="#FFD73C")
                     
                if (i, j) in solved.mineblocks:
                    # grid[j][i].config(bg="#FF8282")
                    grid[j][i].config(bg="red")
                if (i, j) in solved.minepredicts.keys():
                    d = round(solved.minepredicts[(i, j)]*10)
                    # grid[j][i].config(bg='#%02x%02x%02x' % (d, 255-d, 0))
                    grid[j][i].config(bg = color[d])
                if (i,j) in solved.safeblocks:
                    # grid[j][i].config(bg="#68D168")
                    grid[j][i].config(bg="green")
            else:
                if (i,j) in solved.validblocks:
                    grid[j][i].config(bg="yellow")
                

    if game.gameover:
        msgbox.showinfo("Game Over", "You lose!")
        close(False)
    if game.is_win:
        msgbox.showinfo("Game Over", "You win!")
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
                    print(solved.mineblocks)
                    print(solved.safeblocks)
                    print(solved.minepredicts)
                    print(j, i)
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
                        if solved.minepredicts[(i, j)] > highbuf[1]:
                            highbuf = ((i, j), solved.minepredicts[(i, j)])
                        if solved.minepredicts[(i, j)] < lowbuf[1]:
                            lowbuf = ((i, j), solved.minepredicts[(i, j)])
            if (1 - highbuf[1]) >= lowbuf[1]:
                open(lowbuf[0][0], lowbuf[0][1])
            else:
                open(highbuf[0][0], highbuf[0][1])
            update_game()
            return 0

    
    

frame1=tkinter.Frame(window, relief="solid", bd=0, height=1)
frame1.pack(side="top", fill="both")

btn3=tkinter.Button(window, overrelief="solid", width=5, height=1, padx=0, pady=0, repeatdelay=1000, repeatinterval=100, text= "Play", command=play, font=font, fg="black")
btn3.pack()



def save_log():
    (data_dir / ("data" + str(len(list(data_dir.iterdir())) + 1))).with_suffix(".pkl").write_bytes(dumps(game_log))

def close(save):
    if save: save_log()
    reset_game()



window.mainloop()