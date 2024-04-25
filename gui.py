import tkinter
from Game import *
from pathlib import Path, PurePath
from pickle import dumps
from copy import deepcopy
import tkinter.messagebox as msgbox
import tkinter.font



# data save

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

game = Game(16, 16, 40)

# game = Game(12, 12, 8)

label2=tkinter.Label(window, text="남은 지뢰 갯수 : 0", fg="black", relief="solid", bd=0, font=lightfont)
label2.pack()

frame1=tkinter.Frame(window, relief="solid", bd=0, height=1)
frame1.pack(side="top", fill="both")

sizex, sizey = game.size

frame2=tkinter.Frame(window, relief="solid", bd=0, padx=20, pady=20)
frame2.pack(side="top", fill="both", expand=True)

# def interact(i, j, obj):
#     print(i, j)
#     game.open(i, j)
#     obj.config(text = str(game.field[j][i]))

grid: list[list[tkinter.Button]] = []

for j in range(sizey):
    row = []
    for i in range(sizex):
        b = tkinter.Button(frame2, overrelief="solid", width=2, height=1, padx=0, pady=0, repeatdelay=1000, repeatinterval=100, text= str(game.field[j][i]), command=lambda x=i, y=j: open(x, y), font=font, fg="gray")
        b.bind("<Button-3>", lambda e, x=i, y=j: flag(x, y))
        b.grid(row=j, column=i)
        row.append(b)
    grid.append(row)

# [(game, (interaction, (x, y)))]
game_log:list[tuple[Game, tuple[Interaction, tuple[int, int]]]] = []



def flag(x, y):
    if not game_log[-1][0] == game:
        game_log.append((deepcopy(game), (Interaction.FLAG, (x, y))))
    game.flag(x,y)
    update_game()

def open(x, y):
    game_log.append((deepcopy(game), (Interaction.OPEN, (x, y))))
    game.open(x,y)
    update_game()

def update_game():
    label2.config(text="남은 지뢰 갯수 : " + str(game.leftmine))
    for j in range(sizey):
        for i in range(sizex):
            grid[j][i].config(text = str(game.field[j][i]))
            if game.field[j][i].state == State.CLOSED:
                grid[j][i].config(fg="gray")
            if game.field[j][i].state == State.OPENED:
                if game.field[j][i].around == 1:
                    grid[j][i].config(fg="#2828CD")
                if game.field[j][i].around == 2:
                    grid[j][i].config(fg="#2E8B57")
                if game.field[j][i].around == 3:
                    grid[j][i].config(fg="#B90000")
                if game.field[j][i].around == 4:
                    grid[j][i].config(fg="#1E3269")
                if game.field[j][i].around == 5:
                    grid[j][i].config(fg="#800000")
                if game.field[j][i].around == 6:
                    grid[j][i].config(fg="#008080")
                if game.field[j][i].around == 7:
                    grid[j][i].config(fg="black")
                if game.field[j][i].around == 8:
                    grid[j][i].config(fg="gray")
            if game.field[j][i].state is State.FLAGGED:
                    grid[j][i].config(fg="red")    
    if game.gameover:
        msgbox.showinfo("Game Over", "You lose!")
        close(False)
    if game.is_win:
        msgbox.showinfo("Game Over", "You win!")
        close(True)
    # print('\n'.join([' '.join(map(str, j)) for j in list(game.getintegerfield(True))]))
    print(str(game))
    print("\n")

def save_log():
    (data_dir / ("data" + str(len(list(data_dir.iterdir())) + 1))).with_suffix(".pkl").write_bytes(dumps(game_log))

def close(save):
    if save: save_log()
    window.quit()
    window.destroy()

window.mainloop()