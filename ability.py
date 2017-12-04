from enum import Enum, auto
class AbilityType(Enum):
    HEALING = auto()
    DAMAGING = auto()
class Ability:
    def __init__(self, working_name, manaCost, abilityType, influenceAmount, callback = None):
        self.working_name = working_name
        self.manaCost = manaCost
        self.abilityType = abilityType
        self.influenceAmount = influenceAmount #can represent healing or damage
        self.callback = callback

    def cast(self,target, caster, casters, enemies): #caster is the currentcaster, enemies is the list of all Enemies on the field, casters is the list of all casters
        if casters[caster].mana >= self.manaCost:
            if self.callback != None:
                status = self.callback(target,caster,casters,enemies)
                if status == 1: #callback has indicated that additional requirements have not been met
                    return None
            casters[caster].mana -= self.manaCost
            if self.abilityType == AbilityType.DAMAGING:
                enemies[target].damage(self.influenceAmount, casters[caster])
            elif self.abilityType == AbilityType.HEALING:
                casters[target].heal(self.influenceAmount)
            return {'framedelay':5, 'currentaction':'', 'playAbilityAnimation':True}