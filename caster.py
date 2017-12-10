class Caster:
    def __init__(self, name, health, mana, attack_damage, caster_class, ability1, ability2, ability3, animation, spellAnimation, defendAnimation, **kwargs):
        self.name=name
        self.health=health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self.attack_damage = attack_damage
        self.caster_class = caster_class
        self.abilities = [ability1, ability2, ability3]
        self.defending = False
        self.dodging = False
        self.tired=False
        self.targetable = True
        self.specialStats = kwargs
        self.damage_multiplier = 1
        self.animation = animation
        self.spellAnimation = spellAnimation
        self.defendAnimation = defendAnimation
    def regen_mana(self):
        self.mana = min(self.max_mana, self.mana+self.max_mana//5.8)
    def damage(self, amount):
        if self.dodging:
            pass
        elif self.defending:
            self.health = max(0, self.health - (amount // 2))
            self.defending = False
        else:
            self.health = max(0, self.health - amount)
    def heal(self, amount):
        self.health = min(self.max_health, self.health+amount)
    def set_special_stat(self, key, value):
        self.specialStats[key] = value
    def get_special_stat(self, key):
        return self.specialStats[key]
    def modify_special_stat(self, key, amount):
        self.specialStats[key]+=amount
    def is_alive(self):
        return self.health>0
    def can_attack(self):
        return (not self.tired) and self.is_alive()
    def set_defending(self, state):
        self.defending = state
        if self.defending:
            self.defendAnimation.reset()
    def __str__(self):
        return "%-8s hp:%4d/%d mana:%4d/%d %d %s %s"%(self.name, self.health,self.max_health, self.mana, self.max_mana, self.attack_damage, self.caster_class, str(self.abilities))

    def __lt__(self, other):
        return self.health < other.health
