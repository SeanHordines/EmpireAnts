import fsa
import pygame
from typing import Dict, Tuple, Union

BASIS_VECTORS = {
    0: (0, 1, -1),   # N
    1: (1, 0, -1),   # NE
    2: (1, -1, 0),   # SE
    3: (0, -1, 1),   # S
    4: (-1, 0, 1),   # SW
    5: (-1, 1, 0)    # NW
}

class Ant:
    def __init__(self, axialCoords: Tuple[int, int, int]):
        self.r: int = axialCoords[0]
        self.s: int = axialCoords[1]
        self.t: int = axialCoords[2]
        self.facing: int = 0

        self.width, self.height = 40, 40

        self.behavior: FSA = fsa.FSA()
        self.state: str = self.behavior.getInitialState()

    def __str__(self) -> str:
        return "coords: (%d, %d, %d)\nfacing: %d\nstate: %s" % (self.r, self.s, self.t, self.facing, self.state)

    def setMap(self, map):
        self.map = map

    def setBehavior(self, fsa) -> None:
        self.behavior = fsa
        self.state = self.behavior.getInitialState()

    def getPos(self) -> Tuple[Tuple[int, int, int], int]:
        return (self.r, self.s, self.t), self.facing

    def getXY(self) -> Tuple[int, int]:
        hex = self.map.hexes[self.getPos()[0]]
        x = hex.n * hex.width * 0.75
        y = (hex.m * hex.height) + (hex.n%2 * hex.height * 0.5)

        x += hex.width * 0.5
        y += hex.height * 0.5

        x -= self.width * 0.5
        y -= self.height * 0.5
        return (x, y)

    def next(self, inputVector) ->  None:
        self.state = self.behavior.next(inputVector)

    def act(self):
        state = self.behavior.nodes[self.state]
        funcName = state["func"]
        if funcName == "":
            return
        func = getattr(self, funcName)
        return func()

    def move(self, dist: int = 1) -> Tuple[int, int, int]:
        facingVector = BASIS_VECTORS[self.facing]
        self.r += facingVector[0] * dist
        self.s += facingVector[1] * dist
        self.t += facingVector[2] * dist

        return (self.r, self.s, self.t)

    def turn(self, angle: int, clockwise: bool = True) -> int:
        self.facing = self.facing + angle * (1 if clockwise else -1) % 6
        return self.facing

    def detect(self, cell: Dict[str, float], target: str) -> float:
        return cell.get(target, 0)

class AntSprite(pygame.sprite.Sprite):
    def __init__(self, ant: Ant):
        # extends the base sprite class
        super().__init__()

        # creates a sprite from the associated ant
        self.ant = ant
        self.image = pygame.Surface((self.ant.width, self.ant.height), pygame.SRCALPHA)

        # pixel coords of top left corner
        self.x, self.y = (0, 0)

    def draw(self, screen, color=(120, 120, 240)):
        # draw the hex itself
        pygame.draw.circle(self.image, color, (0.5 * self.ant.width, 0.5 * self.ant.height), 0.5 * self.ant.height)

        # update the top left corner
        self.x, self.y = self.ant.getXY()
        screen.blit(self.image, (self.x, self.y))
