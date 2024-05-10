import fsa
from typing import Dict, Tuple, Union

BASIS_VECTORS = {
    0: (0, 1, -1),   # N
    1: (1, 0, -1),   # ENE
    2: (1, -1, 0),   # ESE
    3: (0, -1, 1),   # S
    4: (-1, 0, 1),   # WSW
    5: (-1, 1, 0)    # WNW
}

class ant:
    def __init__(self, axialCoords: Tuple[int, int, int]):
        self.r: int = axialCoords[0]
        self.s: int = axialCoords[1]
        self.t: int = axialCoords[2]
        self.facing: int = 0

        self.behavior: fsa.FSA = fsa.FSA()
        self.state: str = self.behavior.getInitialState()

    def __str__(self) -> str:
        return "coords: (%d, %d, %d)\nfacing: %d\nstate: %s" % (self.r, self.s, self.t, self.facing, self.state)

    def act(self) -> None:
        if self.state == 'IDLING':
            return

        if self.state == 'MOVING':
            self.move()
            return

    def detect(self, cell: Dict[str, Union[int, float]], target: str) -> Union[int, float]:
        return cell.get(target, 0)

    def turn(self, angle: int, clockwise: bool = True) -> int:
        self.facing = self.facing + angle * (1 if clockwise else -1) % 6
        return self.facing

    def move(self, dist: int = 1) -> Tuple[int, int, int]:
        facingVector = BASIS_VECTORS[self.facing]
        self.r += facingVector[0] * dist
        self.s += facingVector[1] * dist
        self.t += facingVector[2] * dist
        return (self.r, self.s, self.t)

    def getPos(self) -> Tuple[Tuple[int, int, int], int]:
        return (self.r, self.s, self.t), self.facing
