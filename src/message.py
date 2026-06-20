class Message:
    def __init__(self, date, time, contents):
        self.contents = contents
        self.date = date
        self.time = time

    def __repr__(self):
        return f"'{self.contents[:15].strip()}'... at {self.date} {self.time}"