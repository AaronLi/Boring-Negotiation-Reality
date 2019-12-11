import src.image_cacher, json, pygame.transform
from src.visual_handler import VisualHandler


class CasterVisualHandler(VisualHandler):
    def __init__(self, game_clock) -> None:
        super().__init__(game_clock)
        self.defend_animation = None
        self.attack_animation = None
        self.spell_animation = None
        self.portrait = None
        self.profile = None
        self.dead_portrait = None

    @property
    def animations(self):
        return [self.attack_animation, self.spell_animation, self.defend_animation]

    def animations_done(self):
        return all([not animation.isRunning() for animation in self.animations])

    def load_from_file(self, file, image_cacher: src.image_cacher.ImageCacher):
        with open(file) as f:
            data = json.load(f)

            animations_info = data['animations']

            self.defend_animation = image_cacher.load_animation(animations_info['defend'], self.game_clock)
            self.attack_animation = image_cacher.load_animation(animations_info['attack'], self.game_clock)
            self.spell_animation = image_cacher.load_animation(animations_info['spell'], self.game_clock)

            self.portrait = image_cacher.try_load(data['portrait'])
            self.dead_portrait = image_cacher.try_load(data['dead_portrait'])
            self.profile = pygame.transform.smoothscale(self.portrait, (100, 100))
            self.dead = image_cacher.try_load(data['dead'])
            self.stance = image_cacher.try_load(data['idle'])
            self.hurt = image_cacher.try_load(data['hurt'])
        return self