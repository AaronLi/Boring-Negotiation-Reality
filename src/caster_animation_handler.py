import src.image_cacher, json, pygame.transform as transform
from src.visual_handler import VisualHandler
from math_tools import resize_to_width


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

            for animation_set in (self.attack_animation, self.spell_animation):
                frames = animation_set.sprites
                resized_frames = [resize_to_width(frame, 170) for frame in frames]

                animation_set.sprites = resized_frames

            self.portrait = image_cacher.try_load(data['portrait'])
            self.dead_portrait = image_cacher.try_load(data['dead_portrait'])
            self.profile = transform.smoothscale(self.portrait, (100, 100))
            self.dead = resize_to_width(image_cacher.try_load(data['dead']), 170)
            self.stance = resize_to_width(image_cacher.try_load(data['idle']), 170)
            self.hurt = resize_to_width(image_cacher.try_load(data['hurt']), 170)
        return self