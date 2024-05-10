import fsa

class ant:
    def __init__(self, axialCoords):
        self.r, self.s, self.t = axialCoords
        self.facing = 0

        self.behavior = fsa.FSA()
        self.state = self.behavior.getInitialState()

    def act(self):
        if self.state == 'IDLING':
            return

        if self.state == 'MOVING':
            self.move()
            return

    def turn(self, n, cw = True):
        self.facing = self.facing + n * (1 if cw else -1) % 6

    def move(self):
        if self.facing == 0: # N
            self.s = self.s + 1
            self.t = self.t - 1
        elif self.facing == 1: # ENE
            self.r = self.r + 1
            self.t = self.t - 1
        elif self.facing == 2: # ESE
            self.r = self.r + 1
            self.s = self.s - 1
        elif self.facing == 3: # S
            self.t = self.t + 1
            self.s = self.s - 1
        elif self.facing == 4: # WSW
            self.t = self.t + 1
            self.r = self.r - 1
        elif self.facing == 5: # WNW
            self.s = self.s + 1
            self.r = self.r - 1

    def getPos(self):
        return (self.r, self.s, self.t), self.facing

    def __str__(self):
        return "coords: (%d, %d, %d)\nfacing: %d\nstate: %s" % (self.r, self.s, self.t, self.facing, self.state)
