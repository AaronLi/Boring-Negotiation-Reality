import src.animation, json
import src.path
from constants import SETTINGS
import itertools
from typing import List
from pygame import *

from src.image_cacher import ImageCacher


class PathedAnimation(src.animation.Animation):
    def __init__(self, sprites, sprite_timing: List[float], paths: List[src.path.Path], path_timing: List[float]):
        super().__init__(sprites, sum(path_timing))
        if sum(sprite_timing) != sum(path_timing):
            raise ValueError("Sprite frame timing and sprite position timing are not aligned")
        self.paths = paths
        self.path_timing = path_timing
        self.sprite_timing = sprite_timing

    def isFinishedRunning(self):
        return self.numFramesPassed / SETTINGS.VIDEO.FRAME_RATE >= self.duration

    @staticmethod
    def loadFromFile(filename, image_cache: 'ImageCacher'):
        with open(filename) as f:
            data = json.load(f)
            position_keypoints = data['position_keypoints']
            position_timing = data['position_timing']
            sprite_timing = data['sprite_timing']
            sprites = [image_cache.try_load(file) for file in data['sprites']]
            return PathedAnimation(sprites, sprite_timing, position_keypoints, position_timing)

    def get_current_path(self):
        elapsed_time = round(self.numFramesPassed / SETTINGS.VIDEO.FRAME_RATE, 2)
        assert elapsed_time <= self.duration
        for progress_time, path, path_time in zip(itertools.accumulate(self.path_timing), self.paths, self.path_timing):
            if progress_time >= elapsed_time:
                return path, path_time, progress_time

    def draw(self, surface: Surface, x, y, w=None, h=None):
        path, path_duration, path_end_time = self.get_current_path()
        elapsed_time = self.numFramesPassed / SETTINGS.VIDEO.FRAME_RATE
        px, py = path.get_pos(1 - ((path_end_time - elapsed_time)/ path_duration))
        draw_frame = self.current_frame
        surface.blit(draw_frame, (int(px - draw_frame.get_width()/2), int(py - draw_frame.get_width()/2)))
