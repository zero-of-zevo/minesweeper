from game import *
@dataclass(frozen=True)
class Soulution:
    mineset: list[tuple[int, int]]
def step(b: Game) -> Soulution:
    s = Soulution()