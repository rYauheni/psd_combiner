class ParseTemplate:
    def __init__(self, title, detector, start, end):
        self.title = title
        self.detector = detector
        self.start = start
        self.end = end

    def __repr__(self):
        return f'ParseTemplate object <{self.title}>'
