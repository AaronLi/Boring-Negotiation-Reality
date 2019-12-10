class EffectEndedException(Exception):
    pass

class StatusEffect:
    def __init__(self, name, duration, icon = None) -> None:
        self.name = name
        self.duration = duration
        self.icon = icon

    def is_finished(self):
        return self.duration <= 0

    def step(self):
        if self.is_finished():
            raise EffectEndedException()
        self.duration-=1



class DOTEffect(StatusEffect):
    def __init__(self, name, duration, influence_amount, icon=None) -> None:
        super().__init__(name, duration, icon)
        self.influence_amount = influence_amount

