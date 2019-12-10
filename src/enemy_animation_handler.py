import src.image_cacher, json, pygame.transform
from src.visual_handler import VisualHandler


class EnemyVisualHandler(VisualHandler):
    def __init__(self, game_clock) -> None:
        super().__init__(game_clock)
        self.death_animation = None
        self.attack = None

    def load_from_file(self, file, image_cacher: src.image_cacher.ImageCacher):
        with open(file) as f:
            data = json.load(f)

            animations_info = data['animations']

            try:
                self.death_animation = image_cacher.load_animation(animations_info['death'], self.game_clock)
            except:
                pass

            self.dead = image_cacher.try_load(data['dead'])
            self.stance = image_cacher.try_load(data['idle'])
            self.hurt = image_cacher.try_load(data['hurt'])
            self.attack = image_cacher.try_load(data['attack'])
            self.attack_effect = image_cacher.try_load(data['attack_effect'])
        return self
