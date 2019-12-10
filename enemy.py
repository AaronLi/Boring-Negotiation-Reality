from src.status_effect import DOTEffect, EffectEndedException
import random


class Enemy:
    def __init__(self, enemyType, health, animations, *argsv):
        self.enemyType = enemyType
        self.health = health
        self.max_health = health
        self.attackDamages = argsv
        self.vulnerable = False
        self.revoked = False
        self.tired = False
        self.taunt_targets = set()
        self.dot_effects = []
        self.animations = animations

    def damage(self, amount, attackingCaster):
        print(self.enemyType, 'took', amount * attackingCaster.damage_multiplier,
              'damage (%.2f%% of base damage)' % (attackingCaster.damage_multiplier * 100))
        damageDealt = min(self.health, amount * attackingCaster.damage_multiplier)
        attackingCaster.damage_multiplier = 1
        self.health -= damageDealt
        return damageDealt

    def is_alive(self):
        return self.health > 0

    def can_attack(self):
        return self.is_alive() and not self.revoked and not self.tired

    @property
    def taunted(self):
        return len(self.taunt_targets) > 0

    def add_taunt_target(self, target):
        print("%s is now taunting %s!" % (target.name, self.enemyType))
        self.taunt_targets.add(target)

    def remove_taunt_target(self, target):
        self.taunt_targets.remove(target)

    def clear_taunt_targets(self):
        self.taunt_targets.clear()

    @property
    def taunt_target(self):
        return random.choice(list(self.taunt_targets))

    def add_status_effect(self, status_effect):
        print("%s has been inflicted with %s (%d) for %d turns!"%(self.enemyType, status_effect.name, status_effect.influence_amount, status_effect.duration))
        self.dot_effects.append(status_effect)

    def apply_status_effects(self):
        if not self.is_alive():
            self.dot_effects.clear()
        for effectIndex in range(len(self.dot_effects) - 1, -1, -1):
            effect = self.dot_effects[effectIndex]
            try:
                effect.step()
                if isinstance(effect, DOTEffect):
                    if effect.influence_amount > 0:
                        print("%s inflicted %d damage to %s"%(effect.name, effect.influence_amount, self.enemyType))
                        self.health = max(0, self.health - effect.influence_amount)
                    else:
                        print("%s healed %d damage on %s"%(effect.name, -effect.influence_amount, self.enemyType))
                        self.health = min(self.max_health, self.health - effect.influence_amount)
            except EffectEndedException:
                self.dot_effects.remove(effect)
