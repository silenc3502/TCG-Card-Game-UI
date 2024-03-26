import queue

from notify_reader.service.notify_read_handler import NotifyReadHandler


class AnimationActionCheckRepository:
    __instance = None
    __is_play_animation = False

    notify_read_handler = NotifyReadHandler.getInstance()

    notify_queue = queue.Queue()
    # notify_reader_service = NotifyReaderServiceImpl.getInstance()

    # notify_callback_table = {}
    # notify_callback_table['NOTIFY_DEPLOY_UNIT'] = notify_deploy_unit
    # notify_callback_table['NOTIFY_TURN_END'] = notify_turn_end
    # notify_callback_table['NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT'] = notify_attach_general_energy_card
    # notify_callback_table['NOTIFY_USE_SPECIAL_ENERGY_CARD_TO_UNIT'] = notify_use_special_energy_card_to_unit
    # notify_callback_table['NOTIFY_USE_UNIT_ENERGY_REMOVE_ITEM_CARD'] = notify_use_unit_energy_remove_item_card
    # notify_callback_table['NOTIFY_BASIC_ATTACK_TO_MAIN_CHARACTER'] = damage_to_main_character
    # notify_callback_table['NOTIFY_USE_MULTIPLE_UNIT_DAMAGE_ITEM_CARD'] = notify_use_multiple_unit_damage_item_card
    # notify_callback_table['NOTIFY_USE_FIELD_ENERGY_REMOVE_ITEM_CARD'] = notify_use_field_energy_remove_item_card
    # notify_callback_table['NOTIFY_USE_INSTANT_UNIT_DEATH_ITEM_CARD'] = notify_use_instant_unit_death_item_card
    # notify_callback_table['NOTIFY_BASIC_ATTACK_TO_UNIT'] = damage_to_each_unit_by_basic_attack
    # notify_callback_table['NOTIFY_USE_SEARCH_DECK_SUPPORT_CARD'] = search_card
    # notify_callback_table['NOTIFY_USE_FIELD_ENERGY_TO_UNIT'] = notify_attach_field_energy_card
    # notify_callback_table['NOTIFY_TARGETING_ATTACK_ACTIVE_SKILL_TO_GAME_MAIN_CHARACTER'] = notify_targeting_attack_active_skill_to_main_character
    # notify_callback_table['NOTIFY_TARGETING_ATTACK_ACTIVE_SKILL_TO_UNIT'] = notify_targeting_attack_active_skill_to_your_unit
    # notify_callback_table['NOTIFY_NON_TARGETING_ACTIVE_SKILL'] = notify_non_targeting_active_skill
    # notify_callback_table['NOTIFY_USE_DRAW_SUPPORT_CARD'] = notify_use_draw_support_card
    # notify_callback_table['NOTIFY_MULLIGAN_END'] = notify_mulligan_end
    # notify_callback_table['NOTIFY_USE_CATASTROPHIC_DAMAGE_ITEM_CARD'] = notify_use_catastrophic_damage_item_card
    # notify_callback_table['NOTIFY_DEPLOY_TARGETING_ATTACK_PASSIVE_SKILL_TO_UNIT'] = notify_deploy_targeting_attack_passive_skill_to_unit
    # notify_callback_table['NOTIFY_DEPLOY_TARGETING_ATTACK_TO_GAME_MAIN_CHARACTER'] = notify_deploy_targeting_attack_to_game_main_character
    # notify_callback_table['NOTIFY_DEPLOY_NON_TARGETING_ATTACK_PASSIVE_SKILL'] = notify_deploy_non_targeting_attack_passive_skill
    # notify_callback_table['NOTIFY_TURN_START_TARGETING_ATTACK_PASSIVE_SKILL_TO_UNIT'] = notify_turn_start_targeting_attack_passive_skill_to_unit
    # notify_callback_table['NOTIFY_TURN_START_TARGETING_ATTACK_TO_GAME_MAIN_CHARACTER'] = notify_turn_start_targeting_attack_to_game_main_character
    # notify_callback_table['NOTIFY_TURN_START_NON_TARGETING_ATTACK_PASSIVE_SKILL'] = notify_turn_start_non_targeting_attack_passive_skill
    # notify_callback_table['NOTIFY_USE_FIELD_ENERGY_INCREASE_ITEM_CARD'] = notify_use_field_energy_increase_item_card
    # notify_callback_table['NOTIFY_SURRENDER'] = notify_surrender
    # notify_callback_table['NOTIFY_USE_UNIT_ENERGY_BOOST_SUPPORT_CARD'] = notify_use_unit_energy_boost_support

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def add_notify_data_to_queue(self, data):
        self.notify_queue.put(data)

    def set_is_play_animation(self, is_play_animation):
        self.__is_play_animation = is_play_animation

    def get_is_play_animation(self):
        return self.__is_play_animation

    def check_if_queue_has_data(self):
        return not self.notify_queue.empty()

    def process_data_from_queue(self):
        if not self.notify_queue.empty():
            self.set_is_play_animation(True)

            notify_data = self.notify_queue.get()
            # self.notify_read_handler.process_remain_notify_handler(notify_data)
            self.process_notify_data(notify_data)
        else:
            print("큐가 비었습니다.")

    def process_notify_data(self, notify_dict_data):
        notify_key = list(notify_dict_data.keys())[0]
        notify_callback_function = self.notify_read_handler.notify_callback_table[notify_key]
        notify_callback_function(notify_dict_data)
