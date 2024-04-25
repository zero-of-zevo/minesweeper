from Game import *


class Solve:
  def __init__(self, game: Game):
    self.game = game
    self.openedblocks:list[tuple[tuple[int, int], int]] = []
    self.safeblocks:list[tuple[int,int]] = []
    self.mineblocks:list[tuple[int,int]] = []
    for j in range(self.game.size[1]):
      for i in range(self.game.size[0]):
        if self.game.field[j][i].state == State.OPENED and not self.game.field[j][i].around == 0 :
          self.openedblocks.append(((i, j), self.game.field[j][i].around))
  
  def solve(self):
    for d in self.openedblocks:
      aroundclosedblockes:list[tuple[int][int]] = []
      aroundflagedblockes:list[tuple[int][int]] = []
      for j in [-1, 0, 1]:
        for i in [-1, 0, 1]:
          if 0 <= d[0][1] + j < self.game.size[1] and 0 <= d[0][0] + i < self.game.size[0]:
            if self.game.field[d[0][1] + j][d[0][0] + i].state == State.CLOSED:
              aroundclosedblockes.append((d[0][0] + i,d[0][1] + j))
            if self.game.field[d[0][1] + j][d[0][0] + i].state == State.FLAGGED:
              aroundflagedblockes.append((d[0][0] + i,d[0][1] + j))
      if len(aroundflagedblockes) == d[1]:
        self.safeblocks.extend(aroundclosedblockes)
      elif len(aroundclosedblockes) == d[1]:
        self.mineblocks.extend(aroundclosedblockes)
    print(self.openedblocks)
    print()
    print(self.mineblocks)
    print()
    print(self.safeblocks)