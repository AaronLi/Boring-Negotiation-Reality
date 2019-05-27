from pygame import *
from tkinter import *
from random import *
import pickle, caster, enemy, ability, animation
from constants import *
import math_tools
from lib_cutscene import cutscene, dialog_section

import infoCard

root = Tk()
root.withdraw()
init()

# All our colours


mb = mouse.get_pressed()
mx, my = mouse.get_pos()
playerturn = True  # Global variable dictating whether its the player's turn or the enemies turn
currentCaster = 0  # This is the global variable that we will be using in order to distinguish who on your team is making the move during the players turn
selection = 0  # This is the global variable used for when we're using skills inside the battle function

framedenom = 3  # This is the number we divide by when the attacking animation happens in order to control the speed of the animation
###################################


party = 0  # This is the number of people who are in the party when character selection is happening
screen = display.set_mode(SETTINGS.VIDEO.SCREEN_SIZE, SRCALPHA)  # making appropriate window

display.set_caption("A Boring Negotiation Reality")
ffont = font.Font("basis33.ttf", 20)
titleFont = font.Font('basis33.ttf', 35)
titleFont.set_italic(True)

# use pokemon font

# MUSIC
# mixer.music.load("eo.ogg")
# mixer.music.play(-1)


# charsel stuff
# char=["EY","AR","JH","SS","NN","JF","ED","LN","PS","MB","VL","OY","ZH"] #everyone's characters, represented with initials ,SS,NN,JF,ED,LN,PS,VR,MB,VL,OZ,ZH
selchar = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0]  # This allows us to know if we're selecting characters at the associated positions
focusedCard = 0  # This tells us what our players position is relevant to one another
pplparty = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11]  # This ties together with selchar as well depicting what position the characters we've selected are
pparty = []  # We use this to blit characters profile pictures during cutscenes as well as during character selection

selcurrent = selchar[focusedCard]  # our current selection is the position in selchar

# lib_cutscene shapes and characters speaking

na = image.load("A BNR/hoodhood.png")
na = transform.scale(na, (150, 150))
Vr = image.load("A BNR/vladhead.png")
Vr = transform.scale(Vr, (150, 150))
Al = image.load("A BNR/aaronhead.png")
Al = transform.scale(Al, (150, 150))
KK = image.load("A BNR/kim.png")

# lib_cutscene backgrounds
abattle = image.load("A BNR/abattle.png")
abattle = transform.scale(abattle, (1260, 650))
vbattle = image.load("A BNR/vladbg.png")
vbattle = transform.scale(vbattle, (1260, 650))
kbattle = image.load("A BNR/kimbg.png")
kbattle = transform.scale(kbattle, (1260, 650))

# image loading for the main menu and cutscenes
menu1 = image.load("A BNR/main menu real.png")

# These are all the scenes used during the opening lib_cutscene

# This is a list of all of the area's or backgrounds occurring during the cutscenes that is blit using the cscene function

# cut scene lines
# intermission cut scenes minion, boss,minions, boss separate Vlad's dialogue later
# after battle 1?
tweleve = "We got you!   Tell us who your master is!"
thirteen = "Me me little boy.... All I know is my master's... home is..."
fourteen = "..at the upper regions of Mount Dew..."
fourteenpointfive = "I was hoping to die before I revealed that."
fifteen = "There, you'll meet the immortal bouncer of the Portal, Vlad."

sixteen = "Nnnnyyeeeessss. Ahh at last you come. You have promise. Alas, it is your naive belief that you can save everyone that blinds you. A shame."
seventeen = "Tell us where your master is!"
eighteen = "I do not have the time required nor the desire to indulge you."
# after battle 2

nineteen = "[One of your party members tries to enter the portal, but gets thrown out!]"
twenty = "You! How do we enter the portal?"
twentyone = "You may hold victory in your grasp, but I hold the answers to your progression toward it in mine."
twentytwo = "Would you destroy us both before learning them?"
twentythree = "What does that mean?"
twentyfour = "[One of your party members takes Vlad's severed arm and sticks it through the portal...]"
twentyfive = "[And they disappear!]"
twentysix = "[Seeing this, the rest of the party looks at Vlad...]"
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



sceneback = [[abattle, abattle, abattle],
             [abattle, abattle, abattle, abattle, ],
             [abattle, abattle, abattle, abattle], [vbattle, vbattle, vbattle, vbattle], [vbattle, vbattle, vbattle],
             [vbattle, vbattle, vbattle, vbattle, vbattle, vbattle, vbattle, vbattle],
             [kbattle, kbattle, kbattle, kbattle, kbattle], [kbattle, kbattle, kbattle]]

instructionsPic = image.load(
    "A BNR/help.png")  # The instructions as a single picture to be blit when being called as a function
# order: ER,AR,JH,SS,NN,JF,ED,LN,PS,MB,VL,OZ,ZH
# This is all the characters standing normally that is used during character select as well as during the main game
erikstand = image.load("A BNR/stands/erik stand.png")
alizastand = image.load("A BNR/stands/aliza stand.png")
juliestand = image.load("A BNR/stands/julie stand.png")
supstand = image.load("A BNR/stands/supreet stand.png")
natstand = image.load("A BNR/stands/nat stand.png")
janstand = image.load("A BNR/stands/jan stand.png")
emilystand = image.load("A BNR/stands/emily stand.png")
linhstand = image.load("A BNR/stands/linh stand.png")
printerstand = image.load("A BNR/stands/priyonto stand.png")
# vladstand was cut due to time constraints
minyastand = image.load("A BNR/stands/minya stand.png")
vivstand = image.load("A BNR/stands/viv stand.png")
ogustand = image.load("A BNR/stands/ogu stand.png")
zakstand = image.load("A BNR/stands/zak stand.png")

# The following is all attacking animations for each character that are also recycled for skill animations


# Each characters final frame in their skill animations that distinguishes between their attack and skill
erikskill = image.load('game sprites/erik skill.png')
alizaskill = image.load('game sprites/aliza skill.png')
julieskill = image.load('game sprites/julie skill.png')
supreetskill = image.load('game sprites/supreet skill.png')
natskill = image.load('game sprites/nat skill.png')
janskill = image.load('game sprites/jan skill.png')
emilyskill = image.load('game sprites/emily skill.png')
linhskill = image.load('game sprites/linh skill.png')
priyontoskill = image.load('game sprites/priyonto skill.png')
minyaskill = image.load('game sprites/minya skill.png')
vivskill = image.load('game sprites/viv skill.png')
oguskill = image.load('game sprites/ogu skill.png')
zakskill = image.load('game sprites/zak skill.png')

# This is all of the character's greyed out or dead forms
erikded = image.load('game sprites/erik ded.png')
julieded = image.load('game sprites/julie ded.png')
alizaded = image.load('game sprites/aliza ded.png')
supreetded = image.load('game sprites/supreet ded.png')
natded = image.load('game sprites/nat ded.png')
janded = image.load('game sprites/jan ded.png')
emilyded = image.load('game sprites/emily ded.png')
linhded = image.load('game sprites/linh ded.png')
priyontoded = image.load('game sprites/priyonto ded.png')
minyaded = image.load('game sprites/minya ded.png')
vivded = image.load('game sprites/viv ded.png')
oguded = image.load('game sprites/ogu ded.png')
zakded = image.load('game sprites/zak ded.png')

# These are sprites that blit when the character is damaged
erikow = image.load('game sprites/erik ow.png')
julieow = image.load('game sprites/julie ow.png')
alizaow = image.load('game sprites/aliza ow.png')
supreetow = image.load('game sprites/supreet ow.png')
natow = image.load('game sprites/nat ow.png')
janow = image.load('game sprites/jan ow.png')
emilyow = image.load('game sprites/emily ow.png')
linhow = image.load('game sprites/linh ow.png')
priyontoow = image.load('game sprites/priyonto ow.png')
minyaow = image.load('game sprites/minya ow.png')
vivow = image.load('game sprites/viv ow.png')
oguow = image.load('game sprites/ogu ow.png')
zakow = image.load('game sprites/zak ow.png')

# All the battle portraits that blit when the character has died
erikdedportrait = image.load('game sprites/battle portraits/erik portraitded.png')
juliededportrait = image.load('game sprites/battle portraits/julie portraitded.png')
alizadedportrait = image.load('game sprites/battle portraits/aliza portraitded.png')
minyadedportrait = image.load('game sprites/battle portraits/minya portraitded.png')
supreetdedportrait = image.load('game sprites/battle portraits/supreet portraitded.png')
natdedportrait = image.load('game sprites/battle portraits/natalie portraitded.png')
jandedportrait = image.load('game sprites/battle portraits/jan portraitded.png')
vivdedportrait = image.load('game sprites/battle portraits/viv portraitded.png')
ogudedportrait = image.load('game sprites/battle portraits/ogu portraitded.png')
zakdedportrait = image.load('game sprites/battle portraits/zak portraitded.png')
emilydedportrait = image.load('game sprites/battle portraits/emily portraitded.png')
linhdedportrait = image.load('game sprites/battle portraits/linh portraitded.png')
priyontodedportrait = image.load('game sprites/battle portraits/priyonto portraitded.png')

