import src.image_cacher, json, pygame.transform

class VisualHandler:
    def __init__(self, game_clock) -> None:
        self.dead = None
        self.stance = None
        self.hurt = None
        self.game_clock = game_clock