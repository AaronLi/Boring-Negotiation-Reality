from pygame import *
class Animation():
    def __init__(self, sprites, totalDuration, gameClockSpeed):
        self.sprites = sprites+[sprites[-1]]
        self.sprite_paths = sprites
        self.duration = totalDuration
        secondsPerSprite = totalDuration/len(sprites)
        self.framesPerSprite = int(gameClockSpeed*secondsPerSprite)
        self.numFramesPassed = 0
    def update(self):
        self.numFramesPassed+=1
    def draw(self, surface, x, y, w=None, h=None):
        if (self.numFramesPassed//self.framesPerSprite) < len(self.sprites):
            spriteToDraw = self.sprites[self.numFramesPassed//self.framesPerSprite]
            scaledSpriteToDraw = transform.scale(spriteToDraw, (spriteToDraw.get_width() if w==None else w, spriteToDraw.get_height() if h==None else h))
            surface.blit(scaledSpriteToDraw, (x, y))
    def isFinishedRunning(self):
        return (self.numFramesPassed//self.framesPerSprite) >= len(self.sprites)
    def reset(self):
        self.numFramesPassed = 0
    def isRunning(self):
        return self.numFramesPassed == 0

    def get_clone(self):
        new_animation = Animation(self.sprite_paths, self.duration, 0)

        new_animation.framesPerSprite = self.framesPerSprite

        return new_animation
    def dictify(self):
        return {
            'sprite_frames':self.sprite_paths,
            'animation_duration':self.duration
        }

    @staticmethod
    def loadFromFile(filename): #TODO: load animations from a json file
        pass