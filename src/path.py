class Path:
    def __init__(self, start, end, **kwargs) -> None:
        super().__init__()
        self.end = end
        self.start = start
        self.kwargs = kwargs

    def get_pos(self, progress: float):
        x = self.start[0] + (self.end[0] - self.start[0]) * progress
        y = self.start[1] + (self.end[1] - self.start[1]) * progress
        return x, y