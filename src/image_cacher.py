import pygame.image, animation

class ImageCacher:
    def __init__(self) -> None:
        self.loaded_files = {}
        self.hits = 0
        self.misses = 0

    @property
    def requests(self):
        return self.hits+self.misses

    def load_animation(self,animation_info, game_clock):
        animation_frames = [self.try_load(i).convert_alpha() for i in animation_info['sprite_frames']]
        animation_duration = animation_info['animation_duration']
        return animation.Animation(animation_frames, animation_duration, game_clock)

    def try_load(self, file):
        cache_check = self.loaded_files.get(file)
        print('cache',"`%s`"%file,end=' ')
        if cache_check == None:
            cache_check = pygame.image.load(file).convert_alpha()
            self.loaded_files[file] = cache_check
            print('miss')
            self.misses+=1
        else:
            self.hits+=1
            print('hit')
        return cache_check