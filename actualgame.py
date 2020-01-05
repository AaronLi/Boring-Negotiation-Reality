from pygame import *
from tkinter import *
from random import *
import enemy
from src import image_cacher, caster_loader, playerparty, code_system, enemyparty, status_effect, ability
from src.battle_menus import skillselect
from src.enemy_animation_handler import EnemyVisualHandler
from src.constants import *
from lib_cutscene import cutscene

root = Tk()
root.withdraw()
init()

mb = mouse.get_pressed()
omb = mb
mx, my = mouse.get_pos()
playerturn = True  # Global variable dictating whether its the player's turn or the enemies turn

screen = display.set_mode(SETTINGS.VIDEO.SCREEN_SIZE, SRCALPHA)  # making appropriate window

display.set_caption("A Boring Negotiation Reality")
ffont = font.Font("basis33.ttf", 20)
titleFont = font.Font('basis33.ttf', 35)
titleFont.set_italic(True)

image_cacher = image_cacher.ImageCacher()

codes = code_system.CodeSys(image_cacher, screen)
# MUSIC
# mixer.music.load("eo.ogg")
# mixer.music.play(-1)

focusedCard = 0  # This tells us what our players position is relevant to one another



# lib_cutscene shapes and characters speaking

na = image_cacher.try_load("A BNR/hoodhood.png")
na = transform.scale(na, (150, 150))
KK = image_cacher.try_load("A BNR/kim.png")

# lib_cutscene backgrounds
kbattle = image_cacher.try_load("A BNR/kimbg.png")
kbattle = transform.scale(kbattle, (1260, 650))

# image loading for the main menu and cutscenes
menu1 = image_cacher.try_load("A BNR/main menu real.png")

# These are all the scenes used during the opening lib_cutscene
# after battle 3

twentyseven = "[Your party has made to the sorceress' lair!]"
twentyeight = "It's her! the dark sorceress!"
twentynine = "Oh! What a cute bunch of insects. I'm surprised you managed to make it this far."
thirtyone = "No worries, you'll make interesting specimens for my necromacy!"
thirtytwo = "Mwahahahahahah!"
# after battle

thirtythree = "Noooooo!"
thirtyfour = "Hooray!"
thirtyfive = "[You have saved the land of Petraglade! You shall be rememebered eternally and hailed as GODS by the peasants and only them.]"

sceneback = [[kbattle, kbattle, kbattle, kbattle, kbattle], [kbattle, kbattle, kbattle]]

# List of all the scenes
scene = [[twentyseven, twentyeight, twentynine, thirtyone, thirtytwo], [thirtythree, thirtyfour, thirtyfive]]


instructionsPic = image_cacher.try_load("A BNR/help.png")  # The instructions as a single picture to be blit when being called as a function



clicked = False

background = image_cacher.try_load("A BNR/cave.jpg")  # The original background for the game
fire = transform.scale(image_cacher.try_load("FIREBALL.png"), (15, 15))  # An enemies attacking animation
lightning = transform.scale(image_cacher.try_load("lightning.png"), (15, 15))  # An enemies attacking animations

# Confirm and back pictures
confirming = image_cacher.try_load("confirm.png")
backing = image_cacher.try_load("back.png")
# lets be lazy and let the only party leader speak.

selectnums = []  # The numbers in the ordered list that each specific character is associated with from your selection

player_party = playerparty.PlayerParty()  # A 2D list with all of the selected characters stats
skilllist = []  # Another 2D list that has all of the skills for each character
abilitybutton = []  # These are all the ability button names that i load in depending on the characters you select
abilitydesc = []  # Same as above except descriptions for those abilities
framedelay = -1  # This delays each of your characters moves to make for a smoother transition
enemyframedelay = 15  # The enemys delay in order to be a little slower
########################################### UI STUFF
selectpoly = [[(380, 30), (360, 10), (400, 10)], [(375, 220), (355, 200), (395, 200)], [(355, 425), (335, 405), (
    375, 405)]]  # Polygons that blit over your current character or when you're switching characters

character_move_choices = [MENU.COMBAT_MENU_MODES.ATTACK, MENU.COMBAT_MENU_MODES.SKILLS, MENU.COMBAT_MENU_MODES.DEFEND,
                          MENU.COMBAT_MENU_MODES.SWITCH]  # The buttons values to be associated to functions

grunt_animations = EnemyVisualHandler(SETTINGS.VIDEO.FRAME_RATE).load_from_file("datafiles/enemy_visual_datafiles/doge_visual.json", image_cacher)
tough_animations = EnemyVisualHandler(SETTINGS.VIDEO.FRAME_RATE).load_from_file("datafiles/enemy_visual_datafiles/pepe_visual.json", image_cacher)
miniboss_animations = EnemyVisualHandler(SETTINGS.VIDEO.FRAME_RATE).load_from_file("datafiles/enemy_visual_datafiles/spinner_visual.json", image_cacher)
aaron_animations = EnemyVisualHandler(SETTINGS.VIDEO.FRAME_RATE).load_from_file("datafiles/enemy_visual_datafiles/aaron_visual.json", image_cacher)
kim_animations = EnemyVisualHandler(SETTINGS.VIDEO.FRAME_RATE).load_from_file("datafiles/enemy_visual_datafiles/kim_visual.json", image_cacher)
vlad_animations = EnemyVisualHandler(SETTINGS.VIDEO.FRAME_RATE).load_from_file("datafiles/enemy_visual_datafiles/vlad_visual.json", image_cacher)

