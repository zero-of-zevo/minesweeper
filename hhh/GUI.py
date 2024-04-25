#Minesweeper GUI
from pathlib import Path
import tkinter as tk
import tkinter.messagebox as msgbox
from copy import deepcopy
from pickle import load, dumps

from Simulation import Game, Cell, Interaction, State

__here__ = Path(__file__).parent
data_dir = __here__ / "data"

root = tk.Tk()
root.title("Minesweeper")
root.geometry("500x500")

label_leftmine = tk.Label(root, text="Mines: 0")
label_leftmine.grid(row=0, column=0, columnspan=5)
outputfilename = "data001"
if len(list(data_dir.iterdir())) > 0:
    outputfilename = "data"+str(max(map(lambda x: int(x.stem.replace("data","")),[i for i in data_dir.iterdir() if i.suffixes == [".pkl"]]))+1).rjust(3, "0")
outputfile = (data_dir / outputfilename).with_suffix(".pkl")

#Game object
gamesize = (16, 16)
game = Game(*gamesize, 40)
# game.mines = [(0, 4), (1, 1)]
# game.render()
game_history:list[tuple[Interaction, tuple[int, int], Game]] = []

grid: list[list[tk.Button]] = []
def create_grid(width, height):
    global grid
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            cell = tk.Button(root, text="", width=2, height=1, command=lambda x=x, y=y: mine_cell(x, y))
            cell.bind("<Button-3>", lambda e, x=x, y=y: flag_cell(x, y))
            cell.grid(row=y+1, column=x)
            row.append(cell)
        grid.append(row)
    grid[gamesize[1]//2 - 1][gamesize[0]//2 - 1].config(background="aqua")

def mine_cell(x, y):
    game_history.append((Interaction.MINE, (x,y), deepcopy(game)))
    game.sweep(x, y)
    update_grid()
def flag_cell(x, y):
    game_history.append((Interaction.FLAG, (x,y), deepcopy(game)))
    game.flag(x, y)
    update_grid()
    
def update_grid():
    label_leftmine.config(text=f"Mines: {game.leftmine}")
    for y, row in enumerate(game.board):
        for x, cell in enumerate(row):
            grid[y][x].config(text=str(cell), 
                              state=tk.DISABLED if cell.state == State.OPENED else tk.NORMAL,
                              relief=tk.SUNKEN if cell.state == State.OPENED else tk.RAISED)
    if game.is_over:
        msgbox.showinfo("Game Over", "You lose!")
        close()
    if game.is_win:
        msgbox.showinfo("Game Over", "You win!")
        close(True)

create_grid(*gamesize)
def close(save=False):
    if save:
        outputfile.write_bytes(dumps(game_history))
    root.quit()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()