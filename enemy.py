from src.status_effect import DOTEffect, EffectEndedException


class Enemy:
    def __init__(self, enemyType, health, animations, *argsv):
        self.enemyType = enemyType
        self.health = health
        self.max_health = health
        self.attackDamages = argsv
        self.vulnerable = False
        self.revoked = False
        self.tired = False
        self.dot_effects = []
        self.animations = animations

    def damage(self, amount, attackingCaster):
        print(self.enemyType, 'took', amount * attackingCaster.damage_multiplier, 'damage (%.2f multiplier applied)'%(attackingCaster.damage_multiplier*100))
        damageDealt = min(self.health, amount * attackingCaster.damage_multiplier)
        self.health -= damageDealt
        return damageDealt

    def is_alive(self):
        return self.health > 0

    def can_attack(self):
        return self.is_alive() and not self.revoked and not self.tired

    def apply_status_effects(self):
        for effectIndex in range(len(self.dot_effects) - 1, -1, -1):
            effect = self.dot_effects[effectIndex]
            try:
                effect.step()
                if isinstance(effect, DOTEffect):
                    self.health -= effect.influence_amount
            except EffectEndedException:
                self.dot_effects.remove(effect)
