from pygame import Surface, Rect, transform
def get_centered_blit_pos(rectangle :Rect, sprite :Surface):
    return rectangle.centerx - sprite.get_width()//2, rectangle.centery - sprite.get_height()//2

def resize_to_width(surface : Surface, width, smoothscale = True):
    scale_amount = width / surface.get_width()
    new_size = (int(surface.get_width() * scale_amount), int(surface.get_height() * scale_amount))
    if smoothscale:
        return transform.smoothscale(surface, new_size)
    else:
        return transform.scale(surface, new_size)