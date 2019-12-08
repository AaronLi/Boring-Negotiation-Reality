import caster, ability, animation
import json, pygame.image, pickle

class CastersLoader:
    def __init__(self, filepath, game_clock) -> None:
        self.filepath = filepath
        self.casters = {}
        self.loaded_files = {}

        with open(self.filepath) as f:
            data = json.load(f)

            for caster_name in data:
                print(caster_name)
                caster_info = data[caster_name]

                ability_info = caster_info['abilities']
                abilities = list(map(self.load_ability, ability_info))
                caster_attack_frames = caster_info['attack_animation']
                caster_attack_animation = self.load_animation(caster_attack_frames, game_clock)

                caster_spell_frames = caster_info['spell_animation']
                caster_spell_animation = self.load_animation(caster_spell_frames, game_clock)

                caster_defend_frames = caster_info['defend_animation']
                caster_defend_animation = self.load_animation(caster_defend_frames, game_clock)

                assert len(abilities) == 3

                self.casters[caster_name] = caster.Caster(caster_info['name'], caster_info['health'], caster_info['mana'], caster_info['attack_damage'], caster_info['caster_class'],
                                                          *abilities, caster_attack_animation, caster_spell_animation, caster_defend_animation, **caster_info['special_stats'])

    def load_ability(self, ability_info):
        callback_handle = pickle.loads(bytes(map(ord, ability_info['callback'])))
        print(callback_handle)
        return ability.Ability(ability_info['name'], ability_info['mana_cost'], ability_info['ability_type'], ability_info['influence_amount'], callback_handle)

    def load_animation(self,animation_info, game_clock):
        animation_frames = [self.try_load(i).convert_alpha() for i in animation_info['sprite_frames']]
        animation_duration = animation_info['animation_duration']
        return animation.Animation(animation_frames, animation_duration, game_clock)


    def try_load(self, file):
        cache_check = self.loaded_files.get(file)
        print('cache',"`%s`"%file,end=' ')
        if cache_check == None:
            cache_check = pygame.image.load(file).convert_alpha()
            self.loaded_files[file] = cache_check
            print('miss')
        else:
            print('hit')
        return cache_check