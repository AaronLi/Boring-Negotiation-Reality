import src.image_cacher, json, pygame.transform

class VisualHandler:
    def __init__(self) -> None:
        self.dead = None
        self.stance = None
        self.hurt = None