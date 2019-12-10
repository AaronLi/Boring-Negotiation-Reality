class Party:
    def __init__(self, members = None) -> None:
        self.members = members if members is not None else []

    def restore_all(self):
        for member in self.members:
            member.full_restore()

    def animations_done(self):
        return all([caster.animation_handler.animations_done() for caster in self.members])

    def get_member_index(self, member):
        return self.members.index(member)

