import caster, ability, os
import json, pickle, glob
import src.caster_animation_handler as caster_animation_handler

class CastersLoader:
    def __init__(self, filepath, game_clock, image_cacher) -> None:
        self.filepath = filepath
        search_path = os.path.join(filepath, '*_stats.json')
        files = glob.iglob(search_path)
        self.casters = {}
        self.loaded_files = {}

        for file in files:
            print(file)
            with open(file) as f:
                caster_info = json.load(f)

                caster_name = caster_info['name']

                ability_info = caster_info['abilities']
                abilities = list(map(self.load_ability, ability_info))

                visual_data = caster_animation_handler.CasterVisualHandler(game_clock).load_from_file(caster_info['visual_data'], image_cacher)

                assert len(abilities) == 3

                self.casters[caster_name] = caster.Caster(caster_info['name'], caster_info['health'], caster_info['mana'], caster_info['attack_damage'], caster_info['caster_class'],
                                                          *abilities, visual_data, caster_info['story'], **caster_info['special_stats'])


    def load_ability(self, ability_info):
        callback_handle = pickle.loads(bytes(map(ord, ability_info['callback'])))
        print(callback_handle)
        return ability.Ability(ability_info['name'], ability_info['mana_cost'], ability_info['ability_type'], ability_info['influence_amount'], callback_handle)