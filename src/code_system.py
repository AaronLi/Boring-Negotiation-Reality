from pygame import *

class CodeSys:
    pokeFont = font.Font("Pokemon GB.ttf", 100)
    bgRect = Rect(0, 0, 1260, 750)
    recta = Surface((555, 170), SRCALPHA)
    bar = Rect(0, 0, 555, 170)

    def __init__(self, image_cacher, screen) -> None:
        self.image_cacher = image_cacher
        self.screen = screen

        self.juvivPics = [(self.image_cacher.try_load("A BNR/CODESYS/juviv" + str(i) + ".png")) for i in
                     range(10)]  # list of the pictures for the code "juviv"
        self.swankPics = [(self.image_cacher.try_load("A BNR/CODESYS/swank" + str(i) + ".png")) for i in
                     range(10)]  # same as above, except for different codes
        self.corgiPics = [(self.image_cacher.try_load("A BNR/CODESYS/corgi" + str(i) + ".png")) for i in range(10)]
        self.punzPics = [(self.image_cacher.try_load("A BNR/CODESYS/punz" + str(i) + ".png")) for i in range(10)]
        self.naePics = [(self.image_cacher.try_load("A BNR/CODESYS/nae" + str(i) + ".png")) for i in range(10)]
        self.guckPics = [(self.image_cacher.try_load("A BNR/CODESYS/guck" + str(i) + ".png")) for i in range(10)]


        # The following is all for the code system
        self.bg = self.image_cacher.try_load("A BNR/CODESYS/code screen.png")
        self.invalidCode = self.image_cacher.try_load("A BNR/CODESYS/invalid.png")  # Code system image if an invalid code is enterred
        self.validCode = self.image_cacher.try_load("A BNR/CODESYS/valid.png")  # Same as above except for other pictures
        self.codeFace = self.image_cacher.try_load("A BNR/CODESYS/code scr face0.png")
        self.codeIMG = self.image_cacher.try_load("A BNR/CODESYS/code0.png")
        self.boisIMG = self.image_cacher.try_load("A BNR/CODESYS/bois0.png")
        self.wahIMG = self.image_cacher.try_load("A BNR/CODESYS/wah.png")
        self.cheatIMG = self.image_cacher.try_load("A BNR/CODESYS/cheat.png")

        self.SLIDESHOW_CODES = {
            'juviv':self.juvivPics,
            'swank':self.swankPics,
            'corgi':self.corgiPics,
            'punz':self.punzPics,
            'nae':self.naePics,
            'guck':self.guckPics,
        }
        self.SINGLE_SLIDE_CODES = {
            'code':self.codeIMG,
            'bois':self.boisIMG,
            'wah':self.wahIMG,
            'cheat':self.cheatIMG
        }

        # More needed things for the coding system

        draw.rect(self.screen, (255, 255, 255), self.bgRect)


    # Secret code system related functions
    def show_slides(self, pics):  # starts the Julie-Vivianne dialogue
        running = True
        frame = 0
        while running:
            for evnt in event.get():
                if evnt.type == QUIT:
                    running = False
                if evnt.type == KEYDOWN:
                    if evnt.key == K_RIGHT:  # if you press right key, frame goes up one
                        frame += 1  # goes to the next image
                        if frame == len(pics):  # if you go up to the last image, it goes back to the main screen
                            return
                    if evnt.key == K_LEFT:  # if you press left, frame goes down one (goes back)
                        frame = max(0, frame-1)
                    if evnt.key == K_k:
                        running = False
            self.screen.blit(pics[frame], (0, 0))
            display.flip()
        return



    def codeSystem(self):  # The code system
        mb = mouse.get_pressed()
        mx, my = mouse.get_pos()
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.validCode, (550, 515))
        self.screen.blit(self.codeFace, (235, 475))
        start = self.screen.copy()  # an image of what the screen initially looks like
        code = ""  # name is what you type out. currently, it's blank
        running = True
        while running:
            for evt in event.get():
                if evt.type == QUIT:
                    running = False
                    return "Menu"
                if evt.type == KEYDOWN:
                    self.screen.blit(start, (0, 0))
                    if len(code) < 5:  # prevents the user from entering codes longer than 5 characters
                        if evt.unicode.isalpha():  # unicode renders what keys are pressed
                            code += evt.unicode  # adds the unicode to name, displays what you type

                    if evt.key == K_BACKSPACE:
                        code = code[:-1]  # backspace removes the last letter that was typed

                    elif evt.key == K_RETURN:  # if you press enter, here we will check what the user entered
                        self.screen.blit(start,
                                    (0, 0))  # when you press enter, the screen goes back to it's original appearance

                        single_slide = self.SINGLE_SLIDE_CODES.get(code)
                        slideshow = self.SLIDESHOW_CODES.get(code)

                        if single_slide is not None:  # if you entered the right code (code=right code) something will happen!
                            self.screen.blit(single_slide, (0, 0))
                        elif slideshow is not None:
                            self.show_slides(slideshow)  # runs a new function to determine what will happen
                            self.screen.blit(start, (0, 0))  # once function is done, blits this image again
                            display.flip()
                        elif code == "bye":
                            quit()
                            running = False

                        else:  # there was the issue where if you pressed enter even if nothing was typed
                            if len(code) > 0:  # it would read it as "invalid", because techincally code="" also means code!=right code
                                self.screen.blit(self.invalidCode,
                                            (550, 515))  # this makes sure it does not read it as incorrect when it is blank

                        code = ""  # after you press enter, code disappears

            draw.rect(CodeSys.recta, (0, 0, 0, 0), CodeSys.bar)
            text = CodeSys.pokeFont.render(code, True, (0, 0, 0))
            CodeSys.recta.blit(text, (0, 50))
            self.screen.blit(CodeSys.recta, (350, 250))

            display.flip()
        return "Menu"