# All the enemy rounds in order of how they will be coming in a 3D list
enemyrotations = [
    [enemy.Enemy("grunt", 1000, grunt_animations, 250), enemy.Enemy("tough", 1500, tough_animations, 150, 450), enemy.Enemy("grunt", 1000, grunt_animations, 250)],
    [enemy.Enemy("tough", 2500, tough_animations, 300, 600), enemy.Enemy("grunt", 2000, grunt_animations, 400), enemy.Enemy("tough", 2500, tough_animations, 300, 600)],
    [enemy.Enemy("tough", 2500, tough_animations, 300, 600), enemy.Enemy("tough", 2500, tough_animations, 300, 600),
     enemy.Enemy("miniboss", 4000, miniboss_animations, 1000, 750, 500)],
    [enemy.Enemy("grunt", 2500, grunt_animations, 500), enemy.Enemy("aaron", 6000, aaron_animations, 800, 1500, 600), enemy.Enemy("grunt", 2500, grunt_animations, 500)],
    [enemy.Enemy("tough", 3000, tough_animations, 400, 650), enemy.Enemy("tough", 3000, tough_animations, 400, 650), enemy.Enemy("tough", 3000, tough_animations, 400, 650)],
    [enemy.Enemy("tough", 3500, tough_animations, 550, 650), enemy.Enemy("grunt", 3000, grunt_animations, 550), enemy.Enemy("grunt", 3000, grunt_animations, 550)],
    [enemy.Enemy("miniboss", 3800, miniboss_animations, 800, 600, 500), enemy.Enemy("miniboss", 3800, miniboss_animations, 800, 600, 500),
     enemy.Enemy("grunt", 1500, grunt_animations, 400)],
    [enemy.Enemy("tough", 3500, tough_animations, 550, 650), enemy.Enemy("vlad", 8000, vlad_animations, 1000, 1700, 750),
     enemy.Enemy("tough", 3500, tough_animations, 550, 650)],
    [enemy.Enemy("grunt", 3000, grunt_animations, 800), enemy.Enemy("grunt", 3000, grunt_animations, 800), enemy.Enemy("grunt", 3000, grunt_animations, 800)],
    [enemy.Enemy("tough", 2500, tough_animations, 550, 650), enemy.Enemy("tough", 2500, tough_animations, 550, 650), enemy.Enemy("tough", 2500, tough_animations, 550, 650)],
    [enemy.Enemy("miniboss", 3600, miniboss_animations, 750, 600, 500), enemy.Enemy("miniboss", 3600, miniboss_animations, 750, 600, 500),
     enemy.Enemy("miniboss", 3600, miniboss_animations, 750, 600, 500)],
    [enemy.Enemy("miniboss", 2500, miniboss_animations, 800, 600, 500), enemy.Enemy("kim", 10000, vlad_animations, 1100, 650, 800),
     enemy.Enemy("miniboss", 2500, miniboss_animations, 800, 600, 500)]
]
enemy_party = enemyparty.EnemyParty()  # 2D list that has the current enemies inside of it to be blitted and use their stats
currentaction = MENU.COMBAT_MENU_MODES.MAIN_COMBAT_MENU  # This depicts what function is being used (Skills,Attacking,Switching,Defending or none)
currentlyCasting = -1  # Same situation with the current attacker
scenenum = 0  # This is which scene is happening inside of the cscene function
battlenum = 0  # This is which round you are on
beforehealth = -1  # Another variable for an ability (jan's flame shell)
beforehealthtarget = -1  # Also being used for jan's flame shell

deathScreen = image_cacher.try_load("A BNR/deathScreen.png")

running = True  # boolean variable

selected_ability = None
direction = 0
scrollMode = True
tempBirbs = image_cacher.try_load('birbs.png').convert_alpha()  # TODO: remove when I have good art

