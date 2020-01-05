from pygame import *
from src.constants.SETTINGS import STATS
font.init()
cardFont = font.Font("basis33.ttf",45)
statFont = font.Font("basis33.ttf",30)
barFont = font.Font('basis33.ttf', 25)
storyFont = font.Font('basis33.ttf', 22)
class InfoCard():
    def __init__(self, character, visual_handler):
        self.characterName = character.name
        self.backStory = character.story
        self.character = character
        self.profile = visual_handler.profile
        self.portrait = visual_handler.portrait
        self.graphic = Surface((500,300), SRCALPHA)
        self.graphic.fill((255,255,255))
        scalePortrait = transform.scale(self.portrait,(100,100))
        draw.rect(self.graphic, (200, 200, 200), (5, 5, 100, 100))
        self.graphic.blit(scalePortrait,(5,5))
        cardName = cardFont.render(self.characterName.strip(), True, (0,0,0))
        charType = cardFont.render(self.character.caster_class.title(), True, (0,0,0))
        healthText = statFont.render("Health", True, (0,0,0))
        manaText = statFont.render("Mana", True, (0,0,0))
        damageText = statFont.render("Damage", True, (0,0,0))
        self.graphic.blit(charType, (110, 105-charType.get_height()))
        self.graphic.blit(cardName, (110, 5))
        healthDrawSpot = (370-healthText.get_width(), 8)
        manaDrawSpot = (370-manaText.get_width(), 58-manaText.get_height()//2)
        damageDrawSpot = (370-damageText.get_width(), 108 - damageText.get_height())
        draw.rect(self.graphic, (240,240,240), (365-damageText.get_width(), 5, 495-(360-damageText.get_width()), 100))
        self.graphic.blit(healthText, healthDrawSpot)
        self.graphic.blit(manaText, manaDrawSpot)
        self.graphic.blit(damageText, damageDrawSpot)
        healthBarSpot = (375, 10)
        manaBarSpot = (375, 60-manaText.get_height()//2)
        damageBarSpot = (375, 110-damageText.get_height())
        draw.rect(self.graphic, (100,100, 100), (healthBarSpot[0], healthBarSpot[1], 120, 23))
        draw.rect(self.graphic, (100, 100, 100), (manaBarSpot[0], manaBarSpot[1], 120, 23))
        draw.rect(self.graphic, (100, 100, 100), (damageBarSpot[0], damageBarSpot[1], 120, 23))
        draw.line(self.graphic, (0,0,0), (360 - damageText.get_width(), 0), (360 - damageText.get_width(), 110),2)
        draw.line(self.graphic, (0,0,0), (0, 110),(360-damageText.get_width(), 110), 2)
        draw.rect(self.graphic, (255,100,100), (healthBarSpot[0], healthBarSpot[1], int(120*(self.character.max_health/STATS.MAX_HEALTH)), 23))
        draw.rect(self.graphic, (100, 100, 255), (manaBarSpot[0], manaBarSpot[1], int(120*(self.character.max_mana/STATS.MAX_MANA)), 23))
        draw.rect(self.graphic, (255, 255, 100), (damageBarSpot[0], damageBarSpot[1],int( 120*(self.character.attack_damage/STATS.MAX_DAMAGE)), 23))
        for i,v in zip([healthBarSpot, manaBarSpot, damageBarSpot], ['Health', 'Mana', 'Damage']):
            barText = barFont.render(str(v), True, (0,0,0))
            self.graphic.blit(barText, (377, i[1]))

        fontWidth, fontHeight = storyFont.size("a")
        lines = []
        storyWords = self.backStory.replace('\n', ' ').strip().split()
        line = ""
        lineWidth = 0
        for i in storyWords:
            if lineWidth + (len(i*fontWidth)+1) < 490:
                line+=i+' '
                lineWidth+=(len(i)+1)*fontWidth
            else:
                lines.append(line)
                line = i+' '
                lineWidth = (len(i)+1)*fontWidth
        lines.append(line)
        draw.rect(self.graphic, (240, 240, 240), (5, 115, 490, 180))
        for i,v in enumerate(lines):
            storyLine = storyFont.render(v, True, (0,0,0))
            self.graphic.blit(storyLine, (5,i*fontHeight+114))
        self.graphic = self.graphic.convert_alpha()