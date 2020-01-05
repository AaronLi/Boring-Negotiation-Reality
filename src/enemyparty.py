from src.constants import RECTANGLES
import math_tools


class EnemyParty:
    def __init__(self, enemies = None) -> None:
        self.members = enemies if enemies is not None else []

    def get_member_index(self, member):
        return self.members.index(member)

    def clear_taunts(self):
        for member in self.members:
            member.clear_taunt_targets()

    @property
    def defeated(self):
        return not any([enemy.is_alive() for enemy in self.members])

    def draw_party(self, surface):
        for i, v in enumerate(RECTANGLES.BATTLE_UI.ENEMY_RECTS):  # Blitting enemies depending on their health
            enemyInfo = self.members[i]
            if not enemyInfo.is_alive():
                continue
            blit_pos = math_tools.get_centered_blit_pos(v, enemyInfo.animations.stance)
            surface.blit(enemyInfo.animations.stance, blit_pos)
