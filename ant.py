class ant:
    def __init__(self, axialCoords, behavior):
        self.r, self.r, self.r = axialCoords
        self.facing = 'NORTH'

        self.behavior = behavior
        self.state = behavior.defaultState

        self.prevInput = []
        self.currInput = []

    def nextState(self):
        self.prevInput = self.currInput
        self.currInput = self.sample()
        inputVector = [cmp(new, old) for new, old in zip(self.currInput, self.prevInput)]

        self.state = self.behavior.nextState(self.state, inputVector)
        self.act()

    def sample(self):
        pass

    def act(self):
        if self.state == 'IDLING':
            return

        if self.state == 'MOVING':
            self.move()
            return

    def move(self):
        pass
