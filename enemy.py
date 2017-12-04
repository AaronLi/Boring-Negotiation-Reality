class Enemy:
    def __init__(self, enemyType, health, *argsv, unknown=1):
        self.enemyType = enemyType
        self.health = health
        self.max_health = health
        self.attackDamages = argsv
        self.unknown = unknown
        self.tired = False
        self.vulnerable = False
    def damage(self, amount, attackingCaster):
        print(self.enemyType,'took',amount*attackingCaster.damage_multiplier,'damage')
        damageDealt = min(self.health, amount*attackingCaster.damage_multiplier)
        self.health -=damageDealt
        return damageDealt
    def is_alive(self):
        return self.health>0