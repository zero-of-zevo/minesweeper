import numpy as np
from Game import *
from pathlib import Path
from pickle import load
from copy import deepcopy
from time import sleep

data:list[tuple[Game, tuple[Interaction, tuple[int, int]]]] = []

__here__ = Path(__file__).parent

data_dir = __here__ / "data"

for child in data_dir.iterdir():
  print(child)

print((data_dir / ("data" + str(len(list(data_dir.iterdir())) + 1) + ".pkl")))

def load_data(target: str) -> list[tuple[Game, tuple[Interaction, tuple[int, int]]]]:
  with (data_dir / (target+".pkl")).open("rb") as f:
    return load(f)

for target in data_dir.iterdir():
  if target.is_file() and target.suffix == ".pkl":
    print(target.stem)
    data.extend(load_data(target.stem))

fieldsizex, fieldsizey = 16, 16

print(str(len(data)))

for i in data:
  print("\n")
  print(str(i[0]))
  sleep(0.01)

# dataprime = [[data[24][0].field[j] for j in range(fieldsizey)][i].around for i in range (fieldsizex)]

# dataprime = [[str(data[24][0].field[j][i].around) for i in range(fieldsizex) if data[24][0].field[j][i].state == State.OPENED else data[24][0][j][i]] for j in range(fieldsizey) ]

# dataprime = [[' ' for _ in range(fieldsizex)] for _ in range(fieldsizey)]

# for j in range(fieldsizex):
#   for i in range(fieldsizey):
#     if data[24][0].field[j][i].state == State.OPENED:
#       dataprime[j][i] = str(data[24][0].field[j][i].around)
#     elif data[24][0].field[j][i].state == State.FLAGGED:
#       dataprime[j][i] = str(-1)
#     else:
#       dataprime[j][i] = str(-2)

# def datachanger(d: Block):
#   if d.state == State.OPENED: return d.around
#   elif d.state == State.FLAGGED: return -1
#   else: return -2

# dataprime2 = [[str(datachanger(data[24][0].field[j][i])) for i in range(fieldsizex)] for j in range(fieldsizey)]

# # dataprime = [str(data[24][0].field[j][i].around) for j in range(fieldsizey) for i in range(fieldsizex)]

# print(data[24][0])

# print('\n'.join([' '.join(map(str, j)) for j in dataprime]))
# print('\n'.join([' '.join(map(str, j)) for j in dataprime2]))


# # from Game import *

# # game = Game(16, 16, 40)

# # game.open(6, 9)

# # print(str(game))


# # def datasetup(data: Game):
