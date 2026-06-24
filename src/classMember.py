class Member:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def __repr__(self):
        return f"{self.name} with colour {self.colour}"