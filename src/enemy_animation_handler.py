import src.image_cacher, json, pygame.transform
from src import pathed_animation
from src import path
from src.visual_handler import VisualHandler
from constants import RECTANGLES, STRINGS


class EnemyVisualHandler(VisualHandler):
    def __init__(self) -> None:
        super().__init__()
        self.death_animation = None
        self.attack = None
        self.attack_effect = None
        self.attack_animations = None

    def animations_complete(self):
        return self.death_animation.isFinishedRunning() and self.attack.isFinishedRunning() and self.attack_effect.isFinishedRunning()

    def load_from_file(self, file, image_cacher: src.image_cacher.ImageCacher):
        with open(file) as f:
            data = json.load(f)

            animations_info = data['animations']

            try:
                self.death_animation = image_cacher.load_animation(animations_info['death'])
            except:
                pass

            self.dead = image_cacher.try_load(data['dead'])
            self.stance = image_cacher.try_load(data['idle'])
            self.hurt = image_cacher.try_load(data['hurt'])
            self.attack = image_cacher.try_load(data['attack'])
            self.attack_animations = {}
            with open(data['attack_effect']) as f:
                attack_info = json.load(f)
                for animation in attack_info:
                    animation_data = attack_info[animation]
                    if animation_data['animation_type'] == 'pathed':
                        sprites = [image_cacher.try_load(image) for image in animation_data['sprites']]
                        print(sprites, animation_data['sprites'])

                        sprite_timing = animation_data['sprite_timing']
                        position_keypoints = animation_data['position_keypoints']
                        position_timing = animation_data['position_timing']
                        if animation == 'default':
                            self.attack_animations.update(EnemyVisualHandler.__expand_animations__(sprites, sprite_timing, position_keypoints, position_timing))
                    elif animation_data['animation_type'] == 'frames':
                        pass
                    else:
                        raise ValueError(f'Unknown animation type encountered while reading {data["attack_effect"]}')
            print(self.attack_animations)
        return self

    @staticmethod
    def __expand_animations__(sprites, sprite_timing, path_keypoints, position_timing):
        animations = {}
        for enemy_rect, enemy_location in zip(RECTANGLES.BATTLE_UI.ENEMY_RECTS, STRINGS.POSITION_LABELS):
            enemy_center = enemy_rect.center
            for player_rect, player_location in zip(RECTANGLES.BATTLE_UI.PLAYER_RECTS, STRINGS.POSITION_LABELS):
                player_center = player_rect.center
                paths = []
                for path_keypoint in path_keypoints:
                    if path_keypoint[0] == 'ATTACKER_POS':
                        start_position = enemy_center
                    else:
                        start_position = path_keypoint[0]
                    if path_keypoint[1] == 'DEFENDER_POS':
                        end_position = player_center
                    else:
                        end_position = path_keypoint[1]
                    path_type = path_keypoint[2]
                    if path_type == 'DIRECT':
                        new_path = path.Path(start_position, end_position)
                        paths.append(new_path)
                    else:
                        raise ValueError(f"Unknown path type: {path_type}")
                new_animation = pathed_animation.PathedAnimation(sprites, sprite_timing, paths, position_timing)
                animations[f'{enemy_location}_{player_location}'] = new_animation
        return animations