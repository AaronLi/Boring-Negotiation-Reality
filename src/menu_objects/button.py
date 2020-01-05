import src.menu_objects.menuobject as mo
class Button(mo.MenuObject):
    def __init__(self, rect, normal_icon = None, hover_icon = None) -> None:
        super().__init__(rect)
        self.hover = False
        self.normal_icon = normal_icon
        self.hover_icon = hover_icon
        self.clicked = False

    def draw(self, surface, *args):
        super().draw(surface, *args)

        if self.hover:
            if self.hover_icon is not None:
                surface.blit(self.hover_icon, self.shape.topleft)
                self.hover_callback(surface, self.shape)
        else:
            if self.normal_icon is not None:
                surface.blit(self.normal_icon, self.shape.topleft)
                self.normal_callback(surface, self.shape)

    def update(self, mx, my, mb, *args):
        self.hover = self.shape.collidepoint(mx, my)
        if mb[0]:
            if self.hover and not self.clicked:
                self.click_callback()
            self.clicked = True
        else:
            self.clicked = False

    def hover_callback(self, surface, shape):
        pass

    def normal_callback(self, surface, shape):
        pass

    def click_callback(self):
        pass