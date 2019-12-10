from pygame import *
import json
from lib_cutscene import dialog_section

loaded_cutscene_files = {}

def get_file(fName: str, scaled_size = None, smooth_scale = True, font_size = 20, image_cacher = None):
    if fName in loaded_cutscene_files:
        found_file = loaded_cutscene_files[fName]
        file_type = type(found_file)

        if file_type == font.Font:
            if found_file.get_linesize() == font_size:
                print('Found cached version of', fName)
                return found_file

    if fName.endswith('.png') or fName.endswith('.jpg'):
        print('Loaded', fName)
        if image_cacher is None:
            loadedImage = image.load(fName).convert()
        else:
            loadedImage = image_cacher.try_load(fName)
        if scaled_size is not None:
            if smooth_scale:
                loadedImage = transform.smoothscale(loadedImage, scaled_size)
            else:
                loadedImage = transform.scale(loadedImage, scaled_size)

        return loadedImage
    elif fName.endswith('.ttf'):
        print('Loaded',fName)
        loaded_file = font.Font(fName, font_size)
        loaded_cutscene_files[fName] = loaded_file
        return loaded_file

class CutScene:
    def __init__(self, player = None, playerProfile = None) -> None:
        self.lines = []
        self.line_number = 0
        self.playerIcon = player
        self.playerProfileIcon = playerProfile

    def show(self, screen):

        running = True
        clockity = time.Clock()

        while running:
            for e in event.get():
                if e.type == QUIT:
                    running = False

                if e.type == KEYDOWN:
                    if e.key == K_RETURN:
                        running = False

            self.lines[self.line_number].update(clockity.get_time() / 1000)

            self.lines[self.line_number].draw(screen)

            if self.lines[self.line_number].is_done():
                self.line_number += 1

            if self.line_number >= len(self.lines):
                running = False

            display.flip()
            clockity.tick(60)


def load_from_file(fname, playerProfileIcon, image_cacher = None):
    with open(fname) as f:
        data = json.load(f)

        cutSceneOut = CutScene()

        for dialogueLine in data['DialogueLines']:
            newDialogue = dialog_section.DialogSection()

            if 'CharsPerSec' in dialogueLine:
                newDialogue.cps = dialogueLine['CharsPerSec']

            if 'ReaderIcon' in dialogueLine:

                if dialogueLine['ReaderIcon'] == '|PLAYER|':
                    newDialogue.reader_icon = transform.smoothscale(playerProfileIcon, (150,150))
                else:
                    newDialogue.reader_icon = get_file(dialogueLine['ReaderIcon'], scaled_size = (150, 150), image_cacher=image_cacher)

            if 'FadeInTime' in dialogueLine:
                newDialogue.fade_in_time = dialogueLine['FadeInTime']

            if 'FadeOutTime' in dialogueLine:
                newDialogue.fade_out_time = dialogueLine['FadeOutTime']

            if 'TextFinishedWaitTime' in dialogueLine:
                newDialogue.text_finished_wait_time = dialogueLine['TextFinishedWaitTime']

            if 'Text' in dialogueLine:
                newDialogue.text = dialogueLine['Text']

            if 'Background' in dialogueLine:
                newDialogue.background_image = get_file(dialogueLine['Background'], scaled_size=(1260, 650), image_cacher=image_cacher)

            if 'Font' in dialogueLine:
                if 'FontSize' in dialogueLine:
                    newDialogue.draw_font = get_file(dialogueLine['Font'], font_size = dialogueLine['FontSize'])
                else:
                    print('[Error] No font size for font')

            if 'FontColour' in dialogueLine:
                newDialogue.font_colour = dialogueLine['FontColour']

            cutSceneOut.lines.append(newDialogue)
    return cutSceneOut



def create_file_template(fname):
    with open(fname, 'w') as f:
        template = {
            'DialogueLines': [
                {
                    'ReaderIcon': 'A BNR\\hoodhood.png',
                    'Text': 'This is placeholder text for a dialogue',
                    'Background': 'A BNR\\other\\haha.png',
                    'Font': 'basis33.ttf',
                    'FadeInTime': 1,
                    'FadeOutTime': 1,
                    'TextFinishedWaitTime': 1,
                    'CharsPerSec': 15,
                    'FontColour': [0,0,0],
                    'FontSize': 20
                },
            ]
        }

        json.dump(template, f, indent=True)

if __name__ == '__main__':
    create_file_template(input('Enter full file name (with extension): '))
