from pygame import Rect
class MenuObject:

    def __init__(self, rect :Rect) -> None:
        self.shape = rect

    def draw(self, surface, *args):
        pass

    def update(self, mx, my, mb, *args):
        pass