# Attacking animations for Erik
erikAnimation = animation.Animation([image.load("game sprites/erik %d.png"%(i)) for i in range(1,6)], 0.4, 60)
erikAttackSprites = erikAnimation.sprites.copy()
erikAttackSprites.insert(3,image.load("game sprites/erik skill.png"))
erikSpellAnimation = animation.Animation(erikAttackSprites, 0.5, 60)
# Attacking animations for Aliza
alizaAnimation = animation.Animation([image.load("game sprites/aliza %d.png"%i) for i in range(1,6)], 0.4, 60)
alizaSpellAnimation = animation.Animation(alizaAnimation.sprites+[alizaskill], 0.5, 60)
# Attacking animations for Julie
julieAnimation = animation.Animation([image.load("game sprites/julie %d.png"%i) for i in range(1,6)], 0.4, 60)
julieSpellAnimation = animation.Animation(julieAnimation.sprites+[julieskill], 0.5, 60)
# Attacking animations for Supreet
supreetAnimation = animation.Animation([image.load("game sprites/supreet %d.png"%i) for i in range(1,6)], 0.4, 60)
supreetSpellAnimation = animation.Animation(supreetAnimation.sprites+[supreetskill], 0.5, 60)
# Attacking animations for Natalie
natAnimation = animation.Animation([image.load("game sprites/nat %d.png"%i) for i in range(1,6)], 0.4, 60)
natAttackSprites = natAnimation.sprites.copy()
natAttackSprites.insert(3,image.load("game sprites/nat skill.png"))
natSpellAnimation = animation.Animation(natAttackSprites, 0.5, 60)
# Attacking animations for Jan
janAnimation = animation.Animation([image.load("game sprites/jan %d.png"%i) for i in range(1,6)], 0.4, 60)
janSpellAnimation = animation.Animation(janAnimation.sprites+[janskill], 0.5, 60)
# Attacking animations for Emily
emilyAnimation = animation.Animation([image.load("game sprites/emily %d.png"%i) for i in range(1,5)], 0.4, 60)
emilySpellAnimation = animation.Animation(emilyAnimation.sprites+[emilyskill], 0.5, 60)
# Attacking animations for Linh
linhAnimation = animation.Animation([image.load("game sprites/linh %d.png"%i) for i in range(1,5)], 0.4, 60)
linhSpellAnimation = animation.Animation(linhAnimation.sprites+[linhskill], 0.5, 60)
# Attacking animations for Priyonto
priyontoAnimation = animation.Animation([image.load("game sprites/priyonto %d.png"%i) for i in range(1,6)], 0.4, 60)
priyontoSpellAnimation = animation.Animation(priyontoAnimation.sprites+[priyontoskill], 0.5, 60)
# Attacking animations for Minya
minyaAnimation = animation.Animation([image.load("game sprites/minya %d.png"%i) for i in range(1,4)], 0.4, 60)
minyaSpellAnimation = animation.Animation(minyaAnimation.sprites+[minyaskill], 0.5, 60)
# Attacking animations for Vivianne
vivAnimation = animation.Animation([image.load("game sprites/viv %d.png"%i) for i in range(1,6)], 0.4, 60)
vivSpellAnimation = animation.Animation(vivAnimation.sprites+[vivskill], 0.5, 60)
# Attacking animations for Oguzhan
oguAnimation = animation.Animation([image.load("game sprites/ogu %d.png"%i) for i in range(1,6)], 0.4, 60)
oguAttackSprites = oguAnimation.sprites.copy()
oguAttackSprites.insert(3,image.load("game sprites/ogu skill.png"))
oguSpellAnimation = animation.Animation(oguAttackSprites, 0.5, 60)
# Attacking animations for Zak
zakAnimation = animation.Animation([image.load("game sprites/zak %d.png"%i) for i in range(1,6)], 0.4, 60)
zakSpellAnimation = animation.Animation(zakAnimation.sprites+[zakskill], 0.5, 60)
clicked = False
# name tags

juvivPics = [(image.load("A BNR/CODESYS/juviv" + str(i) + ".png")) for i in
             range(10)]  # list of the pictures for the code "juviv"
swankPics = [(image.load("A BNR/CODESYS/swank" + str(i) + ".png")) for i in
             range(10)]  # same as above, except for different codes
corgiPics = [(image.load("A BNR/CODESYS/corgi" + str(i) + ".png")) for i in range(10)]
punzPics = [(image.load("A BNR/CODESYS/punz" + str(i) + ".png")) for i in range(10)]
naePics = [(image.load("A BNR/CODESYS/nae" + str(i) + ".png")) for i in range(10)]
guckPics = [(image.load("A BNR/CODESYS/guck" + str(i) + ".png")) for i in range(10)]

# selected for the party pics
# if the person is first in the party, they get the first spot and so forth...
# These also double up as the portraits for the characters during battles
erikportrait = image.load("A BNR/battle/erik portrait.png")
erikprof = transform.smoothscale(erikportrait, (100, 100))
alizaportrait = image.load("A BNR/battle/aliza portrait.png")
alizaprof = transform.smoothscale(alizaportrait, (100, 100))
julieportrait = image.load("A BNR/battle/julie portrait.png")
julieprof = transform.smoothscale(julieportrait, (100, 100))
supportrait = image.load("A BNR/battle/supreet portrait.png")
supprof = transform.smoothscale(supportrait, (100, 100))
natportrait = image.load("A BNR/battle/natalie portrait.png")
natprof = transform.smoothscale(natportrait, (100, 100))
janportrait = image.load("A BNR/battle/jan portrait.png")
janprof = transform.smoothscale(janportrait, (100, 100))
emilyportrait = image.load("A BNR/battle/emily portrait.png")
emilyprof = transform.smoothscale(emilyportrait, (100, 100))
linhportrait = image.load("A BNR/battle/linh portrait.png")
linhprof = transform.smoothscale(linhportrait, (100, 100))
printerportrait = image.load("A BNR/battle/priyonto portrait.png")
printerprof = transform.smoothscale(printerportrait, (100, 100))
minyaportrait = image.load("A BNR/battle/minya portrait.png")
minyaprof = transform.smoothscale(minyaportrait, (100, 100))
vivportrait = image.load("A BNR/battle/viv portrait.png")
vivprof = transform.smoothscale(vivportrait, (100, 100))
oguportrait = image.load("A BNR/battle/ogu portrait.png")
oguprof = transform.smoothscale(oguportrait, (100, 100))
zakportrait = image.load("A BNR/battle/zak portrait.png")
zakprof = transform.smoothscale(zakportrait, (100, 100))

# All the profile pictures for each character for when they're speaking
profs = [erikprof, alizaprof, julieprof, supprof, natprof, janprof, emilyprof, linhprof, printerprof, minyaprof,
         vivprof, oguprof, zakprof]
background = image.load("A BNR/cave.jpg")  # The original background for the game
fire = image.load("FIREBALL.png")  # An enemies attacking animation
ice = image.load("icestar.png")  # An enemies attacking animation
lightning = image.load("lightning.png")  # An enemies attacking animations
dumpling = image.load("dumpling.png")
diamond = image.load("diamond.png")
music = image.load("musicnotes.png")

# All the enemies sprites that need to be used
doge = image.load('game sprites/doge.png')
dogeow = image.load('game sprites/dogeow.png')
doge1 = image.load('game sprites/doge1.png')
dogeow1 = image.load('game sprites/dogeow1.png')
dogeow2 = image.load('game sprites/dogeow2.png')
aaron = image.load('game sprites/aaron.png')
aaronow = image.load('game sprites/aaronow.png')
aaron1 = image.load('game sprites/aaron1.png')
kim = image.load('game sprites/kim.png')
kimow = image.load('game sprites/kimow.png')
kim1 = image.load('game sprites/kim1.png')
pepe = image.load('game sprites/pepe.png')
pepeow = image.load('game sprites/pepeow.png')
pepe1 = image.load('game sprites/pepe1.png')
pepeow1 = image.load('game sprites/pepeow1.png')
pepeow2 = image.load('game sprites/pepeow2.png')
spinner = image.load('game sprites/spinner.png')
spinnerow = image.load('game sprites/spinnerow.png')
spinner1 = image.load('game sprites/spinner1.png')
spinnerow1 = image.load('game sprites/spinnerow1.png')
spinnerow2 = image.load('game sprites/spinnerow2.png')
vlad = image.load('game sprites/vlad stand.png')
vladow = image.load('game sprites/vlad ow.png')
vlad1 = image.load('game sprites/vlad1.png')

# All of the characters in battle animations compiled into a 3d list
animations = [
    [[erikstand], [], [], [erikow], [erikded]],
    [[alizastand], [], [], [alizaow],
     [alizaded]],
    [[juliestand], [], [], [julieow],
     [julieded]],
    [[supstand], [], [],
     [supreetow], [supreetded]],
    [[natstand], [], [], [natow], [natded]],
    [[janstand], [], [], [janow], [janded]],
    [[emilystand], [], [], [emilyow], [emilyded]],
    [[linhstand], [], [], [linhow], [linhded]],
    [[printerstand], [],
     [], [priyontoow], [priyontoded]],
    [[minyastand], [], [], [minyaow], [minyaded]],
    [[vivstand], [], [], [vivow], [vivded]],
    [[ogustand], [], [], [oguow], [oguded]],
    [[zakstand], [], [], [zakow], [zakded]]
]

# Same as above except for enemies
enemyanimation = [
    [[doge], [doge1], [dogeow], [dogeow, dogeow1, dogeow2]],
    [[pepe], [pepe1], [pepeow], [pepeow, pepeow1, pepeow2]],
    [[spinner], [spinner1], [spinnerow], [spinnerow, spinnerow1, spinnerow2]],
    [[aaron], [aaron1], [aaronow]],
    [[vlad], [vlad1], [vladow]],
    [[kim], [kim1], [kimow]]
]
# Pokemon font
font = font.SysFont("Pokemon GB", 100)
# The following is all for the code system
bgRect = Rect(0, 0, 1260, 750)
bg = image.load("A BNR/CODESYS/code screen.png")
invalidCode = image.load("A BNR/CODESYS/invalid.png")  # Code system image if an invalid code is enterred
validCode = image.load("A BNR/CODESYS/valid.png")  # Same as above except for other pictures
codeFace = image.load("A BNR/CODESYS/code scr face0.png")
codeIMG = image.load("A BNR/CODESYS/code0.png")
boisIMG = image.load("A BNR/CODESYS/bois0.png")
wahIMG = image.load("A BNR/CODESYS/wah.png")
cheatIMG = image.load("A BNR/CODESYS/cheat.png")

