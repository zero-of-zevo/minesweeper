from typing import TypeAlias
from game import *
pos: TypeAlias = tuple[int, int]
@dataclass(frozen=True)
class Soulution:
    mineset: list[pos]
def step(b: Game) -> Soulution:
    mineset: list[pos] = []
    numberpos: list[pos] = []
    for x in range(b.size[0]):
        for y in range(b.size[1]):
            b.field[y][x].state == State.OPENED