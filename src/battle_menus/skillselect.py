from pygame import draw
from src.constants import RECTANGLES, COLOURS, MENU
from src.menu_objects import button
from src.playerparty import PlayerParty
from src.enemyparty import EnemyParty
from src import ability
from copy import deepcopy

class SkillSelect:
    def __init__(self, player_party :PlayerParty, enemy_party :EnemyParty, backing, image_cacher):
        self.player_party = player_party
        self.enemy_party = enemy_party
        self.backing = backing
        self.currentaction = MENU.COMBAT_MENU_MODES.SKILLS

        self.abilitybutton = [
            [image_cacher.try_load("ATTACKS/" + ability.working_name + ".png") for ability in member.abilities] for
            member in
            player_party.members]
        self.abilitydesc = [[image_cacher.try_load("DESCS/" + ability.working_name + ".png") for ability in member.abilities]
                       for member in
                       player_party.members]
        self.selected_ability = None

        self.__create_back_button()
        self.__create_skill_buttons()

        self.select_ally = False
        self.select_enemy = False
        self.image_cacher = image_cacher

    def update_ability_labels(self):
        self.abilitybutton = [
            [self.image_cacher.try_load("ATTACKS/" + ability.working_name + ".png") for ability in member.abilities] for
            member in
            self.player_party.members]
        self.abilitydesc = [[self.image_cacher.try_load("DESCS/" + ability.working_name + ".png") for ability in member.abilities]
                       for member in
                       self.player_party.members]
        self.__create_skill_buttons()

    @property
    def __ability_0_title(self):
        if len(self.abilitybutton) == 0:
            return None
        return self.abilitybutton[self.player_party.current_caster_index][0]

    @property
    def __ability_1_title(self):
        if len(self.abilitybutton) == 0:
            return None
        return self.abilitybutton[self.player_party.current_caster_index][1]

    @property
    def __ability_2_title(self):
        if len(self.abilitybutton) == 0:
            return None
        return self.abilitybutton[self.player_party.current_caster_index][2]

    @property
    def __ability_0_desc(self):
        if len(self.abilitydesc) == 0:
            return None
        return self.abilitydesc[self.player_party.current_caster_index][0]

    @property
    def __ability_1_desc(self):
        if len(self.abilitydesc) == 0:
            return None
        return self.abilitydesc[self.player_party.current_caster_index][1]

    @property
    def __ability_2_desc(self):
        if len(self.abilitydesc) == 0:
            return None
        return self.abilitydesc[self.player_party.current_caster_index][2]

    def __create_back_button(self):
        self.back_button = button.Button(RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT, self.backing, self.backing)

        def hover_callback(surface, shape):
            draw.rect(surface, COLOURS.BLACK, shape, 5)

        def back_button_callback():
            self.currentaction = MENU.COMBAT_MENU_MODES.MAIN_COMBAT_MENU

        self.back_button.hover_callback = hover_callback
        self.back_button.click_callback = back_button_callback

    def __create_skill_buttons(self):
        self.skill_buttons = []

        def skill_button_hover_callback(surface, shape, button_number):
            draw.rect(surface, COLOURS.BLUE, shape, 5)
            surface.blit(self.abilitydesc[self.player_party.current_caster_index][button_number], (280, 615))

        def skill_button_normal_callback(surface, shape):
            draw.rect(surface, COLOURS.BLUE, shape, 2)

        def skill_button_clicked_callback(button_number):
            self.selected_ability = button_number
            print(button_number)

        def create_per_button_callbacks(button_number):
            return lambda surf, shap: skill_button_hover_callback(surf, shap, button_number), lambda: skill_button_clicked_callback(button_number)

        ability_buttons = (self.__ability_0_title, self.__ability_1_title, self.__ability_2_title) # since these are properties, they act like fields but are actually functions

        for i, button_rect in enumerate(RECTANGLES.BATTLE_UI.SKILL_BUTTONS):
            skill_button = button.Button(button_rect, normal_icon=ability_buttons[i], hover_icon=ability_buttons[i]) #hopefully the button icons will change automatically because of the usage of properties in this way
            skill_button.hover_callback, skill_button.click_callback = create_per_button_callbacks(i)
            skill_button.normal_callback = skill_button_normal_callback

            self.skill_buttons.append(skill_button)
        for i,v in enumerate(self.skill_buttons):
            v.click_callback()
            print(v.click_callback)

    def draw(self, surface):
        draw.rect(surface, COLOURS.BUTTONBACK, RECTANGLES.BATTLE_UI.BUTTON_BACKGROUND_FILL, 0)
        draw.rect(surface, COLOURS.BLACK, RECTANGLES.BATTLE_UI.BACK_BUTTON_RECT, 2)
        self.back_button.draw(surface)
        for i, skill in enumerate(self.player_party.current_caster.abilities):
            self.skill_buttons[i].draw(surface)

            if self.selected_ability == i:
                draw.rect(surface, COLOURS.WHITE, self.skill_buttons[i].shape, 5)
                surface.blit(self.abilitydesc[self.player_party.current_caster_index][i], (280, 615))

        if self.select_enemy:
            for enemyRect in RECTANGLES.BATTLE_UI.ENEMY_RECTS:
                draw.rect(surface, COLOURS.RED, enemyRect, 3)
        elif self.select_ally:
            for allyRect in RECTANGLES.BATTLE_UI.PLAYER_RECTS:
                draw.rect(surface, COLOURS.GREEN, allyRect, 3)


    def update(self, mx, my, mb, omb):  # Your skill function that draws and blits things getting ready for you skill selection
        self.currentaction = MENU.COMBAT_MENU_MODES.SKILLS
        self.back_button.update(mx, my, mb)
        for i, skill in enumerate(self.player_party.current_caster.abilities):
            self.skill_buttons[i].update(mx, my, mb)
            if self.selected_ability == i: # desired ability selected
                if skill.ability_type == ability.AbilityType.DAMAGING:
                    self.select_enemy = True
                    for selectedEnemyIndex, enemyRect in enumerate(RECTANGLES.BATTLE_UI.ENEMY_RECTS): #draw boxes on enemies
                        if enemyRect.collidepoint(mx, my) and mb[0] and not omb[0]:
                            castResult = skill.cast(selectedEnemyIndex, self.player_party.current_caster,
                                                    self.player_party.members, self.enemy_party.members)
                            self.currentaction = castResult.current_action
                            if castResult.success:
                                framedelay = castResult.frame_delay
                                self.player_party.current_caster.tired = True
                                self.player_party.current_caster.spell_animation.update()
                                self.selected_ability = None
                elif skill.ability_type == ability.AbilityType.HEALING:
                    self.select_ally = True
                    for selectedAllyIndex, allyRect in enumerate(RECTANGLES.BATTLE_UI.PLAYER_RECTS): #draw boxes on allies
                        if allyRect.collidepoint(mx, my) and mb[0] and not omb[0]:
                            castResult = skill.cast(selectedAllyIndex, self.player_party.current_caster,
                                                    self.player_party.members, self.enemy_party.members)
                            self.currentaction = castResult.current_action
                            if castResult.success:
                                framedelay = castResult.frame_delay
                                self.player_party.current_caster.tired = True
                                self.player_party.current_caster.spell_animation.update()
                                self.selected_ability = None

