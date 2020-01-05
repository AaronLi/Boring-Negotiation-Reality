from pygame import Surface, draw, SRCALPHA
from src.constants import COLOURS, RECTANGLES, SETTINGS

class DialogSection:
    def __init__(self) -> None:
        super().__init__()

        self.fade_in_time = 1
        self.fade_out_time = 1
        self.text_finished_wait_time = 1
        self.__text = ""
        self.reader_icon = Surface((150, 150))
        self.background_image = Surface((1260, 650))
        self.__cps = 0
        self.total_time = 0
        self.cps = 15
        self.passed_time = 0
        self.draw_font = None
        self.font_colour = COLOURS.BLACK


    def update(self, delta_time):
        self.passed_time += delta_time

    def draw(self, draw_surface):

        num_characters_to_show = int(self.get_text_progress() * len(self.text))

        draw_surface.blit(self.background_image, (0,0))

        draw.rect(draw_surface, COLOURS.WHITE, RECTANGLES.CUTSCENES.LORE_RECT)
        draw.rect(draw_surface, COLOURS.BLACK, RECTANGLES.CUTSCENES.PROFILE_RECT, 3)
        draw.rect(draw_surface, COLOURS.BLACK, RECTANGLES.CUTSCENES.LORE_RECT, 3)
        draw_surface.blit(self.reader_icon, (0, 600))

        if self.draw_font is not None:
            rendered_text = self.draw_font.render(self.__text[:num_characters_to_show], True, self.font_colour)

            draw_surface.blit(rendered_text, (160, 610))

        if self.is_fading_in():
            draw_surface.blit(self.get_faded_surface((0,0,0), 255 - self.fade_in_progress() * 255, SETTINGS.VIDEO.SCREEN_SIZE), (0, 0))
        elif self.is_fading_out() or self.is_done():
            draw_surface.blit(
                self.get_faded_surface((0, 0, 0), self.fade_out_progress() * 255, SETTINGS.VIDEO.SCREEN_SIZE), (0, 0))

    def is_fading_in(self):
        return 0 <= self.fade_in_progress() < 1

    def is_fading_out(self):
        return 0 <= self.fade_out_progress() < 1


    def is_done(self):
        return self.get_cutscene_progress() >= 1

    def fade_in_progress(self):
        return min(max(0,self.passed_time / self.fade_in_time), 1)

    def fade_out_progress(self):
        return min(max(0, (self.passed_time - self.fade_in_time - self.text_duration - self.text_finished_wait_time) / self.fade_out_time), 1)


    def calculate_total_time(self):
        self.total_time = (len(self.text) / self.cps) + self.fade_in_time + self.fade_out_time + self.text_finished_wait_time

    def get_text_progress(self):
        return max(min((self.passed_time - self.fade_in_time) / self.text_duration, 1), 0)

    def get_cutscene_progress(self):
        return min(self.passed_time / self.total_time, 1)

    def reset(self):
        self.passed_time = 0

    def get_faded_surface(self, colour, alpha, size):
        out_surf = Surface(size, SRCALPHA)

        draw.rect(out_surf, (colour[0], colour[1], colour[2], alpha), (0,0,size[0], size[1]))
        return out_surf

    @property
    def text_duration(self):
        return len(self.text) / self.cps

    @property
    def cps(self):
        return self.__cps

    @cps.setter
    def cps(self, value):
        self.__cps = value
        self.calculate_total_time()

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value

        self.calculate_total_time()