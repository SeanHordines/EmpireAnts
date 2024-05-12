import math
import queue
import pygame
from typing import Dict, List, Tuple

BASIS_VECTORS = {
    0: (0, 1, -1),   # N
    1: (1, 0, -1),   # NE
    2: (1, -1, 0),   # SE
    3: (0, -1, 1),   # S
    4: (-1, 0, 1),   # SW
    5: (-1, 1, 0)    # NW
}

class Hex:
    def __init__(self, n: int, m: int, radius: int, coordTranslator, values: Dict[str, float] = None):
        # ROW and COL coords
        self.n = n
        self.m = m

        # define the size
        self.radius = radius
        self.width = 2 * self.radius
        self.height = math.sqrt(3) * self.width / 2

        # pixel coords of centerpoint
        self.cx = (self.width * 0.5)
        self.cy = (self.height * 0.5)

        # axial coords
        self.coordTranslator = coordTranslator # this is a function
        self.r, self.s, self.t = self.coordTranslator(n, m)

        if values is None:
            self.values = {}
        else:
            self.values = {}

        self.modified = True

        # define the vertices of the hex
        self.points = []
        for i in range(6):
            px = self.cx + self.radius*math.cos(i*math.pi/3)
            py = self.cy + self.radius*math.sin(i*math.pi/3)
            p = (px, py)
            self.points.append(p)

    def __str__(self) -> str:
        output = ""
        output += "Hex at (%d, %d, %d):\n" % self.getCoords()
        output += str(self.values)
        return output

    def getCoords(self) -> Tuple[int, int, int]:
        return (self.r, self.s, self.t)

    def getDist(self, other) -> int:
        # manhatten distance
        dr = abs(self.r - other.r)
        ds = abs(self.s - other.s)
        dt = abs(self.t - other.t)

        # each step is a difference of two
        return (dr + ds + dt) / 2

    def getNeighbors(self) -> List[Tuple[int, int, int]]:
        neighbors = []
        locationVector = self.getCoords()
        for i in range(6):
            facingVector = BASIS_VECTORS[i]
            neighbor = tuple(x + y for x, y in zip(locationVector, facingVector))
            neighbors.append(neighbor)
        return neighbors

    def setValue(self, valueName: str, newValue: float) -> bool:
        self.values[valueName] = newValue
        self.modified = True

        # remove negative and zero entries
        if newValue <= 0:
            del self.values[valueName]
            return False

        # bool represents whether the value is still in the dict or not
        return True

class HexSprite(pygame.sprite.Sprite):
    def __init__(self, hex):
        # extends the base sprite class
        super().__init__()

        # creates a sprite from the associated hex
        self.hex = hex
        self.image = pygame.Surface((self.hex.width, self.hex.height), pygame.SRCALPHA, 32)
        self.image.fill((0, 0, 0, 0))

        # pixel coords of top left corner
        self.x = self.hex.n * self.hex.width * 0.75
        self.y = (self.hex.m * self.hex.height) + (self.hex.n%2 * self.hex.height * 0.5)

    def draw(self, color=(255, 255, 255)):
        # reset the drawing area to black
        pygame.draw.polygon(self.image, (0, 0, 0), self.hex.points)

        # draw the hex itself
        pygame.draw.polygon(self.image, color, self.hex.points, 3)

        # draw the coords along the bottom edge
        font = pygame.font.Font(None, 14)
        text = font.render(f"({self.hex.r}, {self.hex.s}, {self.hex.t})", True, color)
        textRect = text.get_rect()
        textRect.center = (self.hex.cx, self.hex.cy + self.hex.height * 0.4)
        self.image.blit(text, textRect)

        # changes have been recorded
        self.hex.modified = False

class Hexgrid:
    def __init__(self, row, col, hexRadius = 40):
        # define params
        self.row = row
        self.col = col
        self.hexRadius = hexRadius
        self.hexWidth = 2 * self.hexRadius
        self.hexHeight = math.sqrt(3) * self.hexWidth / 2
        self.screenWidth = 0.75 * self.col * self.hexWidth + 0.25 * self.hexWidth
        self.screenHeight = self.row * self.hexHeight + 0.5 * self.hexHeight

        # setup the game window
        pygame.init()
        pygame.display.set_caption("Hexgrid")
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.screen.fill((0, 0, 0))

        # create a sprite group for the hexes
        self.hexSprites = pygame.sprite.Group()

        # create the map
        self.hexes = {}
        for m in range(self.row):
            for n in range(self.col):
                hex = Hex(n, m, self.hexRadius, self.coordTranslater)

                # store using the axial coords
                self.hexes[hex.getCoords()] = hex

                # make a hex sprite and add to the group
                hexSprite = HexSprite(hex)
                self.hexSprites.add(hexSprite)

    def render(self):
        # render hexes
        for sprite in self.hexSprites:
            if sprite.hex.modified:
                sprite.draw()
                self.screen.blit(sprite.image, (sprite.x, sprite.y))
        pygame.display.flip()

    def coordTranslater(self, n, m):
        # translate to axial coords
        r = n - (self.col // 2)
        s = -m + (self.row // 2) - (n // 2) + (self.col // 4)
        t = -r - s # 0=r+s+t

        return (r, s, t)