def charsel(
        clicked):  # This is the character selection function for choosing which characters will be in your party and you'll play the game with
    # TODO: remove magic numbers
    global focusedCard, abilitybutton, abilitydesc, direction, scrollMode  # hee is index of the character that is currently selected in all of the lists
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    keys = key.get_pressed()

    screen.blit(tempBirbs, (0, 0))
    draw.rect(screen, COLOURS.BLACK, (
    305 - infoCards[int(focusedCard)].graphic.get_width() // 2, 0, infoCards[int(focusedCard)].graphic.get_width() + 10,
    755))
    rosterRect = Surface((560, 715), SRCALPHA)
    rosterRect.fill(COLOURS.GREY_TRANSLUCENT)
    screen.blit(rosterRect, (680, 20))
    for i in range(min(int(focusedCard) + 3, len(infoCards) - 1), int(focusedCard), -1):
        v = infoCards[i]
        blitImage = transform.scale(v.graphic, (int((2 / max(abs(focusedCard - i) + 2, 2)) * v.graphic.get_width()),
                                                int((2 / max(abs(focusedCard - i) + 2, 2)) * v.graphic.get_height())))
        maskImage = Surface(blitImage.get_size(), SRCALPHA)
        maskImage.fill((0, 0, 0, min(100 * abs(focusedCard - i), 255)))
        screen.blit(blitImage, (310 - blitImage.get_width() // 2,
                                ((377 - v.graphic.get_height() // 2) + ((i - focusedCard) * blitImage.get_height()))))
        screen.blit(maskImage, (310 - blitImage.get_width() // 2,
                                ((377 - v.graphic.get_height() // 2) + ((i - focusedCard) * blitImage.get_height()))))
    for i in range(max(int(focusedCard) - 3, 0), int(focusedCard + 1)):
        v = infoCards[i]
        blitImage = transform.scale(v.graphic, (int((2 / max(abs(focusedCard - i) + 2, 2)) * v.graphic.get_width()),
                                                int((2 / max(abs(focusedCard - i) + 2,
                                                             2)) * v.graphic.get_height())))  # .convert_alpha()
        maskImage = Surface(blitImage.get_size(), SRCALPHA)
        maskImage.fill((0, 0, 0, min(100 * abs(focusedCard - i), 255)))
        screen.blit(blitImage, (310 - blitImage.get_width() // 2,
                                ((377 - v.graphic.get_height() // 2) + ((i - focusedCard) * blitImage.get_height()))))
        screen.blit(maskImage, (310 - blitImage.get_width() // 2,
                                ((377 - v.graphic.get_height() // 2) + ((i - focusedCard) * blitImage.get_height()))))

    if direction != 0:
        focusedCard = round(focusedCard + direction, 3)
        if abs(focusedCard - int(focusedCard)) < abs(direction) - 0.0001:
            direction = 0
            focusedCard = int(focusedCard)
    else:
        if float(focusedCard).is_integer() and infoCards[int(focusedCard)].characterName.lower() not in [i.name.lower()
                                                                                                         for i in
                                                                                                         player_party.members] and len(
                player_party.members) < 3 and infoCards[int(focusedCard)].characterName.lower() not in [i.name.lower() for i in
                                                                                                player_party.members]:
            focusedCard = int(focusedCard)
            draw.polygon(screen, COLOURS.WHITE, [
                (320 + infoCards[focusedCard].graphic.get_width() // 2, 337),
                (370 + infoCards[focusedCard].graphic.get_width() // 2, 367),
                (320 + infoCards[focusedCard].graphic.get_width() // 2, 397),

            ])
            if Rect(320 + infoCards[focusedCard].graphic.get_width() // 2, 337, 50, 60).collidepoint(mx, my) or keys[
                K_RETURN] or keys[K_RIGHT] or keys[K_d]:
                draw.polygon(screen, COLOURS.GREY, [
                    (320 + infoCards[focusedCard].graphic.get_width() // 2, 337),
                    (370 + infoCards[focusedCard].graphic.get_width() // 2, 367),
                    (320 + infoCards[focusedCard].graphic.get_width() // 2, 397),

                ])
                if mb[0] and not clicked and len(player_party.members) < 3 or keys[K_RETURN] or keys[K_RIGHT] or keys[K_d]:
                    player_party.members.append(stats[focusedCard])
                    selectnums.append(focusedCard)
                    clicked = True
    titleFont.set_italic(True)
    myPartyText = titleFont.render("My Team", False, COLOURS.WHITE)
    screen.blit(myPartyText, (692, 26))
    for i, v in enumerate([i.name.lower() for i in player_party.members]):
        for j in infoCards:
            if j.characterName.lower() == v:
                smallCard = j.graphic.subsurface([0, 0, 500, 110])
                screen.blit(smallCard, (690, i * (smallCard.get_height() + 2) + 60))
                delRect = Rect(695 + smallCard.get_width(), i * (smallCard.get_height() + 2) + 60, 40,
                               smallCard.get_height())
                if delRect.collidepoint(mx, my):
                    draw.rect(screen, (200, 0, 0), delRect)
                    if (mb[0] and not clicked):
                        del player_party.members[i]
                        del selectnums[i]
                        clicked = True
                else:
                    draw.rect(screen, (255, 0, 0), delRect)
                draw.line(screen, COLOURS.WHITE, (delRect.centerx - 10, delRect.centery - 10),
                          (delRect.centerx + 10, delRect.centery + 10), 2)
                draw.line(screen, COLOURS.WHITE, (delRect.centerx - 10, delRect.centery + 10),
                          (delRect.centerx + 10, delRect.centery - 10), 2)
    if (keys[K_a] or keys[K_LEFT] or keys[K_BACKSPACE]) and not clicked:
        for i, v in enumerate(player_party.members):
            if infoCards[int(focusedCard)].characterName.lower() == v.name.lower():
                clicked = True
                del player_party.members[i]
                del selectnums[i]
        clicked = True
    if len(player_party.members) > 0:
        if len(player_party.members) == 3:
            draw.rect(screen, COLOURS.GREEN, (690, 675, 540, 50))
            if Rect(690, 675, 540, 50).collidepoint(mx, my):
                draw.rect(screen, (0, 200, 0), (690, 675, 540, 50))
                if (mb[0] and not clicked):
                    skill_select_menu.update_ability_labels()
                    for i in infoCards:
                        if player_party.party_leader.info_card is i:
                            pl = i.portrait
                            plprof = i.profile
                    clicked = True
                    cutscene.load_from_file('lib_cutscene/Cutscene1.json', plprof, image_cacher).show(screen)
                    if battle(background, battle(background, battle(background, 0))) == -1:
                        return
                    cutscene.load_from_file('lib_cutscene/Cutscene2.json', plprof, image_cacher).show(screen)
                    player_party.restore_all()

                    if battle(background, 3) == -1:
                        return
                    cutscene.load_from_file('lib_cutscene/Cutscene3.json', plprof, image_cacher).show(screen)
                    if battle(background, battle(background, battle(background, 4))) == -1:
                        return
                    cutscene.load_from_file('lib_cutscene/Cutscene4.json', plprof, image_cacher).show(screen)
                    player_party.restore_all()
                    if battle(background, 7) == -1:
                        return
                    cutscene.load_from_file('lib_cutscene/Cutscene5.json', plprof, image_cacher).show(screen)
                    if battle(background, battle(background, battle(background, 8))) == -1:
                        return
                    cscene(clicked, 0, pl, plprof)
                    player_party.restore_all()
                    if battle(background, 11) == -1:
                        return
                    cscene(clicked, 1, pl, plprof)
                    quit()

        else:
            draw.rect(screen, COLOURS.RED, (690, 675, 540, 50))
        titleFont.set_italic(False)
        buttonText = titleFont.render("Start %d/3 >" % len(player_party.members), True, (255, 255, 255))
        screen.blit(buttonText, (1220 - buttonText.get_width(), 700 - buttonText.get_height() // 2))
    if (not clicked) and scrollMode:
        if (focusedCard < len(infoCards) - 1):
            if (mb[0] and my > screen.get_height() // 2) or keys[K_DOWN] or keys[K_s]:
                direction = 0.03
        if (focusedCard > 0):
            if (mb[0] and my < screen.get_height() // 2) or keys[K_UP] or keys[K_w]:
                direction = -0.03
    return clicked


def cscene(clicked, scenenum, pl,
           plprof):  # clicked is whether or not is selected, scenenum is which scene is selected,
    # and pl and plprof are the party leader pics
    global scene
    sceneprof = [[na, plprof, KK, KK, KK],
                 [KK, plprof, na]]  # profile picture order for the dialogue
    clock = time.Clock()


    for j in range(len(scene[scenenum])):  # for each scene presented
        dia = (scene[scenenum][j])  # index of the line of dialogue

        screen.blit(sceneback[scenenum][j], (0, 0))
        #if (sceneback[scenenum][j]) == abattle or (sceneback[scenenum][j]) == vbattle or (
        #        sceneback[scenenum][j]) == kbattle:
            # For the scenes with the minibosses... #TODO fix this!
        #    screen.blit(pl, (200, 250))  # insert the party leader
        draw.rect(screen, COLOURS.WHITE, RECTANGLES.CUTSCENES.LORE_RECT)  # White background for the dialogue/profile
        draw.rect(screen, COLOURS.BLACK, RECTANGLES.CUTSCENES.PROFILE_RECT, 3)
        draw.rect(screen, COLOURS.BLACK, RECTANGLES.CUTSCENES.LORE_RECT, 3)  # outline for the profile picture
        screen.blit(sceneprof[scenenum][j], (0, 600))

        # find a way to blit profiles with the text

        for i in range(len(dia)):  # for each line of each scene
            for evt in event.get():
                if evt.type == KEYDOWN:
                    if evt.key == K_RETURN:
                        return

                        # load the mini pics and test out with a loop?
            text = ffont.render(scene[scenenum][j][:i], True, COLOURS.BLACK)  # formatting of the text

            screen.blit(text, (160, 610))  # centres the text

            display.flip()

            clock.tick(15)  # how long for each line of text


def ngame():  # When you press the new game button
    global clicked, battlenum
    running = True
    clicked = True
    clockity = time.Clock()
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
                return "Menu"
            if evt.type == KEYUP:
                clicked = False
            if evt.type == MOUSEBUTTONUP:
                clicked = False
        clicked = charsel(clicked)
        if clicked is None:
            return "Exit"
        display.flip()
        clockity.tick(SETTINGS.VIDEO.FRAME_RATE)
    return "Menu"


def instructions():  # When you click on the instructions
    running = True

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
                return "Menu"

            mx, my = mouse.get_pos()
            mb = mouse.get_pressed()
            screen.blit(instructionsPic, (0, 0))
            display.flip()
    return "Menu"


def menu():  # function for the main menu
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
                return "Exit"

        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        screen.blit(menu1, (0, 0))

        # selecting a button and a function
        if RECTANGLES.MAIN_MENU.NEW_GAME_RECT.collidepoint(mx, my):
            draw.rect(screen, COLOURS.PURPLE, RECTANGLES.MAIN_MENU.NEW_GAME_RECT, 5)
            if mb[0] == 1:
                return "NGame"
        if RECTANGLES.MAIN_MENU.CONTINUE_RECT.collidepoint(mx, my):
            draw.rect(screen, COLOURS.PURPLE, RECTANGLES.MAIN_MENU.CONTINUE_RECT, 5)
            if mb[0] == 1:
                return "load"
        if RECTANGLES.MAIN_MENU.INSTRUCTION_RECT.collidepoint(mx, my):
            draw.rect(screen, COLOURS.PURPLE, RECTANGLES.MAIN_MENU.INSTRUCTION_RECT, 5)
            if mb[0] == 1:
                return "Instructions"
        if RECTANGLES.MAIN_MENU.CODE_RECT.collidepoint(mx, my):
            draw.rect(screen, COLOURS.PURPLE, RECTANGLES.MAIN_MENU.CODE_RECT, 5)
            if mb[0] == 1:
                return "Codes"
        if RECTANGLES.MAIN_MENU.EXIT_RECT.collidepoint(mx, my):
            draw.rect(screen, COLOURS.PURPLE, RECTANGLES.MAIN_MENU.EXIT_RECT, 5)
            if mb[0] == 1:
                return "Exit"
        display.flip()




##########################################################################
def backstab(target, caster, casters,
             enemies):  # Defining all the skills that are used with damage and heals and other effects for skills. Enemy or Ally rectangles are drawn depending on who the skill targets
    enemies[target].damage(caster.attack_damage * 2, caster)


def silentstrike(target, caster, casters, enemies):
    caster.dodging = True  # TODO: make a property "targetable"


def execute(target, caster, casters, enemies):
    enemies[target].damage(
        (300 + (max(enemies[target].max_health-enemies[target].health, 400 * (len([i for i in enemies if i.is_alive()])-3)))),
        caster)


def lightningbolt(target, caster, casters, enemies):
    enemies[target].damage(300 + 100 ** (1 + (randint(0, 5) / 10)), caster)


def lightningcharge(target, caster, casters, enemies):
    if caster.get_special_stat("lightningCharges") < 5:
        player_party.current_caster.modify_special_stat("lightningCharges", 1)
    else:
        return 1


def lightningrelease(target, caster, casters, enemies):
    if player_party.current_caster.get_special_stat('lightningCharges') >= 5:
        for j in range(3):
            enemies[j].damage(1400, caster)  # TODO: make sure multiplier is applied evenly
    else:
        enemies[target].damage(300 + 250 * player_party.current_caster.get_special_stat("lightningCharges"),
                               caster)
    caster.set_special_stat('lightningCharges', 0)


def herbsandpoultices(target, caster, casters, enemies):
    casters[target].heal(900 if target == caster else 500)


def slay(target, caster, casters, enemies):
    cast_cost = min(300 + 150 * player_party.current_caster.get_special_stat("slayCounter"), 750)

    damage = 300 + 100 * player_party.current_caster.get_special_stat('slayCounter')

    if player_party.current_caster.mana < cast_cost:
        return 1
    enemies[target].damage(damage, caster)
    player_party.current_caster.mana -= cast_cost
    if not enemies[target].is_alive():
        player_party.current_caster.modify_special_stat('slayCounter', 1)


def revoke(target, caster, casters, enemies):
    enemies[target].revoked = True


def healmore(target, caster, casters, enemies):
    for i in range(3):
        if casters[i].is_alive():
            casters[i].heal(900)

def dragonflame(target, caster, casters, enemies):
    enemies[target].add_status_effect(status_effect.DOTEffect("Dragonburn", 3, 300))

def revive(target, caster, casters, enemies):
    if not casters[target].is_alive():
        casters[target].health = casters[target].max_health // 2


def flameshell(target, caster, casters, enemies):
    global beforehealthtarget, currentaction, framedelay, beforehealth
    beforehealthtarget = enemies[target].health  # TODO: flameshell deals 200-400 damage to attacking enemies and lasts 2-3 turns
    beforehealth = player_party.current_caster.health
    player_party.current_caster.tired = False
    currentaction = MENU.COMBAT_MENU_MODES.MAIN_COMBAT_MENU


def firestorm(target, caster, casters, enemies):
    for i in range(3):
        enemies[i].damage(1000, caster)
    if randint(0, 5) == 0:
        caster.damage(700)


def taunt(target, caster, casters, enemies):
    enemies[target].add_taunt_target(caster)


def stabstabstab(target, caster, casters, enemies):
    enemies[target].damage(caster.attack_damage * 3, caster)


def bigtaunt(target, caster, casters, enemies):
    for enemy in enemies:
        enemy.add_taunt_target(caster)


def shieldsup(target, caster, casters, enemies):
    for j in range(3):
        casters[j].set_defending(True)


def lancethrow(target, caster, casters, enemies):
    pass
    # TODO: lancethrow should disable the hero for ane extra turn, maybe make Caster.tired an int?


def fallingsword(target, caster, casters, enemies):
    choice([i for i in enemies if i.is_alive()]).damage(800, caster)


def counterattack(target, caster, casters, enemies):
    pass
    # TODO: counter attack, may need special stat


def preparation(target, caster, casters, enemies):
    caster.damage_multiplier+=1.2


def helpinghand(target, caster, casters, enemies):
    casters[target].damage_multiplier+=0.75
    # TODO: helpinghand, adds to a Caster's storedDamage


def shieldaura(target, caster, casters, enemies):
    pass
    # TODO: shieldaura, maybe change blocking into a float? 1x for normal damage, 0.5x for defending, 0.8x for shieldaura


def extravagantshot(target, caster, casters, enemies):
    caster.heal(800)


def biggerandstronger(target, caster, casters, enemies):
    caster.damage_multiplier += 0.3
    # TODO: biggerandstronger, adds to a caster's storedDamage


def flashyarrow(target, caster, casters, enemies):
    for enemy in enemies:
        enemy.add_taunt_target(caster)


def vampiricstrike(target, caster, casters, enemies):
    caster.heal(min(800, enemies[target].health))


def playdead(target, caster, casters, enemies):
    pass
    # TODO: playdead, add a nontargetable property to Caster


def analyze(target, caster, casters, enemies):
    enemies[target].vulnerable = True
    # TODO: change vulnerable from bool to float multiplier


def cull(target, caster, casters, enemies):
    totalDamageDealt = 0
    for i in range(3):
        if i != target:
            totalDamageDealt += enemies[i].damage(800, caster)


def reap(target, caster, casters, enemies):
    healedAmount = min(enemies[target].health,
                       caster.abilities[2].influence_amount * caster.damage_multiplier)
    livingAllies = [i for i in casters if i.is_alive()]
    for i in livingAllies:
        i.heal(healedAmount / len(livingAllies))



caster_loader = caster_loader.CastersLoader('datafiles/character_datafiles', SETTINGS.VIDEO.FRAME_RATE, image_cacher)
stats = list(caster_loader.casters.values())

infoCards = [i.info_card for i in stats]


def UI():  # This is the UI or health bars that need to be blitted
    for num, i in enumerate(selectnums):
        if player_party.members[num].health > 0:
            screen.blit(stats[i].animation_handler.portrait, (10, [0, 245, 490][num]))
        else:
            screen.blit(stats[i].animation_handler.dead_portrait, (10, [0, 245, 490][num]))
    for playerNum, playerInfo in enumerate(player_party.members):
        # drawhealthbar
        draw.rect(screen, COLOURS.GREEN, (25, 199 + 250 * playerNum, 200, 25), 2)
        draw.rect(screen, COLOURS.BLUE, (25, 225 + 250 * playerNum, 200, 25), 2)
        draw.rect(screen, COLOURS.GREEN,
                  (25, (199 + 250 * playerNum),
                   (2 * (100 * (playerInfo.health) / playerInfo.max_health)), 25),
                  0)
        draw.rect(screen, COLOURS.BLUE,
                  (25, (225 + 250 * playerNum),
                   (2 * (100 * (playerInfo.mana) / playerInfo.max_mana)), 25), 0)
        screen.blit(ffont.render("%4d/%d" % (playerInfo.health, playerInfo.max_health), True,
                                 COLOURS.LIGHT_GREEN),
                    (28, 203 + 250 * playerNum))
        screen.blit(ffont.render("%4d/%d" % (playerInfo.mana, playerInfo.max_mana), True,
                                 COLOURS.LIGHT_BLUE),
                    (28, 228 + 250 * playerNum))
        # draw caster specific icons
        if playerInfo.name.lower() == 'supreet' and playerInfo.is_alive():  # draw supreet's slay counter
            for i in range(playerInfo.get_special_stat('slayCounter')):
                screen.blit(fire, (26 + 16 * i, 180 + 251 * playerNum))
        if playerInfo.name.lower() == 'aliza' and playerInfo.is_alive():
            for i in range(playerInfo.get_special_stat("lightningCharges")):
                screen.blit(lightning, (26 + 16 * i, 180 + 251 * playerNum))
    for enemyInfo, enemyRect in zip(enemy_party.members, RECTANGLES.BATTLE_UI.ENEMY_RECTS):
        if enemyInfo.is_alive():
            draw.rect(screen, COLOURS.WHITE, (enemyRect.x, enemyRect.y - 20, 150, 10), 1)
            draw.rect(screen, COLOURS.WHITE, (enemyRect.x, enemyRect.y - 20, (150 * enemyInfo.health / enemyInfo.max_health), 10), 0)


def battle(area, battlenum):  # The main battle function
    global currentaction, mx, my, mb, omb, clicked, playerturn, framedelay, currentlyCasting, beforehealthtarget
    if battlenum == -1:
        return -1
    enemy_party.members = enemyrotations[battlenum]
    running = True
    clockity = time.Clock()
    speechBubbleTime, speechBubbleText, speechBubbleX, speechBubbleY = 0, '', 0, 0
    while running:
        for evt in event.get():
            mb = mouse.get_pressed()
            mx, my = mouse.get_pos()
            if evt.type == QUIT:
                quit()
                return -1
            if evt.type == MOUSEBUTTONUP:
                clicked = False
            if evt.type == KEYDOWN:
                if evt.key == K_k:
                    for enemy in enemy_party.members:
                        enemy.health = 0
                    print('die')
        if not player_party.defeated:
            if enemy_party.defeated:
                battlenum += 1  # If the enemies are dead then they move on to the next wave
                player_party.current_caster_index = 0
                for caster in player_party.members:
                    caster.tired = False
                return battlenum
            screen.blit(area, (0, 0))  # Blit the area
            UI()
            damage_multipliers = [i.damage_multiplier for i in player_party.members]
            screen.blit(
                ffont.render('Damage Multipliers ' + (' '.join(map(str, damage_multipliers))),
                             True, COLOURS.WHITE, COLOURS.BLACK), (0, 0))
            enemy_party.draw_party(screen)
            player_party.draw_party(screen)

            if (framedelay >= 0):
                framedelay -= 1
            elif framedelay <= -1:  # If your characters went to determine the next ally to go or if its the enemies turn
                if not player_party.can_attack and player_party.animations_done():
                    player_party.current_caster_index = 0
                    playerturn = False
                elif not player_party.current_caster.can_attack() and player_party.animations_done(): #choose a new caster if the current one can't attack
                    player_party.find_next_caster()
            if playerturn:  # While its the players turn
                for enemy in enemy_party.members:
                    enemy.tired = False
                draw.polygon(screen, COLOURS.PURPLE, (selectpoly[player_party.current_caster_index]))
                if framedelay == -1:
                    currentaction = buttons()
                    player_party.current_caster_index = casting(currentaction, player_party.current_caster_index)
            else:  # Its the enemies turn till it turns into the allys turn again
                playerturn = enemycast()
        else:
            # death screen
            screen.blit(deathScreen, (0, 0))
            for i, v in enumerate(selectnums):
                screen.blit(stats[v].animation_handler.dead,
                            (315 + i * 315 - stats[v].animation_handler.dead.get_width() / 2, 500))
            if speechBubbleTime == 0:
                speechBubbleX = 335 + 315 * randint(0, 2)
                speechBubbleY = 500
                speechBubbleText = choice(['Oof', 'Ouch', 'Owie', "I'm dead", "This sucks"])
                speechBubbleTime = 200
            else:
                speechBubbleTime -= 1
            drawSpeechBubble(speechBubbleX, speechBubbleY, speechBubbleText)
        display.flip()
        clockity.tick(60)
        omb = mb
    return battlenum


def drawSpeechBubble(x, y, text, drawSurf=screen):
    renderText = ffont.render(text, True, COLOURS.BLACK)
    draw.polygon(drawSurf, COLOURS.WHITE,
                 [(x, y + renderText.get_height() + 20), (7 + x, y + renderText.get_height() + 20),
                  (5 + x, y + renderText.get_height() + 30), (15 + x, y + 40),
                  (renderText.get_width() + 20 + x, y + 40), (renderText.get_width() + 20 + x, y), (x, y)])
    screen.blit(renderText, (x + (renderText.get_width() + 20) // 2 - renderText.get_width() // 2,
                             y + (renderText.get_height() + 20) // 2 - renderText.get_height() // 2))


def buttons():  # Pressing a button with a function attached calls the function
    global clicked
    if currentaction == MENU.COMBAT_MENU_MODES.MAIN_COMBAT_MENU:
        for b, v in zip(RECTANGLES.BATTLE_UI.ACTION_BUTTONS, character_move_choices):
            draw.rect(screen, COLOURS.BLACK, b, 2)
            if b.collidepoint(mx, my):
                draw.rect(screen, COLOURS.BLACK, b, 5)
                if mb[0] and not omb[0]:
                    clicked = True
                    return v
    return currentaction


skill_select_menu = skillselect.SkillSelect(player_party, enemy_party, backing, image_cacher)

def casting(action, caster):  # This comes from the button being pressed form before
    global currentaction
    if action == MENU.COMBAT_MENU_MODES.ATTACK:
        caster = attack(caster)
    elif action == MENU.COMBAT_MENU_MODES.SWITCH:
        caster = switch(caster)
    elif action == MENU.COMBAT_MENU_MODES.DEFEND:
        caster = defend(caster)
    elif action == MENU.COMBAT_MENU_MODES.SKILLS:
        skill_select_menu.update(mx, my, mb, omb)
        skill_select_menu.draw(screen)
        currentaction = skill_select_menu.currentaction
    return caster



def attack(caster):  # The attacking function for your character selecting an enemy and dealing their damage
    global currentaction, clicked, framedelay
    draw.rect(screen, COLOURS.BUTTONBACK, RECTANGLES.BATTLE_UI.BUTTON_BACKGROUND_FILL, 0)
    draw.rect(screen, COLOURS.BLACK, RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT, 2)
    screen.blit(backing, (320, 620))
    if RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT.collidepoint(mx, my):
        draw.rect(screen, COLOURS.BLACK, RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT, 5)
        if mb[0] and not clicked:
            clicked = True
            currentaction = MENU.COMBAT_MENU_MODES.MAIN_COMBAT_MENU
    for enemy_info, enemy_rect in zip(enemy_party.members, RECTANGLES.BATTLE_UI.ENEMY_RECTS):
        draw.rect(screen, COLOURS.RED, enemy_rect, 3)
        if enemy_rect.collidepoint(mx, my) and mb[0] and not clicked and player_party.members[caster].can_attack() and enemy_info.is_alive():
            framedelay = 5
            enemy_info.damage(player_party.members[caster].attack_damage, player_party.members[caster])
            clicked = True
            player_party.members[caster].attack_animation.update()
            player_party.members[caster].tired = True
            currentaction = MENU.COMBAT_MENU_MODES.MAIN_COMBAT_MENU
    return caster


def defend(caster):  # The defending function where the damage gets halved
    global currentaction, clicked, defending, framedelay
    draw.rect(screen, COLOURS.BUTTONBACK, RECTANGLES.BATTLE_UI.BUTTON_BACKGROUND_FILL, 0)
    draw.rect(screen, COLOURS.BLACK, RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT, 2)
    draw.rect(screen, COLOURS.BLUE, RECTANGLES.BATTLE_UI.CONFIRM_RECT, 2)
    screen.blit(backing, (320, 620))
    screen.blit(confirming, (630, 620))
    if RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT.collidepoint(mx, my):
        draw.rect(screen, COLOURS.BLACK, RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT, 5)
        if mb[0] and not clicked:
            clicked = True
            currentaction = MENU.COMBAT_MENU_MODES.MAIN_COMBAT_MENU
    if RECTANGLES.BATTLE_UI.CONFIRM_RECT.collidepoint(mx, my):
        draw.rect(screen, COLOURS.BLUE, RECTANGLES.BATTLE_UI.CONFIRM_RECT, 5)
        if mb[0] and not clicked and not player_party.members[caster].tired:
            player_party.members[caster].set_defending(True)
            player_party.members[caster].tired = True
            framedelay = 5
            clicked = True
            currentaction = MENU.COMBAT_MENU_MODES.MAIN_COMBAT_MENU
    return caster


def switch(caster):  # Switching between the characters order
    global currentaction, clicked
    draw.rect(screen, COLOURS.BUTTONBACK, RECTANGLES.BATTLE_UI.BUTTON_BACKGROUND_FILL, 0)
    draw.rect(screen, COLOURS.BLACK, RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT, 2)
    screen.blit(backing, (320, 620))
    if RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT.collidepoint(mx, my):
        draw.rect(screen, COLOURS.BLACK, RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT, 5)
        if mb[0] and not clicked:
            clicked = True
            currentaction = MENU.COMBAT_MENU_MODES.MAIN_COMBAT_MENU
    for i, v in enumerate(RECTANGLES.BATTLE_UI.PLAYER_RECTS):
        if not player_party.members[i].tired and caster != i:
            draw.polygon(screen, COLOURS.WHITE, (selectpoly[i]), 2)
        if v.collidepoint(mx, my) and mb[0] and not clicked and not player_party.members[i].tired:
            clicked = True
            currentaction = MENU.COMBAT_MENU_MODES.MAIN_COMBAT_MENU
            return i
    return caster


def enemycast():  # The enemy attacking, It changes depending on what enemy is in the rotation
    global playerturn, nottired, enemyframedelay
    for current_enemy_info in enemy_party.members:
        if enemyframedelay > 0:
            enemyframedelay -= 1
        elif enemyframedelay == 0:
            current_enemy_info.apply_status_effects()
            if current_enemy_info.taunted: # if the enemy is taunted, attack a taunt target
                attacken(current_enemy_info.taunt_target, current_enemy_info.attackDamages[0],
                         current_enemy_info.animations.attack_effect, current_enemy_info)
            else: #otherwise, attack normal target
                if current_enemy_info.enemyType == "grunt" and current_enemy_info.can_attack():
                    target_random(current_enemy_info.attackDamages[0], current_enemy_info.animations.attack_effect, current_enemy_info)
                elif current_enemy_info.enemyType == "tough" and current_enemy_info.can_attack():
                    move = randint(0, 3)
                    if move == 0:
                        target_random(current_enemy_info.attackDamages[1], current_enemy_info.animations.attack_effect, current_enemy_info)
                    else:
                        target_priority(current_enemy_info.attackDamages[0], current_enemy_info.animations.attack_effect, current_enemy_info)
                elif current_enemy_info.can_attack(): # boss and miniboss attack style
                    if current_enemy_info.health > (current_enemy_info.max_health // 2):
                        move = randint(0, 6)
                    else:
                        move = randint(0, 3)
                    if move in [3, 4, 5, 6]:
                        target_random(current_enemy_info.attackDamages[0], current_enemy_info.animations.attack_effect, current_enemy_info)
                    elif move in [2, 1]:
                        target_priority(current_enemy_info.attackDamages[1], current_enemy_info.animations.attack_effect, current_enemy_info)
                    elif move == 0:
                        if current_enemy_info.enemyType == 'miniboss':
                            target_priority(current_enemy_info.attackDamages[1],
                                            current_enemy_info.animations.attack_effect, current_enemy_info)
                        else:
                            attackaoe(current_enemy_info.attackDamages[2], current_enemy_info.animations.attack_effect, current_enemy_info)
                    #screen.blit(enemyanimation[5][0][0], (1080 - 15 * i, 400 - 190 * i))
            if all([not i.can_attack() for i in enemy_party.members]):  # When all the enemies go it becomes the partys turn
                print("-"*10, 'START PLAYER TURN', '-'*10)
                player_party.start_turn()
                enemy_party.clear_taunts()
                playerturn = True
                enemyframedelay = 15

                return playerturn
            enemyframedelay = 15
    return playerturn


def attacken(target, somedmg, animation, enemyInfo):  # This is the main function where an enemy applies his damage to the party member
    screen.blit(animation, (randint(0, 1000), randint(0, 700)))
    if target.defending:  # If the ally is defending then the damage is halved
        # screen.blit(shield1, (325 - 15 * someone, 20 + 190 * someone))
        pass
    target.damage(somedmg)
    enemyInfo.tired = True

    enemynum = enemy_party.get_member_index(enemyInfo)

    screen.blit(enemyInfo.animations.attack, (1080 - 15 * enemynum, 400 - 190 * enemynum))
    display.flip()


def attackaoe(somedmg, animation, enemyInfo):  # The attacking function for the bosses where it deals damage to the entire party
    enemynum = enemy_party.get_member_index(enemyInfo)
    for member in player_party.members:
        screen.blit(animation, (randint(0, 1000), randint(0, 1000)))
        # if yourselection[i].defending:
        #    screen.blit(shield1, (325 - 15 * i, 20 + 190 * i))
        member.damage(somedmg)
    screen.blit(enemyInfo.animations.attack, (1080 - 15 * enemynum, 400 - 190 * enemynum))
    enemyInfo.tired = True


def target_priority(dmg, animation, enemyInfo):  # Prioritizing the party member with the lowest health percentage to attack
    target = min([i for i in player_party.members if i.is_alive()])
    attacken(target, dmg, animation, enemyInfo)


def target_random(dmg, animation, enemyInfo):  # Targeting a random party member to attack
    target = choice([i for i in player_party.members if i.is_alive()])
    attacken(target, dmg, animation, enemyInfo)


def load():  # The loading function
    print("Loading is not implemented yet!")

print("Image cacher loaded %d files with %d hits and %d misses"%(image_cacher.requests, image_cacher.hits, image_cacher.misses))

########################################################################################

# The frames
frame = "Menu"
while frame != "Exit":
    if frame == "Menu":
        frame = menu()
    if frame == "NGame":
        frame = ngame()
    if frame == "Load":
        frame = ngame()
    if frame == "Instructions":
        frame = instructions()
    if frame == "Codes":
        frame = codes.codeSystem()

quit()
