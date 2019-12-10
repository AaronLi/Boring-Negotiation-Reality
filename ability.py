import pickle
from constants.MENU import COMBAT_MENU_MODES
class AbilityType:
    HEALING = 'healing'
    DAMAGING = 'damaging'

class AbilityCastResult:
    def __init__(self, frame_delay, current_action, success) -> None:
        self.frame_delay = frame_delay
        self.current_action = current_action
        self.success = success

class Ability:
    def __init__(self, working_name, manaCost, abilityType, influenceAmount, callback = None):
        self.working_name = working_name
        self.mana_cost = manaCost
        self.ability_type = abilityType
        self.influence_amount = influenceAmount #can represent healing or damage
        self.callback = callback

    def cast(self,target, caster, casters, enemies): #caster is the currentcaster, enemies is the list of all Enemies on the field, casters is the list of all casters
        if casters[caster].mana >= self.mana_cost:
            if self.callback != None:
                status = self.callback(target,caster,casters,enemies)
                if status == 1: #callback has indicated that additional requirements have not been met
                    return AbilityCastResult(0, COMBAT_MENU_MODES.SKILLS, False)
            casters[caster].mana -= self.mana_cost
            if self.ability_type == AbilityType.DAMAGING:
                enemies[target].damage(self.influence_amount, casters[caster])
            elif self.ability_type == AbilityType.HEALING:
                casters[target].heal(self.influence_amount)
            return AbilityCastResult(5, COMBAT_MENU_MODES.MAIN_COMBAT_MENU, True)
        return AbilityCastResult(0, COMBAT_MENU_MODES.SKILLS, False)

    def dictify(self):
        return {
            'name':self.working_name,
            'mana_cost':self.mana_cost,
            'ability_type':self.ability_type,
            'influence_amount':self.influence_amount,
            'callback':''.join(map(chr, pickle.dumps(self.callback)))
        }