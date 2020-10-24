from pygame import Surface, Rect
def get_centered_blit_pos(rectangle :Rect, sprite :Surface):
    return rectangle.centerx - sprite.get_width()//2, rectangle.centery - sprite.get_height()//2