# More needed things for the coding system
recta = Surface((555, 170), SRCALPHA)
bar = Rect(0, 0, 555, 170)
draw.rect(screen, (255, 255, 255), bgRect)


# List of all the scenes
scene = [[tweleve, thirteen, fourteen, fourteenpointfive, fifteen], [sixteen, seventeen, eighteen],
         [nineteen, twenty, twentyone, twentytwo, twentythree, twentyfour, twentyfive, twentysix],
         [twentyseven, twentyeight, twentynine, thirtyone, thirtytwo], [thirtythree, thirtyfour, thirtyfive]]
scene = [[j + (' ' * 7) for j in i] for i in scene]
see = 0

# Confirm and back pictures
confirming = image.load("confirm.png")
backing = image.load("back.png")
# lets be lazy and let the only party leader speak.
# scenee=[[na,na,na,na,na,na,na,na],[Ey,Al,Al],[Ey,Al,Al,Vr,Ey,Vr],[na,Ey,Vr,Ey,na,na,na],[na,Ey,rr,rr,rr],[rr,Ey,na]]



# The portraits either ded or alive
battleportraits = [[erikportrait, erikdedportrait], [alizaportrait, alizadedportrait],
                   [julieportrait, juliededportrait],
                   [supportrait, supreetdedportrait], [natportrait, natdedportrait], [janportrait, jandedportrait],
                   [emilyportrait, emilydedportrait], [linhportrait, linhdedportrait],
                   [printerportrait, priyontodedportrait],
                   [minyaportrait, minyadedportrait], [vivportrait, vivdedportrait], [oguportrait, ogudedportrait],
                   [zakportrait, zakdedportrait]]
selectnums = []  # The numbers in the ordered list that each specific character is associated with from your selection

yourselection = []  # A 2D list with all of the selected characters stats
skilllist = []  # Another 2D list that has all of the skills for each character
abilitybutton = []  # These are all the ability button names that i load in depending on the characters you select
abilitydesc = []  # Same as above except descriptions for those abilities
framedelay = -1  # This delays each of your characters moves to make for a smoother transition
playAbilityAnimation = False
enemyframedelay = 15  # The enemys delay in order to be a little slower
########################################### UI STUFF
selectpoly = [[(380, 30), (360, 10), (400, 10)], [(375, 220), (355, 200), (395, 200)], [(355, 425), (335, 405), (
375, 405)]]  # Polygons that blit over your current character or when you're switching characters

values = ["attack", "skills", "defend", "switch"]  # The buttons values to be associated to functions
# Shiled images for when you're defending
shield0 = image.load("shield0.png")
shield1 = image.load("shield1.png")
shield2 = image.load("shield2.png")
defendAnimation = animation.Animation([shield2, shield1, shield0, shield0, shield0, shield0, shield0, shield1, shield2],0.3,60)
# main menu rectangles


positions = [0, 1, 2]  # The enemies or allys postions to be used in some functions

# All the enemy rounds in order of how they will be coming in a 3D list
enemyrotations = [
    [enemy.Enemy("grunt", 1000, 250), enemy.Enemy("tough", 1500, 150, 450), enemy.Enemy("grunt", 1000, 250)],
    [enemy.Enemy("tough", 2500, 300, 600), enemy.Enemy("grunt", 2000, 400), enemy.Enemy("tough", 2500, 300, 600)],
    [enemy.Enemy("tough", 2500, 300, 600), enemy.Enemy("tough", 2500, 300, 600),
     enemy.Enemy("miniboss", 4000, 1000, 750, 500)],
    [enemy.Enemy("grunt", 2500, 500), enemy.Enemy("aaron", 6000, 800, 1500, 600), enemy.Enemy("grunt", 2500, 500)],
    [enemy.Enemy("tough", 3000, 400, 650), enemy.Enemy("tough", 3000, 400, 650), enemy.Enemy("tough", 3000, 400, 650)],
    [enemy.Enemy("tough", 3500, 550, 650), enemy.Enemy("grunt", 3000, 550), enemy.Enemy("grunt", 3000, 550)],
    [enemy.Enemy("miniboss", 3800, 800, 600, 500), enemy.Enemy("miniboss", 3800, 800, 600, 500),
     enemy.Enemy("grunt", 1500, 400)],
    [enemy.Enemy("tough", 3500, 550, 650), enemy.Enemy("vlad", 8000, 1000, 1700, 750),
     enemy.Enemy("tough", 3500, 550, 650)],
    [enemy.Enemy("grunt", 3000, 800), enemy.Enemy("grunt", 3000, 800), enemy.Enemy("grunt", 3000, 800)],
    [enemy.Enemy("tough", 2500, 550, 650), enemy.Enemy("tough", 2500, 550, 650), enemy.Enemy("tough", 2500, 550, 650)],
    [enemy.Enemy("miniboss", 3600, 750, 600, 500), enemy.Enemy("miniboss", 3600, 750, 600, 500),
     enemy.Enemy("miniboss", 3600, 750, 600, 500)],
    [enemy.Enemy("miniboss", 2500, 800, 600, 500), enemy.Enemy("kim", 10000, 1100, 650, 800),
     enemy.Enemy("miniboss", 2500, 800, 600, 500)]
]
enemieselection = []  # 2D list that has the current enemies inside of it to be blitted and use their stats
planneddamage = 0  # When an enemy is attacking
currentattacker = -1  # This is used for blitting the current attacker
currentattackertime = 0  # This is used to regulate frames when attacking
currentaction = ""  # This depicts what function is being used (Skills,Attacking,Switching,Defending or none)
currentlyCasting = -1  # Same situation with the current attacker
scenenum = 0  # This is which scene is happening inside of the cscene function
battlenum = 0  # This is which round you are on
enemyrevoked = [False, False, False]  # Another list for supreets revoke ability forcing enemies to skip their turn
taunted = [False, False, False]  # Taunting enemies to attack a specific person
beforehealth = -1  # Another variable for an ability (jan's flame shell)
beforehealthtarget = -1  # Also being used for jan's flame shell

deathScreen = image.load("A BNR/deathScreen.png")

running = True  # boolean variable

