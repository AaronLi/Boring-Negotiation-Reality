class PlayerParty:
    def __init__(self, members = None) -> None:
        self.members = members if members is not None else []
        self.current_caster_index = 0

    @property
    def current_caster(self):
        return self.members[self.current_caster_index]

    @property
    def party_leader(self):
        return self.members[0]

    def find_next_caster(self):
        assert self.can_attack
        active_casters = [i for i,member in enumerate(self.members) if member.can_attack()]
        self.current_caster_index = active_casters[0]
        return self.current_caster

    @property
    def can_attack(self):
        return any([member.can_attack() for member in self.members])

    @property
    def defeated(self):
        return not any(member.is_alive() for member in self.members)

    def restore_all(self):
        for member in self.members:
            member.full_restore()

    def animations_done(self):
        return all([caster.animation_handler.animations_done() for caster in self.members])

    def get_member_index(self, member):
        return self.members.index(member)

    def start_turn(self):
        for party_member in self.members:
            party_member.set_defending(False)
            party_member.dodging = False
            party_member.tired = False
            party_member.injured = False
            party_member.regen_mana()

    def draw_party(self, surface):
        for playerNumber, playerInfo in enumerate(self.members):  # This is used for blitting the characters

            if playerInfo.is_alive():
                running_animations = [animation for animation in playerInfo.animation_handler.animations if animation.isRunning()]

                #double check that we aren't in some invalid state
                assert len(running_animations) <= 1

                if len(running_animations) == 0 or playerInfo.defend_animation in running_animations:  # draw non casting, standing player
                    if playerInfo.injured:
                        surface.blit(playerInfo.animation_handler.hurt, (325 - 15 * playerNumber, 20 + 190 * playerNumber))
                    else:
                        surface.blit(playerInfo.animation_handler.stance, (325 - 15 * playerNumber, 20 + 190 * playerNumber))

                for animation in running_animations:
                    animation.draw(surface, 325 - 15 * playerNumber,
                                                    20 + 190 * playerNumber)
                    animation.update()
                    if animation.isFinishedRunning():
                        animation.reset()
            else:
                surface.blit(playerInfo.animation_handler.dead, (325 - 15 * playerNumber, 20 + 190 * playerNumber))
