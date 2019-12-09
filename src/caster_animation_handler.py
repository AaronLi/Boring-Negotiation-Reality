import src.image_cacher, json, pygame.transform

class VisualHandler:
    def __init__(self, game_clock) -> None:
        self.defend_animation = None
        self.attack_animation = None
        self.spell_animation = None
        self.portrait = None
        self.profile = None
        self.dead = None
        self.stance = None
        self.hurt = None
        self.game_clock = game_clock

    def load_from_file(self, file, image_cacher: src.image_cacher.ImageCacher):
        with open(file) as f:
            data = json.load(f)

            animations_info = data['animations']

            self.defend_animation = image_cacher.load_animation(animations_info['defend'], self.game_clock)
            self.attack_animation = image_cacher.load_animation(animations_info['attack'], self.game_clock)
            self.spell_animation = image_cacher.load_animation(animations_info['spell'], self.game_clock)

            self.portrait = image_cacher.try_load(data['portrait'])
            self.profile = pygame.transform.smoothscale(self.portrait, (100, 100))
            self.dead = image_cacher.try_load(data['dead'])
            self.stance = image_cacher.try_load(data['idle'])
            self.hurt = image_cacher.try_load(data['hurt'])
        return self