direction = 0
scrollMode = True
tempBirbs = image.load('birbs.png').convert() #TODO: remove when I have gourd art
def charsel(
        clicked):  # This is the character selection function for choosing which characters will be in your party and you'll play the game with
    global focusedCard, party, skilllist, abilitybutton, abilitydesc, direction, scrollMode  # hee is index of the character that is currently selected in all of the lists
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    keys = key.get_pressed()
    screen.blit(tempBirbs,(0,0))
    draw.rect(screen, COLOURS.BLACK, (305 - infoCards[int(focusedCard)].graphic.get_width() // 2, 0, infoCards[int(focusedCard)].graphic.get_width() + 10, 755))
    rosterRect = Surface((560, 715), SRCALPHA)
    rosterRect.fill(COLOURS.GREY_TRANSLUCENT)
    screen.blit(rosterRect, (680, 20))
    for i in range(min(int(focusedCard)+3, len(infoCards)-1), int(focusedCard), -1):
        v = infoCards[i]
        blitImage = transform.scale(v.graphic, (int((2 / max(abs(focusedCard - i) + 2, 2)) * v.graphic.get_width()),
                                                int((2 / max(abs(focusedCard - i) + 2, 2)) * v.graphic.get_height())))
        maskImage = Surface(blitImage.get_size(), SRCALPHA)
        maskImage.fill((0, 0, 0, min(100 * abs(focusedCard - i), 255)))
        screen.blit(blitImage, (310 - blitImage.get_width() // 2, ((377 - v.graphic.get_height() // 2) + ((i - focusedCard) * blitImage.get_height()))))
        screen.blit(maskImage, (310 - blitImage.get_width() // 2, ((377 - v.graphic.get_height() // 2) + ((i - focusedCard) * blitImage.get_height()))))
    for i in range(max(int(focusedCard)-3, 0), int(focusedCard+1)):
        v = infoCards[i]
        blitImage = transform.scale(v.graphic, (int((2 / max(abs(focusedCard - i) + 2, 2)) * v.graphic.get_width()),
                                                int((2 / max(abs(focusedCard - i) + 2, 2)) * v.graphic.get_height())))#.convert_alpha()
        maskImage = Surface(blitImage.get_size(), SRCALPHA)
        maskImage.fill((0, 0, 0, min(100 * abs(focusedCard - i), 255)))
        screen.blit(blitImage, (310 - blitImage.get_width() // 2, ((377 - v.graphic.get_height() // 2) + ((i - focusedCard) * blitImage.get_height()))))
        screen.blit(maskImage, (310 - blitImage.get_width() // 2, ((377 - v.graphic.get_height() // 2) + ((i - focusedCard) * blitImage.get_height()))))

    if direction!=0:
        focusedCard=round(focusedCard + direction, 3)
        if abs(focusedCard-int(focusedCard))<abs(direction)-0.0001:
            direction = 0
            focusedCard = int(focusedCard)
    else:
        if float(focusedCard).is_integer() and infoCards[int(focusedCard)].characterName.lower() not in [i.name.lower() for i in yourselection] and len(yourselection)<3 and infoCards[int(focusedCard)].workingName.lower() not in [i.name.lower() for i in yourselection]:
            focusedCard = int(focusedCard)
            draw.polygon(screen, COLOURS.WHITE, [
                (320 + infoCards[focusedCard].graphic.get_width() // 2, 337),
                (370 + infoCards[focusedCard].graphic.get_width() // 2, 367),
                (320 + infoCards[focusedCard].graphic.get_width() // 2, 397),

            ])
            if Rect(320 + infoCards[focusedCard].graphic.get_width() // 2, 337, 50, 60).collidepoint(mx, my) or keys[K_RETURN] or keys[K_RIGHT] or keys[K_d]:
                draw.polygon(screen, COLOURS.GREY, [
                    (320 + infoCards[focusedCard].graphic.get_width() // 2, 337),
                    (370 + infoCards[focusedCard].graphic.get_width() // 2, 367),
                    (320 + infoCards[focusedCard].graphic.get_width() // 2, 397),

                ])
                if mb[0] and not clicked and len(pparty)<3 or keys[K_RETURN] or keys[K_RIGHT] or keys[K_d]:
                    yourselection.append(stats[focusedCard])
                    pparty.append(profs[focusedCard])
                    selectnums.append(focusedCard)
                    clicked = True
    titleFont.set_italic(True)
    myPartyText = titleFont.render("My Team", False, COLOURS.WHITE)
    screen.blit(myPartyText, (692, 26))
    for i,v in enumerate([i.name.lower() for i in yourselection]):
        for j in infoCards:
            if j.characterName.lower() == v  or v == j.workingName.lower():
                smallCard = j.graphic.subsurface([0,0,500,110])
                screen.blit(smallCard,(690, i*(smallCard.get_height()+2)+60))
                delRect = Rect(695+smallCard.get_width(), i*(smallCard.get_height()+2)+60, 40, smallCard.get_height())
                if delRect.collidepoint(mx, my):
                    draw.rect(screen, (200, 0, 0), delRect)
                    if(mb[0] and not clicked):
                        del yourselection[i]
                        del pparty[i]
                        del selectnums[i]
                        clicked = True
                else:
                    draw.rect(screen, (255,0,0), delRect)
                draw.line(screen, COLOURS.WHITE, (delRect.centerx-10, delRect.centery-10), (delRect.centerx+10, delRect.centery+10), 2)
                draw.line(screen, COLOURS.WHITE, (delRect.centerx - 10, delRect.centery + 10), (delRect.centerx + 10, delRect.centery - 10), 2)
    if (keys[K_a] or keys[K_LEFT] or keys[K_BACKSPACE]) and not clicked:
        for i,v in enumerate(yourselection):
            if (infoCards[int(focusedCard)].workingName.lower() == v.name.lower() or infoCards[int(focusedCard)].characterName.lower() == v.name.lower()):
                    clicked = True
                    del yourselection[i]
                    del pparty[i]
                    del selectnums[i]
        clicked = True
    if len(yourselection)>0:
        if len(yourselection)==3:
            draw.rect(screen, COLOURS.GREEN, (690, 675, 540, 50))
            if Rect(690, 675, 540, 50).collidepoint(mx, my):
                draw.rect(screen, (0, 200, 0), (690, 675, 540, 50))
                if(mb[0] and not clicked):
                    for i in infoCards:
                        if i.characterName.lower() == yourselection[0].name.lower() or i.workingName.lower() == yourselection[0].name.lower():
                            pl = i.portrait
                            plprof = i.profile
                    skilllist = [yourselection[0].abilities, yourselection[1].abilities, yourselection[2].abilities]  # Appending the necessary values and images for our abilities/skills
                    abilitybutton = [[image.load("ATTACKS/" + i.working_name + ".png") for i in skilllist[j]] for j in
                                     range(3)]
                    abilitydesc = [[image.load("DESCS/" + i.working_name + ".png") for i in skilllist[j]] for j in
                                   range(3)]
                    clicked = True
                    cutscene.load_from_file('lib_cutscene/Cutscene1.json', plprof).show(screen)
                    battle(background, battle(background, battle(background, 0)))
                    cutscene.load_from_file('lib_cutscene/Cutscene2.json', plprof).show(screen)
                    battle(background, 3)
                    cscene(clicked, 2, pl, plprof)
                    battle(background, battle(background, battle(background, 4)))
                    cscene(clicked, 3, pl, plprof)
                    battle(background, 7)
                    cscene(clicked, 4, pl, plprof)
                    battle(background, battle(background, battle(background, 8)))
                    cscene(clicked, 5, pl, plprof)
                    battle(background, 11)
                    cscene(clicked, 6, pl, plprof)
                    quit()

        else:
            draw.rect(screen, COLOURS.RED, (690, 675, 540, 50))
        titleFont.set_italic(False)
        buttonText = titleFont.render("Start %d/3 >"%len(yourselection), True, (255, 255, 255))
        screen.blit(buttonText, (1220-buttonText.get_width(), 700-buttonText.get_height()//2))
    if (not clicked) and scrollMode:
        if(focusedCard<len(infoCards)-1):
            if (mb[0] and my>screen.get_height()//2) or keys[K_DOWN] or keys[K_s]:
                direction = 0.03
        if(focusedCard>0):
            if (mb[0] and my<screen.get_height()//2) or keys[K_UP] or keys[K_w]:
                direction = -0.03
    #TODO: Main Mengyu
    return clicked



def cscene(clicked, scenenum, pl,
           plprof):  # clicked is whether or not is selected, scenenum is which scene is selected,
    # and pl and plprof are the party leader pics
    global scene

    clock = time.Clock()
    sceneprof = [ [plprof, Al, Al, Al], [Vr, plprof, Vr],
                 [na, plprof, Vr, Vr, plprof, na, na, na], [na, plprof, KK, KK, KK],
                 [KK, plprof, na]]  # profile picture order for the dialogue

    for j in range(len(scene[scenenum])):  # for each scene presented
        dia = (scene[scenenum][j])  # index of the line of dialogue

        screen.blit(sceneback[scenenum][j], (0, 0))
        if (sceneback[scenenum][j]) == abattle or (sceneback[scenenum][j]) == vbattle or (
        sceneback[scenenum][j]) == kbattle:
            # For the scenes with the minibosses...
            screen.blit(pl, (200, 250))  # insert the party leader
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
    clockity= time.Clock()
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
        display.flip()
        clockity.tick(60)
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


# Secret code system related functions
def juvivCode(frame, pics):  # starts the Julie-Vivianne dialogue
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                frame = 0  # if you press x-button, it also goes back to main screen and frame resets
                running = False
            if evnt.type == KEYDOWN:
                if evnt.key == K_RIGHT:  # if you press right key, frame goes up one
                    frame += 1  # goes to the next image
                    if frame == 10:  # if you go up to the last image, it goes back to the main screen
                        frame = 0  # frame resets to 0 for the next time you enter that code
                        return
                if evnt.key == K_LEFT:  # if you press left, frame goes down one (goes back)
                    if frame > 0:  # as long as frame is greater than 0. prevents a crash
                        frame -= 1
        screen.blit(pics[frame], (0, 0))
        display.flip()
    return


def swankCode(frame, pics):
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                frame = 0
                running = False
            if evnt.type == KEYDOWN:
                if evnt.key == K_RIGHT:
                    frame += 1
                    if frame == 10:
                        frame = 0
                        return
                if evnt.key == K_LEFT:
                    if frame > 0:
                        frame -= 1
        screen.blit(pics[frame], (0, 0))
        display.flip()
    return


def corgiCode(frame, pics):
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                frame = 0
                running = False
            if evnt.type == KEYDOWN:
                if evnt.key == K_RIGHT:
                    frame += 1
                    if frame == 10:
                        frame = 0
                        return
                if evnt.key == K_LEFT:
                    if frame > 0:
                        frame -= 1
        screen.blit(pics[frame], (0, 0))
        display.flip()
    return


def punzCode(frame, pics):
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                frame = 0
                running = False
            if evnt.type == KEYDOWN:
                if evnt.key == K_RIGHT:
                    frame += 1
                    if frame == 10:
                        frame = 0
                        return
                if evnt.key == K_LEFT:
                    if frame > 0:
                        frame -= 1
        screen.blit(pics[frame], (0, 0))
        display.flip()
    return


def naeCode(frame, pics):
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                frame = 0
                running = False
            if evnt.type == KEYDOWN:
                if evnt.key == K_RIGHT:
                    frame += 1
                    if frame == 10:
                        frame = 0
                        return
                if evnt.key == K_LEFT:
                    if frame > 0:
                        frame -= 1
        screen.blit(pics[frame], (0, 0))
        display.flip()


def guckCode(frame, pics):
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                frame = 0
                running = False
            if evnt.type == KEYDOWN:
                if evnt.key == K_RIGHT:
                    frame += 1
                    if frame == 10:
                        frame = 0
                        return
                if evnt.key == K_LEFT:
                    if frame > 0:
                        frame -= 1
        screen.blit(pics[frame], (0, 0))
        display.flip()


def codeSystem():  # The code system
    mb = mouse.get_pressed()
    mx, my = mouse.get_pos()
    frame = 0
    screen.blit(bg, (0, 0))
    screen.blit(validCode, (550, 515))
    screen.blit(codeFace, (235, 475))
    start = screen.copy()  # an image of what the screen initially looks like
    screenstuff = []  # this list will contain the screenshots, Erik and I worked on this idea together
    code = ""  # name is what you type out. currently, it's blank
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
                return "Menu"
            if evt.type == KEYDOWN:
                screen.blit(start, (0, 0))
                if len(code) < 5:  # prevents the user from entering codes longer than 5 characters
                    if evt.unicode.isalpha():  # unicode renders what keys are pressed
                        code += evt.unicode  # adds the unicode to name, displays what you type
                        if len(screenstuff) < 5:  # if the list has less than 5 pictures
                            back = screen.copy()
                            screenstuff.append(back)  # adds that capture to the list

                if evt.key == K_BACKSPACE:
                    code = code[:-1]  # backspace removes the last letter that was typed
                    if len(screenstuff) > 0:  # as long as the list has at least one picture, it removes the latest
                        screenstuff.pop()
                    elif len(
                            screenstuff) < 1:  # when the list only has 1 image left (AKA backspacing with only one letter left)
                        screen.blit(start, (0, 0))  # it will go back to it's original appearance

                elif evt.key == K_RETURN:  # if you press enter, here we will check what the user entered
                    screenstuff = []
                    screen.blit(start,
                                (0, 0))  # when you press enter, the screen goes back to it's original appearance
                    if code == "code":  # if you entered the right code (code=right code) something will happen!
                        screen.blit(codeIMG, (0, 0))

                    elif code == "bois":
                        screen.blit(boisIMG, (0, 0))

                    elif code == "wah":
                        screen.blit(wahIMG, (0, 0))

                    elif code == "cheat":
                        screen.blit(cheatIMG, (0, 0))

                    elif code == "juviv":
                        juvivCode(frame, juvivPics)  # runs a new function to determine what will happen
                        screen.blit(start, (0, 0))  # once function is done, blits this image again
                        display.flip()

                    elif code == "swank":
                        swankCode(frame, swankPics)
                        screen.blit(start, (0, 0))
                        display.flip()

                    elif code == "corgi":
                        corgiCode(frame, corgiPics)
                        screen.blit(start, (0, 0))
                        display.flip()

                    elif code == "punz":
                        punzCode(frame, punzPics)
                        screen.blit(start, (0, 0))
                        display.flip()

                    elif code == "nae":
                        naeCode(frame, naePics)
                        screen.blit(start, (0, 0))
                        display.flip()

                    elif code == "guck":
                        guckCode(frame, guckPics)
                        screen.blit(start, (0, 0))
                        display.flip()

                    elif code == "bye":
                        quit()
                        running = False

                    else:  # there was the issue where if you pressed enter even if nothing was typed
                        if code != "":  # it would read it as "invalid", because techincally code="" also means code!=right code
                            screen.blit(invalidCode,
                                        (550, 515))  # this makes sure it does not read it as incorrect when it is blank

                    code = ""  # after you press enter, code disappears

        if len(screenstuff) > 0:
            screen.blit(screenstuff[len(screenstuff) - 1], (0, 0))  # blit the latest image in the list onto the screen

        draw.rect(recta, (0, 0, 0, 0), bar)
        text = font.render(code, True, (0, 0, 0))
        recta.blit(text, (0, 50))
        screen.blit(recta, (350, 250))

        display.flip()
    return "Menu"


##########################################################################
def backstab(target, caster, casters, enemies):  # Defining all the skills that are used with damage and heals and other effects for skills. Enemy or Ally rectangles are drawn depending on who the skill targets
    enemies[target].damage(casters[caster].attack_damage*2, casters[caster])

def silentstrike(target, caster, casters, enemies):
    casters[caster].dodging = True # TODO: make a property "targetable"

def execute(target, caster, casters, enemies):
    enemies[target].damage((300 + (min(casters[caster].health-300, 400 * (3-len([i for i in enemies if i.is_alive()]))))), casters[caster])

def lightningbolt(target, caster, casters, enemies):
    enemies[target].damage(300+100**(1+(randint(0,5)/10)), casters[caster])


def lightningcharge(target, caster, casters, enemies):
    if casters[caster].get_special_stat("lightningCharges") < 5:
        yourselection[currentCaster].modify_special_stat("lightningCharges",1)
    else:
        return 1
def lightningrelease(target, caster, casters, enemies):
    if yourselection[currentCaster].get_special_stat('lightningCharges') >= 5:
        for j in range(3):
            enemies[j].damage(1200, casters[caster]) #TODO: make sure multiplier is applied evenly
    else:
        enemies[target].damage(200+250*yourselection[currentCaster].get_special_stat("lightningCharges"), casters[caster])
    casters[caster].set_special_stat('lightningCharges',0)

def herbsandpoultices(target, caster, casters, enemies):
    casters[target].heal(900 if target==caster else 500)

def slay(target, caster, casters, enemies):
            if yourselection[currentCaster].mana < min(300 + 100 * yourselection[currentCaster].get_special_stat("slayCounter"), 1200):
                return 1
            enemies[target].damage(300 + 100 * yourselection[currentCaster].get_special_stat('slayCounter'), casters[caster])
            yourselection[currentCaster].mana -= min(300 + 100 * yourselection[currentCaster].get_special_stat("slayCounter"), 1200)
            if not enemies[target].is_alive():
                yourselection[currentCaster].modify_special_stat('slayCounter',1)

def revoke(target, caster, casters, enemies):
    global enemyrevoked
    enemyrevoked[target] = True #TODO: make this a property of Enemy

def healmore(target, caster, casters, enemies):
    for i in range(3):
            casters[i].heal(900)


def revive(target, caster, casters, enemies):
    #TODO: figure out how to do revive
    if not casters[target].is_alive():
        casters[target].health = casters[target].max_health//2
    pass

def flameshell():
    global skilldamage, beforehealthtarget, currentaction, framedelay, beforehealth, playAbilityAnimation
    beforehealthtarget = positions[i] #TODO: flameshell deals 200-400 damage to attacking enemies and lasts 2-3 turns
    beforehealth = yourselection[currentCaster].health
    yourselection[currentCaster].tired = False
    currentaction = ""
    playAbilityAnimation = True

def firestorm(target, caster, casters, enemies):
    for i in range(3):
        enemies[i].damage(1000, casters[caster])
    if randint(0,5) == 0:
        casters[caster].damage(700)
def taunt(target, caster, casters, enemies):
    global taunted
    taunted[target] = True #TODO: make taunted a property of Caster, sidenote: taunted probably doesn't work, haven't tested but have a suspicion
def stabstabstab(target, caster, casters, enemies):
    enemies[target].damage(casters[caster].attack_damage*3, casters[caster])

def bigtaunt(target, caster, casters,enemies):
    global taunted
    for j in range(3):
        taunted[j] = True
def shieldsup(target, caster, casters, enemies):
    for j in range(3):
        casters[j].set_defending(True)
def lancethrow(target, caster, casters, enemies):
    pass
    #TODO: lancethrow should disable the hero for ane extra turn, maybe make Caster.tired an int?
def fallingsword(target, caster, casters, enemies):
    choice([i for i in enemies if i.is_alive()]).damage(800, casters[caster])

def counterattack(target, caster, casters, enemies):
    pass
    #TODO: counter attack, may need special stat

def preparation(target, caster, casters, enemies):
    casters[caster].damage_multiplier+=1.2

def helpinghand(target, caster, casters, enemies):
    casters[target].damage_multiplier+=0.5
    #TODO: helpinghand, adds to a Caster's storedDamage

def shieldaura(target, caster, casters, enemies):
    pass
    #TODO: shieldaura, maybe change blocking into a float? 1x for normal damage, 0.5x for defending, 0.8x for shieldaura

def extravagantshot(target, caster, casters, enemies):
    casters[caster].heal(800)
def biggerandstronger(target, caster, casters, enemies):
    casters[caster].damage_multilpier+=0.3
    #TODO: biggerandstronger, adds to a caster's storedDamage

def flashyarrow(target, caster, casters, enemies):
    pass
    #TODO: this requires taunting to work

def vampiricstrike(target, caster, casters, enemies):
    casters[caster].heal(min(800,enemies[target].health))

def playdead(target, caster, casters, enemies):
    pass
    #TODO: playdead, add a nontargetable property to Caster

def analyze(target, caster, casters, enemies):
    enemies[target].vulnerable = True
    #TODO: change vulnerable from bool to float multiplier

def cull(target, caster, casters, enemies):
    totalDamageDealt = 0
    for i in range(3):
        if i!=target:
            totalDamageDealt+=enemies[i].damage(800, casters[caster])

def reap(target, caster, casters, enemies):
    healedAmount = min(enemies[target].health,900*casters[caster].damage_multiplier)
    livingAllies = [i for i in casters if i.is_alive()]
    for i in livingAllies:
        i.heal(healedAmount/len(livingAllies))
# All the character names stats and abilities in a list

stats = [
    caster.Caster('erik', 3000, 1000, 500, 'assassin',
                  ability.Ability("backstab", 350, ability.AbilityType.DAMAGING, 0, callback=backstab),
                  ability.Ability("silentstrike", 350, ability.AbilityType.DAMAGING, 350, callback = silentstrike),
                  ability.Ability('execute', 750, ability.AbilityType.DAMAGING, 0, callback=execute), erikAnimation, erikSpellAnimation, defendAnimation),
    # high damage ability, ability that makes erik untargetable, ability does damage based on imssing health
    caster.Caster("aliza", 3600, 2600, 250, "mage",
                  ability.Ability("lightningbolt", 300, ability.AbilityType.DAMAGING, 0, callback= lightningbolt),
                  ability.Ability("lightningcharge", 500, ability.AbilityType.DAMAGING, 0, callback = lightningcharge),
                  ability.Ability("lightningrelease", 700, ability.AbilityType.DAMAGING, 0, callback = lightningrelease), alizaAnimation, alizaSpellAnimation, defendAnimation,lightningCharges=0),
    # random damage, charging move, release the charge
    caster.Caster("julie", 3500, 1250, 350, "archer",
                  ability.Ability("sniperarrow", 500, ability.AbilityType.DAMAGING, 800),
                  ability.Ability("herbsandpoultices", 500, ability.AbilityType.HEALING, 0, callback = herbsandpoultices),
                  ability.Ability("gunsling", 1000, ability.AbilityType.DAMAGING, 1200), julieAnimation, julieSpellAnimation, defendAnimation),
    # boom headshot, heal to her or small heal to ally, throws a gun at someone
    caster.Caster("supreet", 3800, 1750, 300, "noble",
                  ability.Ability("slay", 0, ability.AbilityType.DAMAGING, 0, callback = slay),
                  ability.Ability("darkmagic", 450, ability.AbilityType.DAMAGING, 800),
                  ability.Ability("revoke", 600, ability.AbilityType.DAMAGING, 0, callback = revoke), supreetAnimation, supreetSpellAnimation, defendAnimation, slayCounter=0),
    # whenever you kill something, the damage permanently goes up, dark pulse magic, enemy can't attack
    caster.Caster("natalie", 3800, 2000, 80, "healer",
                  ability.Ability("heal", 400, ability.AbilityType.HEALING, 1000),
                  ability.Ability("healmore", 800, ability.AbilityType.HEALING, 0, callback = healmore),
                  ability.Ability("revive", 600, ability.AbilityType.HEALING, 0, callback = revive), natAnimation, natSpellAnimation, defendAnimation),
    # single target heal, AOE heal, revives an ally
    caster.Caster("jan", 3700, 2600, 150, "mage",
                  ability.Ability("fireball",350, ability.AbilityType.DAMAGING, 800),
                  ability.Ability("flameshell",500,ability.AbilityType.DAMAGING, 0, callback = flameshell),
                  ability.Ability("firestorm", 1000, ability.AbilityType.DAMAGING, 0, callback= firestorm), janAnimation, janSpellAnimation, defendAnimation),
    # Steady just fireball, reflect a certain amount of damage to one enemy, AOE damage that can potentially hit jan as well
    caster.Caster("emily", 5200, 1750, 250, "knight",
                  ability.Ability("taunt",200, ability.AbilityType.DAMAGING, 0, callback = taunt),
                  ability.Ability("stabstabstab",400, ability.AbilityType.DAMAGING, 0, callback= stabstabstab),
                  ability.Ability("dragonflame", 500, ability.AbilityType.DAMAGING, 800), emilyAnimation, emilySpellAnimation, defendAnimation),
    # taunts target enemy to attack her, normal attack 3 times on an enemy, dragon breath
    caster.Caster("linh", 5500, 2000, 200, "knight",
                  ability.Ability("bigtaunt", 600, ability.AbilityType.DAMAGING, 0, callback = bigtaunt),
                  ability.Ability("shieldsup",500, ability.AbilityType.DAMAGING, 0, callback = shieldsup),
                  ability.Ability("lancethrow", 500, ability.AbilityType.DAMAGING, 800, callback = lancethrow), linhAnimation, linhSpellAnimation, defendAnimation),
    # all enemies have to attack this char, allies get defend, damage but can't attack next turn
    caster.Caster("priyonto", 3600, 1600, 325, "lord",
                  ability.Ability("fallingsword", 500, ability.AbilityType.DAMAGING, 0, callback = fallingsword),
                  ability.Ability("counterattack", 500, ability.AbilityType.DAMAGING, 0, callback = counterattack),
                  ability.Ability("preparation", 500, ability.AbilityType.DAMAGING, 0, callback = preparation), priyontoAnimation, priyontoSpellAnimation, defendAnimation),
    # falling sword hits a random enemy, deals counter damage, buffffs own next attack
    caster.Caster("minya", 2900, 1800, 100, "healer",
                  ability.Ability("heal", 400, ability.AbilityType.HEALING, 1000),
                  ability.Ability("helpinghand", 500, ability.AbilityType.HEALING, 0, callback = helpinghand),
                  ability.Ability("shieldaura", 500, ability.AbilityType.DAMAGING, 0, callback = shieldaura), minyaAnimation, minyaSpellAnimation, defendAnimation),#TODO: make shieldaura work
    # single target heal, damage buff to an ally, shield buff to an ally
    caster.Caster("viv", 3400, 1300, 375, "archer",
                  ability.Ability("extravagantshot", 500, ability.AbilityType.DAMAGING, 800, callback = extravagantshot),
                  ability.Ability("biggerandstronger", 500, ability.AbilityType.DAMAGING, 0, callback = biggerandstronger), #TODO: verify these are correctly implemented to the description
                  ability.Ability("flashyarrow", 800, ability.AbilityType.DAMAGING, 1600, callback = flashyarrow), vivAnimation, vivSpellAnimation, defendAnimation),
    # heals and damages, buffs next damaging attack, big damage but targeted by enemies
    caster.Caster("ogu", 3000, 1250, 500, "assassin",
                  ability.Ability("vampiricstrike", 500, ability.AbilityType.DAMAGING, 800, callback = vampiricstrike),
                  ability.Ability("playdead", 350, ability.AbilityType.DAMAGING, 0, callback = playdead), #TODO: make these work
                  ability.Ability("analyze", 500, ability.AbilityType.DAMAGING, 0, callback = analyze), oguAnimation, oguSpellAnimation, defendAnimation),
    # does damage and heals, can't be targeted by enemies or allies, enemy takes extra damage from all sources for a turn
    #caster.Caster("zak", 3900, 1500, 300, "warrior", "groundslam", "cull", "reap")
    caster.Caster("zak", 3900, 1500, 300, "warrior",
                  ability.Ability("groundslam", 500, ability.AbilityType.DAMAGING, 700),
                  ability.Ability("cull", 600, ability.AbilityType.DAMAGING, 0, callback = cull),
                  ability.Ability("reap", 700, ability.AbilityType.DAMAGING, 900, callback = reap), zakAnimation, zakSpellAnimation, defendAnimation)
    # slams earth into the persons face, slashes 2 times at 2 enemies, attacks an enemy and heals all party members for small amount
]

infoCards = infoCard.constructCards(stats,
                                    [erikprof, alizaprof, julieprof, supprof, natprof, janprof, emilyprof, linhprof, printerprof, minyaprof, vivprof, oguprof, zakprof],
                                    [erikportrait, alizaportrait, julieportrait, supportrait, natportrait, janportrait, emilyportrait, linhportrait, printerportrait, minyaportrait, vivportrait, oguportrait, zakportrait],
                                    )
def UI():  # This is the UI or health bars that need to be blitted
    for num, i in enumerate(selectnums):
        if yourselection[num].health > 0:
            screen.blit(battleportraits[i][0], (10, [0, 245, 490][num]))
        else:
            screen.blit(battleportraits[i][1], (10, [0, 245, 490][num]))
    for playing in positions:
        # drawhealthbar
        draw.rect(screen, COLOURS.GREEN, (25, 199 + 250 * (playing), 200, 25), 2)
        draw.rect(screen, COLOURS.BLUE, (25, 225 + 250 * (playing), 200, 25), 2)
        draw.rect(screen, COLOURS.GREEN,
                  (25, (199 + 250 * (playing)), (2 * (100 * (yourselection[playing].health) / yourselection[playing].max_health)), 25),
                  0)
        draw.rect(screen, COLOURS.BLUE,
                  (25, (225 + 250 * (playing)), (2 * (100 * (yourselection[playing].mana) / yourselection[playing].max_mana)), 25), 0)
        screen.blit(ffont.render("%4d/%d" % (yourselection[playing].health, yourselection[playing].max_health), True, COLOURS.LIGHT_GREEN),
                    (28, 203 + 250 * playing))
        screen.blit(ffont.render("%4d/%d" % (yourselection[playing].mana, yourselection[playing].max_mana), True, COLOURS.LIGHT_BLUE),
                    (28, 228 + 250 * playing))
    for i, enemyRect in zip(range(0, len(enemieselection)), RECTANGLES.BATTLE_UI.ENEMY_RECTS):
        if enemieselection[i].is_alive():
           draw.rect(screen, COLOURS.WHITE, (enemyRect.x, enemyRect.y-20, 150, 10), 1)
           draw.rect(screen, COLOURS.WHITE,
                  (enemyRect.x, enemyRect.y-20, (150 * enemieselection[i].health / enemieselection[i].max_health), 10),
                  0)


def battle(area, battlenum):  # The main battle function
    global currentCaster, currentaction, currentattacker, currentattackertime, mx, my, mb, clicked, playerturn, framedelay, planneddamage, skilldamage, currentlyCasting, healing, enemieselection, enemieshealths, beforehealth, beforehealthtarget, playAbilityAnimation
    defendingcounter = 0  # A counter used for blitting defense
    currentSkillAnimationFrame = 0  # Same as above except for skills
    enemieselection = [enemyrotations[battlenum][i] for i in range(3)]
    running = True
    clockity = time.Clock()
    speechBubbleTime, speechBubbleText, speechBubbleX, speechBubbleY = 0, '', 0, 0
    if battlenum == 3 or battlenum == 7 or battlenum == 11:
        for i in range(3):
            yourselection[i].health = yourselection[i].max_health
            yourselection[i].mana = yourselection[i].max_mana
            yourselection[i].tired = False
        playerturn = True
    while running:
        for evt in event.get():
            mb = mouse.get_pressed()
            mx, my = mouse.get_pos()
            if evt.type == QUIT:
                running = False  # This is meant to be for loading
                quit()
            if evt.type == MOUSEBUTTONUP:
                clicked = False
        if any([i.health for i in yourselection]):
            if currentattacker != -1 and framedelay == -1:
                currentattackertime += 1  # This initializes the attacking animation
            if not any([i.health for i in enemieselection]):
                battlenum += 1  # If the enemies are dead then they move on to the next wave
                running = False
                return battlenum
            screen.blit(area, (0, 0))  # Blit the area
            UI()
            screen.blit(ffont.render('Damage Multipliers '+(' '.join([str(i.damage_multiplier) for i in yourselection])),True,COLOURS.WHITE,COLOURS.BLACK),(0,0))
            for i, v in enumerate(RECTANGLES.BATTLE_UI.ENEMY_RECTS):  # Blitting enemies depending on their health
                enemyType = enemieselection[i].enemyType
                if enemyType == "grunt" and enemieselection[i].health > 0:
                    blit_pos = math_tools.get_centered_blit_pos(v, enemyanimation[0][0][0])
                    screen.blit(enemyanimation[0][0][0], blit_pos)
                elif enemyType == "tough" and enemieselection[i].health > 0:
                    blit_pos = math_tools.get_centered_blit_pos(v, enemyanimation[1][0][0])
                    screen.blit(enemyanimation[1][0][0], blit_pos)
                elif enemyType == "miniboss":
                    blit_pos = math_tools.get_centered_blit_pos(v, enemyanimation[2][0][0])
                    screen.blit(enemyanimation[2][0][0], blit_pos)
                elif enemyType == "aaron":
                    blit_pos = math_tools.get_centered_blit_pos(v, enemyanimation[3][0][0])
                    screen.blit(enemyanimation[3][0][0], blit_pos)
                elif enemyType == "vlad":
                    blit_pos = math_tools.get_centered_blit_pos(v, enemyanimation[4][0][0])
                    screen.blit(enemyanimation[4][0][0], blit_pos)
                elif enemyType == "kim":
                    blit_pos = math_tools.get_centered_blit_pos(v, enemyanimation[5][0][0])
                    screen.blit(enemyanimation[5][0][0], blit_pos)
            for players, playerNumber in zip(selectnums, positions):  # This is used for blitting the characters
                if playerNumber == currentCaster and playAbilityAnimation: # don't draw ability casting player
                    yourselection[currentCaster].spellAnimation.update()
                    yourselection[currentCaster].spellAnimation.draw(screen, 325 - 15 * currentCaster,
                                                                     20 + 190 * currentCaster)
                    if yourselection[currentCaster].spellAnimation.isFinishedRunning():
                        yourselection[currentCaster].tired = True
                        currentlyCasting = -1
                        framedelay = -1
                        playAbilityAnimation = False
                elif playerNumber == currentattacker and framedelay==-1: #draw casting player
                    yourselection[currentattacker].animation.update()
                    yourselection[currentattacker].animation.draw(screen,325-15*playerNumber,  20+190*playerNumber)
                    if yourselection[
                        currentCaster].animation.isFinishedRunning():  # currentattackertime >= len(animations[playerNumber][1]) * framedenom:  # Changing the character to having gone already
                        clicked = False
                        currentattacker = -1
                        yourselection[currentCaster].tired = True
                        currentattackertime = 0
                elif yourselection[playerNumber].is_alive():  # draw non casting, standing player
                    yourselection[playerNumber].animation.reset()
                    yourselection[playerNumber].spellAnimation.reset()
                    screen.blit(animations[players][0][0], (325 - 15 * playerNumber, 20 + 190 * playerNumber))
                else:
                    screen.blit(animations[players][4][0], (325 - 15 * playerNumber, 20 + 190 * playerNumber))
                #draw caster specific icons
                if yourselection[playerNumber].name == 'supreet' and yourselection[
                    playerNumber].health != 0:  # draw supreet's slay counter
                    for i in range(yourselection[playerNumber].get_special_stat('slayCounter')):
                        screen.blit(transform.scale(fire, (15, 15)), (26 + 16 * i, 180 + 251 * playerNumber))
                if yourselection[playerNumber].name == 'aliza' and yourselection[playerNumber].health!=0:
                    for i in range(yourselection[playerNumber].get_special_stat("lightningCharges")):
                        screen.blit(transform.scale(lightning, (15, 15)), (26 + 16 * i, 180 + 251 * playerNumber))

                if yourselection[playerNumber].defending:
                    yourselection[playerNumber].defendAnimation.update()
                    yourselection[playerNumber].defendAnimation.draw(screen, 325 - 15 * currentCaster, 40 + 190 * currentCaster)
                    if yourselection[playerNumber].defendAnimation.isFinishedRunning():
                        clicked = False
                        currentattacker = -1
                        yourselection[currentCaster].tired = True
                        currentattackertime = 0
            if(framedelay>=0):
                framedelay-=1
            if beforehealth != -1:  # Used for Jan's Flame Shell
                for i in range(3):
                    if yourselection[i][0] == "jan":
                        if beforehealth != yourselection[i].health:
                            enemieshealths[beforehealthtarget] = max(0, enemieshealths[beforehealthtarget] - (
                            beforehealth - yourselection[currentCaster].health))
                beforehealth = -1
                beforehealthtarget = -1


            if framedelay == -1:  # If your characters went to determine the next ally to go or if its the enemies turn
                if any([i.health for i in yourselection]):
                    while yourselection[currentCaster].health == 0:
                        yourselection[currentCaster].tired = True
                        currentCaster = (currentCaster+1)%3
                if yourselection[currentCaster].tired and currentCaster + 1 == 3:
                    currentCaster = 0
                while yourselection[currentCaster].tired and currentCaster + 1 != 3:
                    currentCaster += 1
                if all([i.tired for i in yourselection]):
                    currentCaster = 0
                    playerturn = False
            if playerturn:  # While its the players turn
                for i in range(3):
                    enemieselection[i].tired=False
                draw.polygon(screen, COLOURS.PURPLE, (selectpoly[currentCaster]))
                if framedelay == -1:
                    currentaction = buttons(currentCaster)
                    currentCaster = casting(currentaction, currentCaster)
            if not playerturn:  # Its the enemies turn till it turns into the allys turn again
                playerturn = enemycast()
        else:
            #death screen
            screen.blit(deathScreen,(0,0))
            for i,v in enumerate(selectnums):
                screen.blit(animations[v][4][0],(315+i*315-animations[v][4][0].get_width()/2,500))
            if speechBubbleTime == 0:
                speechBubbleX = 335+315*randint(0,2)
                speechBubbleY = 500
                speechBubbleText = choice(['Oof','Ouch','Owie',"I'm dead", "This sucks"])
                speechBubbleTime = 200
            else:
                speechBubbleTime-=1
            drawSpeechBubble(speechBubbleX,speechBubbleY,speechBubbleText)
        display.flip()
        clockity.tick(60)
    return battlenum

def drawSpeechBubble(x ,y, text, drawSurf=screen):
    renderText=ffont.render(text, True, COLOURS.BLACK)
    draw.polygon(drawSurf,COLOURS.WHITE,[(x,y+renderText.get_height()+20),(7+x,y+renderText.get_height()+20),(5+x,y+renderText.get_height()+30),(15+x,y+40),(renderText.get_width()+20+x,y+40),(renderText.get_width()+20+x,y),(x,y)])
    screen.blit(renderText,(x+(renderText.get_width()+20)//2-renderText.get_width()//2,y+(renderText.get_height()+20)//2-renderText.get_height()//2))
def buttons(caster):  # Pressing a button with a function attached calls the function
    global clicked
    if currentaction == "":
        for b, v in zip(RECTANGLES.BATTLE_UI.ACTION_BUTTONS, values):
            draw.rect(screen, COLOURS.BLACK, b, 2)
            if b.collidepoint(mx, my):
                draw.rect(screen, COLOURS.BLACK, b, 5)
                if mb[0] and not + clicked:
                    clicked = True
                    return v
    return currentaction


def casting(action, caster):  # This comes from the button being pressed form before
    startCaster = caster
    if action == "attack":
        caster = attack(caster)
    elif action == "switch":
        caster = switch(caster)
    elif action == "defend":
        caster = defend(caster)
    elif action == "skills":
        caster = skills(caster)
    return caster


def skills(caster):  # Your skill function that draws and blits things getting ready for you skill selection
    global currentaction, clicked, currentattacker, selection, framedelay, playAbilityAnimation
    draw.rect(screen, COLOURS.BUTTONBACK, RECTANGLES.BATTLE_UI.BUTTON_BACKGROUND_FILL, 0)
    draw.rect(screen, COLOURS.BLACK, RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT, 2)
    screen.blit(backing, (320, 620))
    if RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT.collidepoint(mx, my):
        draw.rect(screen, COLOURS.BLACK, RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT, 5)
        if mb[0] and not clicked:
            clicked = True
            currentaction = ""
            return caster
    for button, skill in zip(RECTANGLES.BATTLE_UI.SKILL_BUTTONS, skilllist[caster]):
        draw.rect(screen, COLOURS.BLUE, button, 2)
        screen.blit(abilitybutton[caster][RECTANGLES.BATTLE_UI.SKILL_BUTTONS.index(button)], (660, 620 + 47 * RECTANGLES.BATTLE_UI.SKILL_BUTTONS.index(button)))
        if selection == button:
            draw.rect(screen, COLOURS.WHITE, button, 5)
            screen.blit(abilitydesc[caster][RECTANGLES.BATTLE_UI.SKILL_BUTTONS.index(button)], (320, 683))
            if skill.abilityType == ability.AbilityType.DAMAGING:
                for selectedEnemyIndex, enemyRect in enumerate(RECTANGLES.BATTLE_UI.ENEMY_RECTS):
                    draw.rect(screen, COLOURS.RED, RECTANGLES.BATTLE_UI.ENEMY_RECTS[selectedEnemyIndex], 3)
                    if enemyRect.collidepoint(mx, my) and mb[0] and not clicked:
                        castResult = skill.cast(selectedEnemyIndex,currentCaster, yourselection, enemieselection)
                        if castResult!=None:
                            framedelay = castResult['framedelay']
                            currentaction = castResult['currentaction']
                            playAbilityAnimation = castResult['playAbilityAnimation']
                            yourselection[caster].damage_multiplier = 1
            elif skill.abilityType == ability.AbilityType.HEALING:
                for selectedAllyIndex, allyRect in enumerate(RECTANGLES.BATTLE_UI.PLAYER_RECTS):
                    draw.rect(screen, COLOURS.GREEN, RECTANGLES.BATTLE_UI.PLAYER_RECTS[selectedAllyIndex], 3)
                    if allyRect.collidepoint(mx, my) and mb[0] and not clicked:
                        castResult = skill.cast(selectedAllyIndex,currentCaster, yourselection, enemieselection)
                        if castResult!=None:
                            framedelay = castResult['framedelay']
                            currentaction = castResult['currentaction']
                            playAbilityAnimation = castResult['playAbilityAnimation']
                            yourselection[caster].damage_multiplier = 1
        if button.collidepoint(mx, my):
            draw.rect(screen, COLOURS.BLUE, button, 5)
            screen.blit(abilitydesc[caster][RECTANGLES.BATTLE_UI.SKILL_BUTTONS.index(button)], (320, 683))
            if mb[0] and not clicked:
                selection = button
                clicked = True
    return caster


def attack(caster):  # The attacking function for your character selecting an enemy and dealing their damage
    global currentaction, clicked, currentattacker, framedelay, planneddamage
    draw.rect(screen, COLOURS.BUTTONBACK, RECTANGLES.BATTLE_UI.BUTTON_BACKGROUND_FILL, 0)
    draw.rect(screen, COLOURS.BLACK, RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT, 2)
    screen.blit(backing, (320, 620))
    if RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT.collidepoint(mx, my):
        draw.rect(screen, COLOURS.BLACK, RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT, 5)
        if mb[0] and not clicked:
            clicked = True
            currentaction = ""
    for i, v in enumerate(RECTANGLES.BATTLE_UI.ENEMY_RECTS):
        draw.rect(screen, COLOURS.RED, RECTANGLES.BATTLE_UI.ENEMY_RECTS[i], 3)
        if v.collidepoint(mx, my) and mb[0] and not clicked and yourselection[caster].can_attack() and enemieselection[i].is_alive():
            framedelay = 5
            enemieselection[i].damage(yourselection[caster].attack_damage, yourselection[caster])
            clicked = True
            currentattacker = caster
            currentaction = ""
            yourselection[caster].damage_multiplier = 1
    return caster


def defend(caster):  # The defending function where the damage gets halved
    global currentaction, clicked, defending, nottired, framedelay
    draw.rect(screen, COLOURS.BUTTONBACK, RECTANGLES.BATTLE_UI.BUTTON_BACKGROUND_FILL, 0)
    draw.rect(screen, COLOURS.BLACK, RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT, 2)
    draw.rect(screen, COLOURS.BLUE, RECTANGLES.BATTLE_UI.CONFIRM_RECT, 2)
    screen.blit(backing, (320, 620))
    screen.blit(confirming, (630, 620))
    if RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT.collidepoint(mx, my):
        draw.rect(screen, COLOURS.BLACK, RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT, 5)
        if mb[0] and not clicked:
            clicked = True
            currentaction = ""
    if RECTANGLES.BATTLE_UI.CONFIRM_RECT.collidepoint(mx, my):
        draw.rect(screen, COLOURS.BLUE, RECTANGLES.BATTLE_UI.CONFIRM_RECT, 5)
        if mb[0] and not clicked and not yourselection[caster].tired:
            yourselection[caster].set_defending(True)
            yourselection[caster].tired = True
            framedelay = 5
            clicked = True
            currentaction = ""
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
            currentaction = ""
    for i, v in zip(positions, RECTANGLES.BATTLE_UI.PLAYER_RECTS):
        if not yourselection[i].tired and caster != i:
            draw.polygon(screen, COLOURS.WHITE, (selectpoly[i]), 2)
        if v.collidepoint(mx, my) and mb[0] and not clicked and not yourselection[i].tired:
            clicked = True
            currentaction = ""
            switched = True
            return i
    return caster


def enemycast():  # The enemy attacking, It changes depending on what enemy is in the rotation
    global playerturn, nottired, enemyframedelay, taunted
    for i, v in enumerate(RECTANGLES.BATTLE_UI.ENEMY_RECTS):
        if enemyframedelay > 0:
            enemyframedelay -= 1
        elif enemyframedelay == 0:
            if enemyrevoked[i] == True:
                enemieselection[i].tired = True
            if enemieselection[i].health == 0:
                enemieselection[i].tired = True
            if enemieselection[i].enemyType == "grunt" and not enemieselection[i].tired:
                if taunted[i]:
                    attacken(positions[selectnums.index(6)], enemieselection[i].attackDamages[0], fire, 0, i)
                else:
                    targeting(enemieselection[i].attackDamages[0], fire, 0, i)
            elif enemieselection[i].enemyType == "tough" and not enemieselection[i].tired:
                move = randint(0, 3)
                if taunted[i]:
                    attacken(positions[selectnums.index(6)], enemieselection[i].attackDamages[0], ice, 1, i)
                if move == 0:
                    targeting(enemieselection[i].attackDamages[1], ice, 1, i)
                else:
                    priority(enemieselection[i].attackDamages[0], ice, 1, i)
            elif enemieselection[i].enemyType == "miniboss" and not enemieselection[i].tired:
                if taunted[i]:
                    attacken(positions[selectnums.index(6)], enemieselection[i].attackDamages[0], lightning, 2, i)
                if enemieselection[i].health > (enemieselection[i].health // 2):
                    move = randint(0, 6)
                else:
                    move = randint(0, 3)
                if move in [3, 4, 5, 6]:
                    priority(enemieselection[i].attackDamages[0], lightning, 2, i)
                elif move in [1, 2]:
                    priority(enemieselection[i].attackDamages[1], lightning, 2, i)
                elif move == 0:
                    priority(enemieselection[i].attackDamages[2], lightning, 2, i)
            elif enemieselection[i].enemyType == "aaron":
                screen.blit(enemyanimation[3][0][0], (1080 - 15 * i, 400 - 190 * i))
                if taunted[i]:
                    attacken(positions[selectnums.index(6)], enemieselection[i].attackDamages[0], dumpling, 3, i)
                if enemieselection[i].health > (enemieselection[i].health // 2):
                    move = randint(0, 6)
                else:
                    move = randint(0, 3)
                if move in [3, 4, 5, 6]:
                    targeting(enemieselection[i].attackDamages[0], dumpling, 3, i)
                elif move in [2, 1]:
                    priority(enemieselection[i].attackDamages[1], dumpling, 3, i)
                elif move == 0:
                    attackaoe(enemieselection[i].attackDamages[2], dumpling, 3, i)
            elif enemieselection[i].enemyType == "vlad":
                screen.blit(enemyanimation[4][0][0], (1080 - 15 * i, 400 - 190 * i))
                if taunted[i]:
                    attacken(positions[selectnums.index(6)], enemieselection[i].attackDamages[0], music, 4, i)
                if enemieselection[i].health > (enemieselection[i].health // 2):
                    move = randint(0, 6)
                else:  # Depending on which numer is picked, either a stronger or weaker move is made
                    move = randint(0, 3)
                if move in [3, 4, 5, 6]:
                    targeting(enemieselection[i].attackDamages[0], music, 4, i)
                elif move in [1, 2]:
                    priority(enemieselection[i].attackDamages[1], music, 4, i)
                elif move == 0:
                    attackaoe(enemieselection[i].attackDamages[2], music, 4, i)
            elif enemieselection[i].enemyType == "kim":
                if taunted[i]:
                    attacken(positions[selectnums.index(6)], enemieselection[i].attackDamages[0], diamond, 5, i)
                if enemieselection[i].health > (enemieselection[i].health // 2):
                    move = randint(0, 6)
                else:
                    move = randint(0, 3)
                if move in [3, 4, 5, 6]:
                    targeting(enemieselection[i].attackDamages[0], diamond, 5, i)
                elif move in [1, 2]:
                    priority(enemieselection[i].attackDamages[1], diamond, 5, i)
                elif move == 0:
                    attackaoe(enemieselection[i].attackDamages[2], diamond, 5, i)
                screen.blit(enemyanimation[5][0][0], (1080 - 15 * i, 400 - 190 * i))
            if all([i.tired for i in enemieselection]):  # When all the enemies go it becomes the partys turn
                for i in range(3):
                    yourselection[i].set_defending(False)
                    yourselection[i].dodging=False
                    yourselection[i].tired=False
                playerturn = True
                taunted = [False, False, False]
                enemyframedelay = 15
                for i in range(3):
                    yourselection[i].regen_mana()
                return playerturn
            enemyframedelay = 15
    return playerturn


def attacken(someone, somedmg, animation, enemypos,
             enemynum):  # This is the main function where an enemy applies his damage to the party member
    screen.blit(animation, (randint(0, 1000), randint(0, 700)))
    if yourselection[someone].defending:  # If the ally is defending then the damage is halved
        screen.blit(shield1, (325 - 15 * someone, 20 + 190 * someone))
    yourselection[someone].damage(somedmg)
    enemieselection[enemynum].tired = True
    screen.blit(enemyanimation[enemypos][1][0], (1080 - 15 * enemynum, 400 - 190 * enemynum))
    screen.blit(animations[selectnums[someone]][3][0], (325 - 15 * someone, 20 + 190 * someone))
    display.flip()


def attackaoe(somedmg, animation, enemypos,
              enemynum):  # The attacking function for the bosses where it deals damage to the entire party
    for i in range(3):
        screen.blit(animation, (randint(0, 1000), randint(0, 1000)))
        if yourselection[i].defending:
            screen.blit(shield1, (325 - 15 * i, 20 + 190 * i))
        yourselection[currentCaster].damage(somedmg)
        screen.blit(enemyanimation[enemypos][1][0], (1080 - 15 * enemynum, 400 - 190 * enemynum))
        screen.blit(animations[selectnums[i]][3][0], (325 - 15 * i, 20 + 190 * i))
    enemieselection[enemynum] = True


def priority(dmg, animation, enemypos, enemynum):  # Prioritizing the lowest healthed party member to attack
    target = yourselection.index(min([i for i in yourselection if i.health > 0]))
    attacken(target, dmg, animation, enemypos, enemynum)


def targeting(dmg, animation, enemypos, enemynum):  # Targetting a random party member to attack
    target = yourselection.index(choice([i for i in yourselection if i.health > 0]))#healths.index(choice([health for health in healths if health > 0]))
    attacken(target, dmg, animation, enemypos, enemynum)


def load():  # The loading function
    global yourselectio, pparty, selectnums, abilitybutton, abilitydesc, healths, manas, battlenum, scenenum
    print("Loading is not implemented yet!")


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
        frame = codeSystem()

quit()
