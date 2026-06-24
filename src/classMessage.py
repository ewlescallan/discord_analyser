class Message:
    def __init__(self, date, time, contents, author):
        self.contents = contents
        self.date = date
        self.time = time
        self.author = author

    def __repr__(self):
        return f"'{self.contents[:15].strip()}'... at {self.date} {self.time} written by {self.author}"