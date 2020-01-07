from pygame import Rect

class MAIN_MENU:
    NEW_GAME_RECT = Rect(430, 275, 400, 95)
    CONTINUE_RECT = Rect(430, 385, 400, 95)
    INSTRUCTION_RECT = Rect(430, 500, 400, 90)
    CODE_RECT = Rect(430, 610, 400, 100)
    EXIT_RECT = Rect(485, 805, 190, 87)

class CHARACTER_SELECTION:
    SELECT_RECT = Rect(514, 638, 230, 90)
    LEFT_TRIPTS= [(412, 325), (412, 590), (303, 457)]
    RIGHT_TRIPTS = [(835, 325), (835, 590), (930, 457)]
    WHITE_RECT = Rect(513, 355, 224, 200)
    NO_RECT = Rect(490, 700, 190, 87)
    NAME_RECT = Rect(476, 202, 300, 100)
    STORY_RECT = Rect(980, 308, 250, 300)
    STATS_RECT = Rect(24, 308, 250, 300)

class CUTSCENES:
    LORE_RECT = Rect(0, 600, 1260, 150)
    PROFILE_RECT = Rect(0, 600, 150, 150)

class BATTLE_UI:

    __action_button_width = 195
    __action_button_left_margin = 253
    __action_button_top_margin = 698
    __action_button_spacing = 8
    __action_button_height = 42

    ENEMY_RECTS = [Rect(1080, 540, 160, 180), Rect(1050, 300, 160, 180),
                  Rect(1020, 60, 160, 180)]  # The enemies rectangles to be pressed when attacking or using skills

    PLAYER_RECTS = [Rect(325, 20, 120, 180), Rect(310, 210, 120, 180),
                   Rect(295, 400, 120, 180)]  # Ally rectangles for when heals are happening

    ACTION_BUTTONS = [(Rect(__action_button_left_margin, __action_button_top_margin, __action_button_width, __action_button_height)),
                      (Rect(__action_button_left_margin + __action_button_width + __action_button_spacing, __action_button_top_margin, __action_button_width, __action_button_height)),
                      (Rect(__action_button_left_margin + (__action_button_width + __action_button_spacing) * 2, __action_button_top_margin, __action_button_width, __action_button_height)),
                      (Rect(__action_button_left_margin + (__action_button_width + __action_button_spacing) * 3, __action_button_top_margin, __action_button_width, __action_button_height))]  # The buttons for all your possible options
    SKILL_BUTTONS = ACTION_BUTTONS[1:]  # The buttons for the skills when youre using a skill

    ABILITY_DESCRIPTION = (252, 622)

    BUTTON_BACKGROUND_FILL = Rect(__action_button_left_margin-__action_button_spacing, 611, __action_button_width*4+__action_button_spacing*5, 144)
    BACK_BUTTON_RECT = ACTION_BUTTONS[0]
    CONFIRM_RECT = ACTION_BUTTONS[1]