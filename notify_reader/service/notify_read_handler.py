from colorama import Fore, Style

from battle_field.animation_support.animation_action import AnimationAction
from battle_field.animation_support.attack_animation import AttackAnimation
from battle_field.components.field_area_inside.field_area_inside_handler import FieldAreaInsideHandler
from battle_field.components.field_area_inside.turn_start_action import TurnStartAction
from battle_field.components.opponent_field_area_inside.opponent_field_area_action_process import \
    OpponentFieldAreaActionProcess
from battle_field.components.opponent_field_area_inside.opponent_field_area_inside_handler import \
    OpponentFieldAreaInsideHandler
from battle_field.components.opponent_field_area_inside.opponent_unit_action import OpponentUnitAction
from battle_field.entity.effect_animation import EffectAnimation
from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field.infra.opponent_field_energy_repository import OpponentFieldEnergyRepository
from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.opponent_hand_repository import OpponentHandRepository
from battle_field.infra.opponent_tomb_repository import OpponentTombRepository
from battle_field.infra.your_deck_repository import YourDeckRepository
from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from battle_field.infra.your_hp_repository import YourHpRepository
from battle_field.infra.your_tomb_repository import YourTombRepository
from battle_field.state.energy_type import EnergyType
from battle_field_muligun.infra.muligun_your_hand_repository import MuligunYourHandRepository
from common.message_number import MessageNumber
from common.target_type import TargetType
from image_shape.circle_kinds import CircleKinds
from image_shape.non_background_number_image import NonBackgroundNumberImage
from music_player.repository.music_player_repository_impl import MusicPlayerRepositoryImpl
from notify_reader.entity.notice_type import NoticeType
from notify_reader.repository.notify_reader_repository_impl import NotifyReaderRepositoryImpl
from notify_reader.service.request.effect_animation_request import EffectAnimationRequest
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class NotifyReadHandler:
    __instance = None

    notify_callback_table = {}

    __battle_field_repository = BattleFieldRepository.getInstance()
    __opponent_field_unit_repository = OpponentFieldUnitRepository.getInstance()
    __music_player_repository = MusicPlayerRepositoryImpl.getInstance()
    __card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()
    __opponent_field_area_inside_handler = OpponentFieldAreaInsideHandler.getInstance()
    __notify_reader_repository = NotifyReaderRepositoryImpl.getInstance()
    __your_deck_repository = YourDeckRepository.getInstance()
    __your_hand_repository = YourHandRepository.getInstance()
    __field_area_inside_handler = FieldAreaInsideHandler.getInstance()
    __pre_drawed_image_instance = PreDrawedImage.getInstance()
    __attack_animation_object = AttackAnimation.getInstance()
    __your_hp_repository = YourHpRepository.getInstance()
    __opponent_hand_repository = OpponentHandRepository.getInstance()
    __opponent_tomb_repository = OpponentTombRepository.getInstance()
    __your_field_unit_repository = YourFieldUnitRepository.getInstance()
    __opponent_field_energy_repository = OpponentFieldEnergyRepository.getInstance()
    __your_tomb_repository = YourTombRepository.getInstance()
    __your_field_energy_repository = YourFieldEnergyRepository.getInstance()
    __mulligan_repository = MuligunYourHandRepository.getInstance()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

            cls.__instance.notify_callback_table['NOTIFY_DEPLOY_UNIT'] = cls.__instance.notify_deploy_unit
            cls.__instance.notify_callback_table['NOTIFY_TURN_END'] = cls.__instance.notify_turn_end
            cls.__instance.notify_callback_table['NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT'] = cls.__instance.notify_attach_general_energy_card
            cls.__instance.notify_callback_table['NOTIFY_USE_SPECIAL_ENERGY_CARD_TO_UNIT'] = cls.__instance.notify_use_special_energy_card_to_unit
            cls.__instance.notify_callback_table['NOTIFY_USE_UNIT_ENERGY_REMOVE_ITEM_CARD'] = cls.__instance.notify_use_unit_energy_remove_item_card
            cls.__instance.notify_callback_table['NOTIFY_BASIC_ATTACK_TO_MAIN_CHARACTER'] = cls.__instance.damage_to_main_character
            cls.__instance.notify_callback_table['NOTIFY_USE_MULTIPLE_UNIT_DAMAGE_ITEM_CARD'] = cls.__instance.notify_use_multiple_unit_damage_item_card
            cls.__instance.notify_callback_table['NOTIFY_USE_FIELD_ENERGY_REMOVE_ITEM_CARD'] = cls.__instance.notify_use_field_energy_remove_item_card
            cls.__instance.notify_callback_table['NOTIFY_USE_INSTANT_UNIT_DEATH_ITEM_CARD'] = cls.__instance.notify_use_instant_unit_death_item_card
            cls.__instance.notify_callback_table['NOTIFY_BASIC_ATTACK_TO_UNIT'] = cls.__instance.damage_to_each_unit_by_basic_attack
            cls.__instance.notify_callback_table['NOTIFY_USE_SEARCH_DECK_SUPPORT_CARD'] = cls.__instance.search_card
            cls.__instance.notify_callback_table['NOTIFY_USE_FIELD_ENERGY_TO_UNIT'] = cls.__instance.notify_attach_field_energy_card
            cls.__instance.notify_callback_table['NOTIFY_TARGETING_ATTACK_ACTIVE_SKILL_TO_GAME_MAIN_CHARACTER'] = cls.__instance.notify_targeting_attack_active_skill_to_main_character
            cls.__instance.notify_callback_table['NOTIFY_TARGETING_ATTACK_ACTIVE_SKILL_TO_UNIT'] = cls.__instance.notify_targeting_attack_active_skill_to_your_unit
            cls.__instance.notify_callback_table['NOTIFY_NON_TARGETING_ACTIVE_SKILL'] = cls.__instance.notify_non_targeting_active_skill
            cls.__instance.notify_callback_table['NOTIFY_USE_DRAW_SUPPORT_CARD'] = cls.__instance.notify_use_draw_support_card
            cls.__instance.notify_callback_table['NOTIFY_MULLIGAN_END'] = cls.__instance.notify_mulligan_end
            cls.__instance.notify_callback_table['NOTIFY_USE_CATASTROPHIC_DAMAGE_ITEM_CARD'] = cls.__instance.notify_use_catastrophic_damage_item_card
            cls.__instance.notify_callback_table['NOTIFY_DEPLOY_TARGETING_ATTACK_PASSIVE_SKILL_TO_UNIT'] = cls.__instance.notify_deploy_targeting_attack_passive_skill_to_unit
            cls.__instance.notify_callback_table['NOTIFY_DEPLOY_TARGETING_ATTACK_TO_GAME_MAIN_CHARACTER'] = cls.__instance.notify_deploy_targeting_attack_to_game_main_character
            cls.__instance.notify_callback_table['NOTIFY_DEPLOY_NON_TARGETING_ATTACK_PASSIVE_SKILL'] = cls.__instance.notify_deploy_non_targeting_attack_passive_skill
            cls.__instance.notify_callback_table['NOTIFY_TURN_START_TARGETING_ATTACK_PASSIVE_SKILL_TO_UNIT'] = cls.__instance.notify_turn_start_targeting_attack_passive_skill_to_unit
            cls.__instance.notify_callback_table['NOTIFY_TURN_START_TARGETING_ATTACK_TO_GAME_MAIN_CHARACTER'] = cls.__instance.notify_turn_start_targeting_attack_to_game_main_character
            cls.__instance.notify_callback_table['NOTIFY_TURN_START_NON_TARGETING_ATTACK_PASSIVE_SKILL'] = cls.__instance.notify_turn_start_non_targeting_attack_passive_skill
            cls.__instance.notify_callback_table['NOTIFY_USE_FIELD_ENERGY_INCREASE_ITEM_CARD'] = cls.__instance.notify_use_field_energy_increase_item_card
            cls.__instance.notify_callback_table['NOTIFY_SURRENDER'] = cls.__instance.notify_surrender
            cls.__instance.notify_callback_table['NOTIFY_USE_UNIT_ENERGY_BOOST_SUPPORT_CARD'] = cls.__instance.notify_use_unit_energy_boost_support

        return cls.__instance

    def notify_deploy_unit(self, notice_dictionary):
        print(f"notify_deploy_unit() -> notice_dictionary: {notice_dictionary}")

        #
        # print(f"{Fore.RED}notify_deploy_unit() -> whose_turn True(Your) or False(Opponent):{Fore.GREEN} {whose_turn}{Style.RESET_ALL}")
        #
        # if whose_turn is True:
        #     # self.__notify_reader_repository.set_is_your_turn_for_check_fake_process(not whose_turn)
        #     # print(f"after set whose_turn: {self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()}")
        #     return

        card_id = (notice_dictionary.get('NOTIFY_DEPLOY_UNIT', {})
                   .get('player_hand_use_map', {})
                   .get('Opponent', {})
                   .get('card_id', None))

        print(f"{Fore.RED}notify_deploy_unit() -> Opponent deploy card_id:{Fore.GREEN} {card_id}{Style.RESET_ALL}")

        self.__battle_field_repository.set_current_use_card_id(card_id)

        def deploy_unit(card_id):
            self.__opponent_field_unit_repository.create_field_unit_card(card_id)
            self.__music_player_repository.play_sound_effect_of_unit_deploy(str(card_id))
            # self.__opponent_field_unit_repository.place_field_unit(card_id)

            self.__opponent_field_unit_repository.replace_opponent_field_unit_card_position()
            recently_added_card_index = self.__opponent_field_unit_repository.get_field_unit_max_index()

            passive_skill_type = self.__card_info_repository.getCardPassiveFirstForCardNumber(card_id)
            if passive_skill_type == 2:
                print("광역기")

                # # self.__opponent_field_area_action = OpponentFieldAreaActionProcess.REQUIRED_FIRST_PASSIVE_SKILL_PROCESS
                # if card_id == 19:
                #     opponent_animation_actor = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(recently_added_card_index)
                #     self.__attack_animation_object.set_opponent_animation_actor(opponent_animation_actor)
                #     # self.__opponent_field_area_inside_handler.set_field_area_action(OpponentFieldAreaActionProcess.PLAY_ANIMATION)
                #     # self.__opponent_field_area_inside_handler.set_field_area_action(OpponentFieldAreaActionProcess.REQUIRED_FIRST_PASSIVE_SKILL_PROCESS)
                #
                #     damage = self.__card_info_repository.getCardPassiveFirstDamageForCardNumber(opponent_animation_actor.get_card_number())
                #     self.__attack_animation_object.set_opponent_animation_actor_damage(damage)
                #
                #     self.__opponent_field_area_inside_handler.set_unit_action(OpponentUnitAction.NETHER_BLADE_FIRST_WIDE_AREA_PASSIVE_SKILL)
                #
                #     extra_ability = self.__opponent_field_unit_repository.get_opponent_unit_extra_ability_at_index(recently_added_card_index)
                #     self.__attack_animation_object.set_extra_ability(extra_ability)
                #
                #     self.__opponent_field_area_inside_handler.set_active_field_area_action(OpponentFieldAreaActionProcess.PLAY_ANIMATION)
                #
                #     process_first_passive_skill_response = self.__fake_battle_field_frame_repository.request_to_process_first_passive_skill(
                #         WideAreaPassiveSkillFromDeployRequest(
                #             _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                #             _unitCardIndex=str(recently_added_card_index),
                #             _usageSkillIndex="1"))
                #
                #     is_success = process_first_passive_skill_response['is_success']
                #     if is_success is False:
                #         return FieldAreaAction.Dummy

                return


            elif passive_skill_type == 1:
                print("단일기")

                self.__opponent_field_area_inside_handler.set_field_area_action(
                    OpponentFieldAreaActionProcess.REQUIRED_FIRST_PASSIVE_SKILL_PROCESS)
                return

        if card_id == 19:
            effect_animation = EffectAnimation()
            effect_animation.set_animation_name('nether_blade_scene')
            self.__notify_reader_repository.save_notify_effect_animation_request(
                EffectAnimationRequest(
                    effect_animation=effect_animation,
                    target_player='Opponent',
                    target_index=99999,
                    target_type=TargetType.FULL_SCREEN,
                    call_function=deploy_unit,
                    function_need_param=True,
                    param=card_id,
                    need_dalay=True
                )
            )
        else:
            deploy_unit(card_id)

        return

    # {"NOTIFY_DEPLOY_NON_TARGETING_ATTACK_PASSIVE_SKILL": {"player_field_unit_health_point_map": {
    #     "You": {"field_unit_health_point_map": {"1": 0, "3": 10, "4": 5, "5": 10, "0": 0, "2": 10}}},
    #                                                       "player_field_unit_harmful_effect_map": {"You": {
    #                                                           "field_unit_harmful_status_map": {
    #                                                               "2": {"harmful_status_list": []},
    #                                                               "0": {"harmful_status_list": []},
    #                                                               "4": {"harmful_status_list": []},
    #                                                               "1": {"harmful_status_list": []},
    #                                                               "3": {"harmful_status_list": []},
    #                                                               "5": {"harmful_status_list": []}}}},
    #                                                       "player_field_unit_death_map": {
    #                                                           "You": {"dead_field_unit_index_list": [0, 1]}}}}
    def notify_deploy_non_targeting_passive_skill_attack(self, notice_dictionary):
        print(
            f"{Fore.RED}notify_deploy_non_targeting_passive_skill_attack() -> notice_dictionary:{Fore.GREEN} {notice_dictionary}{Style.RESET_ALL}")

        # self.__opponent_field_area_inside_handler.set_active_field_area_action(OpponentFieldAreaActionProcess.PLAY_ANIMATION)
        self.__opponent_field_area_inside_handler.set_field_area_action(
            OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_PASSIVE_SKILL_PROCESS)

    def notify_turn_end(self, notice_dictionary):
        print(f"{Fore.RED}notify_turn_end() -> notice_dictionary:{Fore.GREEN} {notice_dictionary}{Style.RESET_ALL}")

        self.__notify_reader_repository.save_notify_message_on_screen(
            MessageNumber.YOUR_TURN.value)

        # Deck Update
        print(
            f"{Fore.RED}before draw current_deck: {Fore.GREEN}{self.__your_deck_repository.get_current_deck_state()}{Style.RESET_ALL}")
        self.__your_deck_repository.draw_deck()
        print(
            f"{Fore.RED}after draw current_deck: {Fore.GREEN}{self.__your_deck_repository.get_current_deck_state()}{Style.RESET_ALL}")

        # Your Draw
        your_drawn_card_list = notice_dictionary['NOTIFY_TURN_END']['player_drawn_card_list_map'].get('You', [])
        self.__your_hand_repository.save_current_hand_state(your_drawn_card_list)
        self.__your_hand_repository.update_your_hand()

        your_field_energy = notice_dictionary['NOTIFY_TURN_END']['player_field_energy_map'].get('You', [])
        self.__your_field_energy_repository.set_your_field_energy(your_field_energy)
        print(f"{Fore.RED}notify_turn_end() -> your_field_energy:{Fore.GREEN} {your_field_energy}{Style.RESET_ALL}")

        self.apply_notify_data_of_harmful_status(
            notice_dictionary['NOTIFY_TURN_END']['player_field_unit_harmful_effect_map'])

        self.apply_notify_data_of_field_unit_hp(
            notice_dictionary['NOTIFY_TURN_END']['player_field_unit_health_point_map'])

        self.apply_notify_data_of_dead_unit(notice_dictionary['NOTIFY_TURN_END']['player_field_unit_death_map'])

        your_which_one_has_passive_skill_to_turn_start_lists = {unit_index: passive_list for unit_index, passive_list in
                                                                notice_dictionary['NOTIFY_TURN_END'][
                                                                    'unit_index_turn_start_passive_list_map'].items() if
                                                                passive_list}
        print(
            f"{Fore.RED}your_which_one_has_passive_skill_to_turn_start_lists:{Fore.GREEN} {your_which_one_has_passive_skill_to_turn_start_lists}{Style.RESET_ALL}")

        required_to_process_passive_skill_multiple_unit_list = []
        for key, value in your_which_one_has_passive_skill_to_turn_start_lists.items():
            required_to_process_passive_skill_multiple_unit_list.append(key)

        self.__field_area_inside_handler.set_field_turn_start_action(
            TurnStartAction.CHECK_MULTIPLE_UNIT_REQUIRED_FIRST_PASSIVE_SKILL_PROCESS)
        self.__field_area_inside_handler.set_required_to_process_passive_skill_multiple_unit_list(
            required_to_process_passive_skill_multiple_unit_list)

    def notify_attach_general_energy_card(self, notice_dictionary):

        print(f"{Fore.RED}notify_attach_general_energy_card() -> notice_dictionary:{Fore.GREEN} {notice_dictionary}{Style.RESET_ALL}")

        # fake_opponent_field_unit_energy_map = notice_dictionary['NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT']['player_field_unit_energy_map']['Opponent']
        # print(f"{Fore.RED}fake_opponent_field_unit_energy_map:{Fore.GREEN} {fake_opponent_field_unit_energy_map}{Style.RESET_ALL}")
        self.__battle_field_repository.set_current_use_card_id(93)

        for unit_index, unit_value in \
                notice_dictionary['NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT']['player_field_unit_energy_map']['Opponent'][
                    'field_unit_energy_map'].items():
            print(f"{Fore.RED}opponent_unit_index:{Fore.GREEN} {unit_index}{Style.RESET_ALL}")
            print(f"{Fore.RED}opponent_unit_value:{Fore.GREEN} {unit_value}{Style.RESET_ALL}")

            # opponent_unit_attached_undead_energy_count = unit_value['attached_energy_map']['2']

            for race_energy_number, race_energy_count in unit_value['attached_energy_map'].items():
                print(f"{Fore.RED}energy_key:{Fore.GREEN} {race_energy_number}{Style.RESET_ALL}")
                print(f"{Fore.RED}energy_count:{Fore.GREEN} {race_energy_count}{Style.RESET_ALL}")

                before_race_energy = self.__opponent_field_unit_repository.get_opponent_field_unit_race_energy(
                    int(unit_index), EnergyType.Undead
                )

                energy_diff = race_energy_count - before_race_energy

                self.__opponent_field_unit_repository.attach_race_energy(int(unit_index), EnergyType.Undead,
                                                                         energy_diff)

                opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
                    int(unit_index))

                opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                total_energy_count = unit_value['total_energy_count']
                print(f"{Fore.RED}total_energy_count:{Fore.GREEN} {total_energy_count}{Style.RESET_ALL}")

                for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                    if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                        if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                            opponent_fixed_card_attached_shape.set_image_data(
                                self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                                    total_energy_count))

    def damage_to_main_character(self, notice_dictionary):
        notify_dict_data = notice_dictionary['NOTIFY_BASIC_ATTACK_TO_MAIN_CHARACTER']

        # {"NOTIFY_BASIC_ATTACK_TO_MAIN_CHARACTER": {"player_field_unit_attack_map": {"Opponent": {
        #     "field_unit_attack_map": {
        #         "1": {"target_player_index": "You", "target_unit_index": -1, "active_skill_index": -1,
        #               "passive_skill_index": -1}}}}, "player_main_character_health_point_map": {"You": 95},
        #                                            "player_main_character_survival_map": {"You": "Survival"}}}

        self.__opponent_field_area_inside_handler.set_active_field_area_action(
            OpponentFieldAreaActionProcess.PLAY_ANIMATION)
        self.__attack_animation_object.set_notify_data(notify_dict_data)

        self.__attack_animation_object.set_is_opponent_attack_main_character(True)

        survival_info = notify_dict_data['player_main_character_survival_map']['You']

        if survival_info == "Death":
            self.__your_hp_repository.your_character_die()

        opponent_attacker_unit_info = next(
            iter(notify_dict_data["player_field_unit_attack_map"]["Opponent"]["field_unit_attack_map"]))
        opponent_attacker_unit_index = int(opponent_attacker_unit_info)
        print(f"{Fore.RED}opponent_attacker_unit_index: {Fore.GREEN}{opponent_attacker_unit_index}{Style.RESET_ALL}")

        # target_unit_index = data["player_field_unit_attack_map"]["Opponent"]["field_unit_attack_map"][opponent_attacker_unit_index]["target_unit_index"]

        opponent_attacker_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
            opponent_attacker_unit_index)
        self.__attack_animation_object.set_opponent_animation_actor(opponent_attacker_unit)

        self.__opponent_field_area_inside_handler.set_field_area_action(
            OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_GENERAL_ATTACK_TO_MAIN_CHARACTER_PROCESS)

    def notify_use_multiple_unit_damage_item_card(self, notice_dictionary):

        data = notice_dictionary['NOTIFY_USE_MULTIPLE_UNIT_DAMAGE_ITEM_CARD']

        opponent_usage_card_info = (data)['player_hand_use_map']['Opponent']
        used_card_id = opponent_usage_card_info['card_id']

        self.__battle_field_repository.set_current_use_card_id(used_card_id)

        self.__attack_animation_object.set_notify_data(data)
        # 유저 관련 키값 대입
        self.__attack_animation_object.set_animation_action(AnimationAction.CORPSE_EXPLOSION)

    def search_card(self, notice_dictionary):
        notify_dict_data = notice_dictionary['NOTIFY_USE_SEARCH_DECK_SUPPORT_CARD']
        card_id = (notify_dict_data.get("player_hand_use_map", {})
                   .get("Opponent", {})
                   .get("card_id", None))

        self.__battle_field_repository.set_current_use_card_id(card_id)

        def call_of_leonic(notify_dict_data):
            search_count = (notify_dict_data.get("player_search_count_map", {})
                            .get("Opponent", None))

            fake_search_list = []
            for count in range(0, search_count):
                fake_search_list.append(-1)

            # self.__fake_opponent_hand_repository.save_fake_opponent_hand_list(fake_search_list)
            self.__opponent_hand_repository.save_current_opponent_hand_state(fake_search_list)

        effect_animation = EffectAnimation()
        effect_animation.set_animation_name('call_of_leonic')

        self.__notify_reader_repository.save_notify_effect_animation_request(
            EffectAnimationRequest(
                effect_animation=effect_animation,
                target_player='Opponent',
                target_index=99999,
                target_type=TargetType.AREA,
                call_function=call_of_leonic,
                function_need_param=True,
                param=notify_dict_data,
                need_dalay=True
            )
        )

        # self.__opponent_hand_repository.save_current_opponent_hand_state(fake_search_list)

    def damage_to_each_unit_by_basic_attack(self, notice_dictionary):

        # {"NOTIFY_BASIC_ATTACK_TO_UNIT": {"player_field_unit_attack_map": {"Opponent": {"field_unit_attack_map": {
        #     "2": {"target_player_index": "You", "target_unit_index": 3, "active_skill_index": -1,
        #           "passive_skill_index": -1}}}}, "player_field_unit_health_point_map": {
        #     "You": {"field_unit_health_point_map": {"3": 0}}, "Opponent": {"field_unit_health_point_map": {"2": 0}}},
        #                                  "player_field_unit_harmful_effect_map": {"Opponent": {
        #                                      "field_unit_harmful_status_map": {"2": {"harmful_status_list": []}}},
        #                                                                           "You": {
        #                                                                               "field_unit_harmful_status_map": {
        #                                                                                   "3": {
        #                                                                                       "harmful_status_list": []}}}},
        #                                  "player_field_unit_death_map": {
        #                                      "Opponent": {"dead_field_unit_index_list": [2]},
        #                                      "You": {"dead_field_unit_index_list": [3]}}}}

        # {"NOTIFY_BASIC_ATTACK_TO_UNIT": {"player_field_unit_attack_map": {"Opponent": {"field_unit_attack_map": {
        #     "0": {"target_player_index": "You", "target_unit_index": 0, "active_skill_index": -1,
        #           "passive_skill_index": -1}}}}, "player_field_unit_health_point_map": {
        #     "You": {"field_unit_health_point_map": {"0": 15}}, "Opponent": {"field_unit_health_point_map": {"0": 0}}},
        #                                  "player_field_unit_harmful_effect_map": {"You": {
        #                                      "field_unit_harmful_status_map": {"0": {"harmful_status_list": []}}},
        #                                                                           "Opponent": {
        #                                                                               "field_unit_harmful_status_map": {
        #                                                                                   "0": {
        #                                                                                       "harmful_status_list": []}}}},
        #                                  "player_field_unit_death_map": {
        #                                      "Opponent": {"dead_field_unit_index_list": [0]},
        #                                      "You": {"dead_field_unit_index_list": []}}}}

        data = notice_dictionary['NOTIFY_BASIC_ATTACK_TO_UNIT']
        self.__attack_animation_object.set_notify_data(data)

        is_opponent_data_in_data = False
        is_your_data_in_data = False

        self.apply_notify_data_of_harmful_status(data['player_field_unit_harmful_effect_map'])

        self.__attack_animation_object.set_is_opponent_attack_main_character(False)

        opponent_attacker_unit_info = next(
            iter(data["player_field_unit_attack_map"]["Opponent"]["field_unit_attack_map"]))
        opponent_attacker_unit_index = int(opponent_attacker_unit_info)
        print(f"{Fore.RED}opponent_attacker_unit_index: {Fore.GREEN}{opponent_attacker_unit_index}{Style.RESET_ALL}")

        # target_unit_index = data["player_field_unit_attack_map"]["Opponent"]["field_unit_attack_map"][opponent_attacker_unit_index]["target_unit_index"]

        opponent_attacker_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
            opponent_attacker_unit_index)
        self.__attack_animation_object.set_opponent_animation_actor(opponent_attacker_unit)

        self.__opponent_field_area_inside_handler.set_active_field_area_action(
            OpponentFieldAreaActionProcess.PLAY_ANIMATION)

        self.__opponent_field_area_inside_handler.set_field_area_action(
            OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_GENERAL_ATTACK_TO_YOUR_UNIT_PROCESS)

    def notify_attach_field_energy_card(self, notice_dictionary):

        self.__battle_field_repository.set_current_use_card_id(93)

        remain_opponent_field_energy = \
            notice_dictionary['NOTIFY_USE_FIELD_ENERGY_TO_UNIT']['player_field_energy_map']['Opponent']

        self.__opponent_field_energy_repository.set_opponent_field_energy(remain_opponent_field_energy)
        for unit_index, unit_value in \
                notice_dictionary['NOTIFY_USE_FIELD_ENERGY_TO_UNIT']['player_field_unit_energy_map']['Opponent'][
                    'field_unit_energy_map'].items():
            print(f"{Fore.RED}opponent_unit_index:{Fore.GREEN} {unit_index}{Style.RESET_ALL}")
            print(f"{Fore.RED}opponent_unit_value:{Fore.GREEN} {unit_value}{Style.RESET_ALL}")

            # opponent_unit_attached_undead_energy_count = unit_value['attached_energy_map']['2']

            for race_energy_number, race_energy_count in unit_value['attached_energy_map'].items():
                print(f"{Fore.RED}energy_key:{Fore.GREEN} {race_energy_number}{Style.RESET_ALL}")
                print(f"{Fore.RED}energy_count:{Fore.GREEN} {race_energy_count}{Style.RESET_ALL}")

                current_race_energy_count = self.__opponent_field_unit_repository.get_opponent_field_unit_race_energy(
                    int(unit_index), EnergyType.Undead)
                energy_difference = race_energy_count - current_race_energy_count

                self.__opponent_field_unit_repository.attach_race_energy(int(unit_index), EnergyType.Undead,
                                                                         energy_difference)

                opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
                    int(unit_index))

                opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                total_energy_count = unit_value['total_energy_count']
                print(f"{Fore.RED}total_energy_count:{Fore.GREEN} {total_energy_count}{Style.RESET_ALL}")

                for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                    if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                        if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                            opponent_fixed_card_attached_shape.set_image_data(
                                self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                                    total_energy_count))

    def notify_targeting_attack_active_skill_to_main_character(self, notice_dictionary):

        self.__opponent_field_area_inside_handler.set_active_field_area_action(
            OpponentFieldAreaActionProcess.PLAY_ANIMATION)

        notify_data = notice_dictionary['NOTIFY_TARGETING_ATTACK_ACTIVE_SKILL_TO_GAME_MAIN_CHARACTER']
        self.__attack_animation_object.set_notify_data(notify_data)

        self.__attack_animation_object.set_is_opponent_attack_main_character(True)

        survival_info = notify_data['player_main_character_survival_map']['You']

        if survival_info == "Death":
            self.__your_hp_repository.your_character_die()

        opponent_attacker_unit_info = next(
            iter(notify_data["player_field_unit_attack_map"]["Opponent"]["field_unit_attack_map"]))
        opponent_attacker_unit_index = int(opponent_attacker_unit_info)
        print(f"{Fore.RED}opponent_attacker_unit_index: {Fore.GREEN}{opponent_attacker_unit_index}{Style.RESET_ALL}")

        # target_unit_index = data["player_field_unit_attack_map"]["Opponent"]["field_unit_attack_map"][opponent_attacker_unit_index]["target_unit_index"]

        opponent_attacker_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
            opponent_attacker_unit_index)
        self.__attack_animation_object.set_opponent_animation_actor(opponent_attacker_unit)

        if opponent_attacker_unit.get_card_number() == 27:
            self.__opponent_field_area_inside_handler.set_field_area_action(
                OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_VALRN_ACTIVE_TARGETING_SKILL_TO_YOUR_MAIN_CHARACTER)

    def notify_targeting_attack_active_skill_to_your_unit(self, notice_dictionary):

        self.__opponent_field_area_inside_handler.set_active_field_area_action(
            OpponentFieldAreaActionProcess.PLAY_ANIMATION)
        data = notice_dictionary['NOTIFY_TARGETING_ATTACK_ACTIVE_SKILL_TO_UNIT']

        # {"NOTIFY_TARGETING_ATTACK_ACTIVE_SKILL_TO_UNIT": {"player_field_unit_attack_map": {"Opponent": {
        #     "field_unit_attack_map": {
        #         "2": {"target_player_index": "You", "target_unit_index": 0, "active_skill_index": 1,
        #               "passive_skill_index": -1}}}}, "player_field_unit_health_point_map": {
        #     "You": {"field_unit_health_point_map": {"0": 0}}}, "player_field_unit_harmful_effect_map": {
        #     "You": {"field_unit_harmful_status_map": {"0": {"harmful_status_list": []}}}},
        #                                                   "player_field_unit_death_map": {
        #                                                       "You": {"dead_field_unit_index_list": [0]}}}}

        self.__attack_animation_object.set_notify_data(data)

        self.__attack_animation_object.set_is_opponent_attack_main_character(False)

        opponent_attacker_unit_info = next(
            iter(data["player_field_unit_attack_map"]["Opponent"]["field_unit_attack_map"]))
        opponent_attacker_unit_index = int(opponent_attacker_unit_info)

        your_field_unit_index = \
        data["player_field_unit_attack_map"]["Opponent"]["field_unit_attack_map"][opponent_attacker_unit_info][
            'target_unit_index']
        your_field_unit = self.__your_field_unit_repository.find_field_unit_by_index(int(your_field_unit_index))
        self.__attack_animation_object.set_your_field_unit(your_field_unit)

        print(f"{Fore.RED}opponent_attacker_unit_index: {Fore.GREEN}{opponent_attacker_unit_index}{Style.RESET_ALL}")

        # target_unit_index = data["player_field_unit_attack_map"]["Opponent"]["field_unit_attack_map"][opponent_attacker_unit_index]["target_unit_index"]

        opponent_attacker_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
            opponent_attacker_unit_index)
        self.__attack_animation_object.set_opponent_animation_actor(opponent_attacker_unit)

        if opponent_attacker_unit.get_card_number() == 27:
            self.__opponent_field_area_inside_handler.set_field_area_action(
                OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_VALRN_ACTIVE_TARGETING_SKILL_TO_YOUR_UNIT)

    def notify_non_targeting_active_skill(self, notice_dictionary):

        self.__opponent_field_area_inside_handler.set_active_field_area_action(
            OpponentFieldAreaActionProcess.PLAY_ANIMATION)
        data = notice_dictionary['NOTIFY_NON_TARGETING_ACTIVE_SKILL']
        self.__attack_animation_object.set_notify_data(data)

        self.__attack_animation_object.set_is_opponent_attack_main_character(False)

        opponent_attacker_unit_info = next(
            iter(data["player_field_unit_attack_map"]["Opponent"]["field_unit_attack_map"]))
        opponent_attacker_unit_index = int(opponent_attacker_unit_info)
        print(f"{Fore.RED}opponent_attacker_unit_index: {Fore.GREEN}{opponent_attacker_unit_index}{Style.RESET_ALL}")

        # target_unit_index = data["player_field_unit_attack_map"]["Opponent"]["field_unit_attack_map"][opponent_attacker_unit_index]["target_unit_index"]

        opponent_attacker_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
            opponent_attacker_unit_index)
        self.__attack_animation_object.set_opponent_animation_actor(opponent_attacker_unit)

        if opponent_attacker_unit.get_card_number() == 27:
            self.__opponent_field_area_inside_handler.set_field_area_action(
                OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_VALRN_ACTIVE_NON_TARGETING_SKILL_TO_YOUR_FIELD)

    def notify_use_special_energy_card_to_unit(self, notice_dictionary):

        # 일단은 opponent 밖에 없으니 아래와 같이 처리할 수 있음
        data = notice_dictionary['NOTIFY_USE_SPECIAL_ENERGY_CARD_TO_UNIT']

        opponent_usage_card_info = (
            data)['player_hand_use_map']['Opponent']
        opponent_field_unit_energy_map = (
            data)['player_field_unit_energy_map']['Opponent']['field_unit_energy_map']
        opponent_field_unit_extra_effect_map = (
            data)['player_field_unit_extra_effect_map']['Opponent']['field_unit_extra_effect_map']

        # 사용된 카드 묘지로 보냄
        used_card_id = opponent_usage_card_info['card_id']
        self.__opponent_tomb_repository.create_opponent_tomb_card(used_card_id)
        self.__battle_field_repository.set_current_use_card_id(used_card_id)

        for opponent_unit_index, opponent_unit_energy_info in opponent_field_unit_energy_map.items():
            print(f"{Fore.RED}opponent_unit_index:{Fore.GREEN} {opponent_unit_index}{Style.RESET_ALL}")
            print(f"{Fore.RED}opponent_unit_energy_info:{Fore.GREEN} {opponent_unit_energy_info}{Style.RESET_ALL}")

            for race_energy_number, race_energy_count in opponent_unit_energy_info['attached_energy_map'].items():
                extra_effect_list = opponent_field_unit_extra_effect_map[str(opponent_unit_index)]['extra_effect_list']
                print(f"{Fore.RED}race_energy_number:{Fore.GREEN} {race_energy_number}{Style.RESET_ALL}")
                print(f"{Fore.RED}race_energy_count:{Fore.GREEN} {race_energy_count}{Style.RESET_ALL}")
                print(f"{Fore.RED}extra_effect_list:{Fore.GREEN} {extra_effect_list}{Style.RESET_ALL}")

                # if race_energy_number == EnergyType.Undead.value:

                current_opponent_field_unit_race_energy_count = (
                    self.__opponent_field_unit_repository.get_opponent_field_unit_race_energy(
                        int(opponent_unit_index), EnergyType(int(race_energy_number))))
                print(f"{Fore.RED}current_opponent_field_unit_race_energy_count:{Fore.GREEN}"
                      f" {current_opponent_field_unit_race_energy_count}{Style.RESET_ALL}")

                self.__opponent_field_unit_repository.attach_race_energy(
                    int(opponent_unit_index),
                    EnergyType(int(race_energy_number)),
                    (race_energy_count - current_opponent_field_unit_race_energy_count))

                # TODO: String 이 아닌 Enum 으로 처리해야 함
                self.__opponent_field_unit_repository.update_opponent_unit_extra_effect_at_index(
                    int(opponent_unit_index), extra_effect_list)

                opponent_field_unit = (
                    self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(int(opponent_unit_index)))

                opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                total_energy_count = opponent_unit_energy_info['total_energy_count']
                print(f"{Fore.RED}total_energy_count:{Fore.GREEN} {total_energy_count}{Style.RESET_ALL}")

                for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                    if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                        if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                            opponent_fixed_card_attached_shape.set_image_data(
                                self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                                    total_energy_count))

                        # TODO: 특수 효과에 맞는 이미지 Setting
                        # if 'DarkFire' in extra_effect_list:
                        #     print("set_image_data: dark_fire")
                        #     opponent_fixed_card_attached_shape.set_image_data(
                        #         self.__pre_drawed_image_instance.get_pre_draw_dark_flame_energy())
                        # if 'Freeze' in extra_effect_list:
                        #     print("set_image_data: freeze")
                        #     opponent_fixed_card_attached_shape.set_image_data(
                        #         self.__pre_drawed_image_instance.get_pre_draw_freezing_energy())

    def analyze_notify_data_of_field_unit_energy(self, player_field_unit_energy_data):
        try:
            for player, field_unit_energy_map in player_field_unit_energy_data.items():
                for unit_index, attached_energy_map in field_unit_energy_map['field_unit_energy_map'].items():
                    for energy_race, energy_count in attached_energy_map.get('attached_energy_map', {}).items():
                        total_energy_count = attached_energy_map.get('total_energy_count', 0)

                        if player == 'You':
                            self.apply_notify_data_of_your_field_unit_energy(int(unit_index), energy_count,
                                                                             total_energy_count)
                        elif player == 'Opponent':
                            self.apply_notify_data_of_opponent_field_unit_energy(int(unit_index), energy_count,
                                                                                 total_energy_count)
                        else:
                            print('Target error: Target is not "You" or "Opponent"')

        except Exception as e:
            print('apply_notify_data_of_your_field_unit_energy error! ', e)

    def apply_notify_data_of_your_field_unit_energy(self, unit_index, race_energy_count, total_energy_count):
        self.__your_field_unit_repository.attach_race_energy(unit_index, EnergyType.Undead, race_energy_count)

        your_field_unit = self.__your_field_unit_repository.find_your_field_unit_by_index(unit_index)

        your_fixed_card_base = your_field_unit.get_fixed_card_base()
        your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

        print(f"{Fore.RED}total_energy_count:{Fore.GREEN} {total_energy_count}{Style.RESET_ALL}")

        for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
            if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                    your_fixed_card_attached_shape.set_number(total_energy_count)
                    your_fixed_card_attached_shape.set_image_data(
                        self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                            total_energy_count))

    def apply_notify_data_of_opponent_field_unit_energy(self, unit_index, race_energy_count, total_energy_count):
        self.__opponent_field_unit_repository.attach_race_energy(unit_index, EnergyType.Undead, race_energy_count)

        opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(unit_index)

        opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
        opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

        print(f"{Fore.RED}total_energy_count:{Fore.GREEN} {total_energy_count}{Style.RESET_ALL}")

        for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
            if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                    opponent_fixed_card_attached_shape.set_number(total_energy_count)
                    opponent_fixed_card_attached_shape.set_image_data(
                        self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                            total_energy_count))

    def apply_notify_data_of_field_unit_hp(self, player_field_unit_health_point_data):
        print('apply notify data of field unit hp!! : ', player_field_unit_health_point_data)

        for player, hp_map in player_field_unit_health_point_data.items():
            for unit_index, remain_hp in hp_map['field_unit_health_point_map'].items():
                if remain_hp <= 0:
                    continue

                if player == 'You':
                    field_unit = self.__your_field_unit_repository.find_field_unit_by_index(int(unit_index))
                    fixed_card_base = field_unit.get_fixed_card_base()
                    fixed_card_attached_shape_list = fixed_card_base.get_attached_shapes()

                    for fixed_card_attached_shape in fixed_card_attached_shape_list:
                        if isinstance(fixed_card_attached_shape, NonBackgroundNumberImage):
                            if fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                fixed_card_attached_shape.set_number(remain_hp)
                                fixed_card_attached_shape.set_image_data(
                                    self.__pre_drawed_image_instance.get_pre_draw_unit_hp(remain_hp))

                elif player == 'Opponent':
                    field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
                        int(unit_index))
                    fixed_card_base = field_unit.get_fixed_card_base()
                    fixed_card_attached_shape_list = fixed_card_base.get_attached_shapes()

                    for fixed_card_attached_shape in fixed_card_attached_shape_list:
                        if isinstance(fixed_card_attached_shape, NonBackgroundNumberImage):
                            if fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                fixed_card_attached_shape.set_number(remain_hp)
                                fixed_card_attached_shape.set_image_data(
                                    self.__pre_drawed_image_instance.get_pre_draw_unit_hp(remain_hp))

    def apply_notify_data_of_dead_unit(self, player_field_unit_death_data):

        for player, dead_field_unit_index_list_map in player_field_unit_death_data.items():
            dead_field_unit_index_list = dead_field_unit_index_list_map.get('dead_field_unit_index_list', [])
            if len(dead_field_unit_index_list) == 0:
                continue

            if player == 'You':
                for unit_index in dead_field_unit_index_list:
                    def remove_field_unit(unit_index):
                        card_id = self.__your_field_unit_repository.get_card_id_by_index(unit_index)
                        self.__your_tomb_repository.create_tomb_card(card_id)
                        self.__your_field_unit_repository.remove_card_by_index(unit_index)
                        self.__your_field_unit_repository.remove_harmful_status_by_index(unit_index)
                        self.__your_field_unit_repository.replace_field_card_position()

                    effect_animation = EffectAnimation()
                    effect_animation.set_animation_name('death')
                    effect_animation.change_local_translation(
                        self.__your_field_unit_repository.find_field_unit_by_index(
                            unit_index).get_fixed_card_base().get_local_translation())
                    effect_animation.draw_animation_panel()

                    self.__notify_reader_repository.save_notify_effect_animation_request(
                        EffectAnimationRequest(
                            effect_animation=effect_animation,
                            target_player=player,
                            target_index=unit_index,
                            target_type=TargetType.UNIT,
                            call_function=remove_field_unit,
                            function_need_param=True,
                            param=unit_index
                        )
                    )
            elif player == 'Opponent':
                for unit_index in dead_field_unit_index_list:
                    def remove_field_unit(unit_index):
                        card_id = self.__opponent_field_unit_repository.get_opponent_card_id_by_index(unit_index)
                        self.__opponent_tomb_repository.create_opponent_tomb_card(card_id)
                        self.__opponent_field_unit_repository.remove_current_field_unit_card(unit_index)
                        self.__opponent_field_unit_repository.remove_harmful_status_by_index(unit_index)

                        self.__opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                    effect_animation = EffectAnimation()
                    effect_animation.set_animation_name('death')
                    effect_animation.change_local_translation(
                        self.__opponent_field_unit_repository.find_field_unit_by_index(
                            unit_index).get_fixed_card_base().get_local_translation())
                    effect_animation.draw_animation_panel()

                    self.__notify_reader_repository.save_notify_effect_animation_request(
                        EffectAnimationRequest(
                            effect_animation=effect_animation,
                            target_player=player,
                            target_index=unit_index,
                            target_type=TargetType.UNIT,
                            call_function=remove_field_unit,
                            function_need_param=True,
                            param=unit_index
                        )
                    )

            else:
                print(f'apply_notify_data_of_dead_unit error : unknown player {player}')

    def apply_notify_data_of_harmful_status(self, player_field_unit_harmful_effect_data):

        try:
            for player, field_data in player_field_unit_harmful_effect_data.items():
                for unit_index, harmful_status_value in field_data.get('field_unit_harmful_status_map', {}).items():
                    harmful_status_list = harmful_status_value.get('harmful_status_list', [])
                    if len(harmful_status_list) == 0:
                        continue

                    if player == 'Opponent':
                        self.__opponent_field_unit_repository.apply_harmful_status(int(unit_index), harmful_status_list)
                    elif player == 'You':
                        self.__your_field_unit_repository.apply_harmful_status(int(unit_index), harmful_status_list)
        except Exception as e:
            print('An error occurred while applying harmful status data:', e)

    def apply_notify_data_of_field_energy(self, player_field_energy_data):

        for player, field_energy_count in player_field_energy_data.items():
            if player == 'You':
                self.__your_field_energy_repository.set_your_field_energy(field_energy_count)
            elif player == 'Opponent':
                self.__opponent_field_energy_repository.set_opponent_field_energy(field_energy_count)
            else:
                print('apply_notify_data_of_field_energy error! : unknown player ->', player)

    def notify_use_draw_support_card(self, notice_dictionary):
        data = notice_dictionary['NOTIFY_USE_DRAW_SUPPORT_CARD']

        opponent_usage_card_info = (
            data)['player_hand_use_map']['Opponent']

        # 사용된 카드 묘지로 보냄
        used_card_id = opponent_usage_card_info['card_id']
        self.__opponent_tomb_repository.create_opponent_tomb_card(used_card_id)
        self.__battle_field_repository.set_current_use_card_id(used_card_id)

        def opponent_draw_card(data):
            opponent_draw_count = (
                data)['player_draw_count_map']['Opponent']

            # 뒷면 카드 3장 추가
            unknown_hand_list = []
            for count in range(opponent_draw_count):
                unknown_hand_list.append(-1)

            current_opponent_hand = self.__opponent_hand_repository.get_current_opponent_hand_state()
            print(f"current_opponent_hand: {current_opponent_hand}")
            self.__opponent_hand_repository.save_current_opponent_hand_state(unknown_hand_list)

            updated_opponent_hand = self.__opponent_hand_repository.get_current_opponent_hand_state()
            print(f"updated_opponent_hand: {updated_opponent_hand}")

        effect_animation = EffectAnimation()
        effect_animation.set_animation_name('swamp_of_ghost')

        self.__notify_reader_repository.save_notify_effect_animation_request(
            EffectAnimationRequest(
                effect_animation=effect_animation,
                target_player='Opponent',
                target_index=99999,
                target_type=TargetType.AREA,
                call_function=opponent_draw_card,
                function_need_param=True,
                param=data,
                need_dalay=True
            )
        )

        # TODO: 상대 핸드 뒷면 이미지를 추가된 카드 장수 만큼 띄워야 함

    def notify_mulligan_end(self, notice_dictionary):
        is_opponent_mulligan = notice_dictionary['NOTIFY_MULLIGAN_END'].get('is_done')

        print(f"{Fore.RED}mulligan end?:{Fore.GREEN} {is_opponent_mulligan}{Style.RESET_ALL}")

        if is_opponent_mulligan is True:
            self.__mulligan_repository.set_is_opponent_mulligan(True)
        else:
            self.__mulligan_repository.set_is_opponent_mulligan(False)

    def notify_use_catastrophic_damage_item_card(self, notice_dictionary):

        data = notice_dictionary['NOTIFY_USE_CATASTROPHIC_DAMAGE_ITEM_CARD']
        self.__attack_animation_object.set_notify_data(data)

        opponent_usage_card_info = (data)['player_hand_use_map']['Opponent']
        used_card_id = opponent_usage_card_info['card_id']

        self.__battle_field_repository.set_current_use_card_id(used_card_id)

        self.__attack_animation_object.set_animation_action(AnimationAction.CONTRACT_OF_DOOM)
        print('파멸의 계약 준비됨')

    def notify_use_unit_energy_boost_support(self, notice_dictionary):
        data = notice_dictionary['NOTIFY_USE_UNIT_ENERGY_BOOST_SUPPORT_CARD']

        # 수신된 정보를 대입

        for key in data['player_hand_use_map']:
            player_who_use_card = key
            usage_card_deck_list_map = (
                data)['player_deck_card_use_list_map'][player_who_use_card]
            field_unit_energy_map = (
                data)['player_field_unit_energy_map'][player_who_use_card]['field_unit_energy_map']
            hand_use_card_id = data['player_hand_use_map'][player_who_use_card]['card_id']
            self.__battle_field_repository.set_current_use_card_id(hand_use_card_id)

            # 카드를 사용 하고, 묘지로 보냄
            for used_card_id in usage_card_deck_list_map:
                print(f"{Fore.RED}used_card_id:{Fore.GREEN} {used_card_id}{Style.RESET_ALL}")
                if player_who_use_card == "Opponent":
                    self.__opponent_tomb_repository.create_opponent_tomb_card(used_card_id)
                elif player_who_use_card == "You":
                    self.__your_tomb_repository.create_tomb_card(used_card_id)

            # 필드 유닛 에너지 정보 호출
            for unit_index, unit_value in \
                    notice_dictionary['NOTIFY_USE_UNIT_ENERGY_BOOST_SUPPORT_CARD']['player_field_unit_energy_map'][
                        player_who_use_card][
                        'field_unit_energy_map'].items():
                print(f"{Fore.RED}opponent_unit_index:{Fore.GREEN} {unit_index}{Style.RESET_ALL}")
                print(f"{Fore.RED}opponent_unit_value:{Fore.GREEN} {unit_value}{Style.RESET_ALL}")

                for race_energy_number, race_energy_count in unit_value['attached_energy_map'].items():
                    print(f"{Fore.RED}energy_key:{Fore.GREEN} {race_energy_number}{Style.RESET_ALL}")
                    print(f"{Fore.RED}energy_count:{Fore.GREEN} {race_energy_count}{Style.RESET_ALL}")

                    # 에너지 붙임
                    if player_who_use_card == "Opponent":
                        self.__opponent_field_unit_repository.attach_race_energy(int(unit_index), EnergyType.Undead,
                                                                                 race_energy_count)
                    elif player_who_use_card == "You":
                        self.__your_field_unit_repository.attach_race_energy(int(unit_index), EnergyType.Undead,
                                                                             race_energy_count)

                    # 필드 유닛 에너지 정보 갱신
                    for field_unit_index, field_unit_energy_info in field_unit_energy_map.items():
                        field_unit_index = int(field_unit_index)
                        print(f"{Fore.RED}field_unit_index:{Fore.GREEN} {field_unit_index}{Style.RESET_ALL}")
                        print(
                            f"{Fore.RED}field_unit_energy_info:{Fore.GREEN} {field_unit_energy_info}{Style.RESET_ALL}")

                        if player_who_use_card == "Opponent":
                            def calculate_notify_overflow_of_energy(param):
                                field_unit_index = param[0]
                                race_energy_number = param[1]
                                field_unit_energy_info = param[2]
                                current_opponent_field_unit_race_energy_count = (
                                    self.__opponent_field_unit_repository.get_opponent_field_unit_race_energy(
                                        field_unit_index, race_energy_number))
                                print(f"{Fore.RED}current_opponent_field_unit_race_energy_count:{Fore.GREEN}"
                                      f" {current_opponent_field_unit_race_energy_count}{Style.RESET_ALL}")

                                opponent_field_unit = (
                                    self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
                                        field_unit_index))
                                print(f"opponent_field_unit:{opponent_field_unit}")

                                opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                                opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                                total_energy_count = field_unit_energy_info['total_energy_count']
                                print(
                                    f"{Fore.RED}total_energy_count:{Fore.GREEN} {total_energy_count}{Style.RESET_ALL}")

                                for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                                    if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                                        if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                                            opponent_fixed_card_attached_shape.set_image_data(
                                                self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                                                    total_energy_count))

                            effect_animation = EffectAnimation()
                            effect_animation.set_animation_name('overflow_of_energy')
                            effect_animation.change_local_translation(
                                self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
                                    field_unit_index).get_fixed_card_base().get_local_translation())
                            effect_animation.draw_animation_panel()

                            self.__notify_reader_repository.save_notify_effect_animation_request(
                                EffectAnimationRequest(
                                    effect_animation=effect_animation,
                                    target_player=player_who_use_card,
                                    target_index=field_unit_index,
                                    target_type=TargetType.UNIT,
                                    call_function=calculate_notify_overflow_of_energy,
                                    function_need_param=True,
                                    param=(field_unit_index, race_energy_number, field_unit_energy_info)
                                )
                            )

                        elif player_who_use_card == "You":
                            def calculate_notify_overflow_of_energy(param):
                                field_unit_index = param[0]
                                race_energy_number = param[1]
                                field_unit_energy_info = param[2]
                                current_your_field_unit_race_energy_count = (
                                    self.__your_field_unit_repository.get_your_field_unit_race_energy(
                                        int(field_unit_index), int(race_energy_number)))
                                print(f"{Fore.RED}current_your_field_unit_race_energy_count:{Fore.GREEN}"
                                      f" {current_your_field_unit_race_energy_count}{Style.RESET_ALL}")

                                your_field_unit = (
                                    self.__your_field_unit_repository.find_field_unit_by_index(int(field_unit_index)))

                                your_fixed_card_base = your_field_unit.get_fixed_card_base()
                                your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                                total_energy_count = field_unit_energy_info['total_energy_count']
                                print(
                                    f"{Fore.RED}total_energy_count:{Fore.GREEN} {total_energy_count}{Style.RESET_ALL}")

                                for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                                    if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                                        if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                                            your_fixed_card_attached_shape.set_image_data(
                                                self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                                                    total_energy_count))

                            effect_animation = EffectAnimation()
                            effect_animation.set_animation_name('overflow_of_energy')
                            effect_animation.change_local_translation(
                                self.__your_field_unit_repository.find_field_unit_by_index(
                                    field_unit_index).get_fixed_card_base().get_local_translation())
                            effect_animation.draw_animation_panel()

                            self.__notify_reader_repository.save_notify_effect_animation_request(
                                EffectAnimationRequest(
                                    effect_animation=effect_animation,
                                    target_player=player_who_use_card,
                                    target_index=field_unit_index,
                                    target_type=TargetType.UNIT,
                                    call_function=calculate_notify_overflow_of_energy,
                                    function_need_param=True,
                                    param=(field_unit_index, race_energy_number, field_unit_energy_info)
                                )
                            )

    def notify_turn_start_targeting_attack_passive_skill_to_unit(self, notice_dictionary):

        data = notice_dictionary['NOTIFY_TURN_START_TARGETING_ATTACK_PASSIVE_SKILL_TO_UNIT']
        self.__attack_animation_object.set_notify_data(data)

        opponent_unit_index = list(data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'].keys())[0]
        opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
            int(opponent_unit_index))
        self.__attack_animation_object.set_opponent_animation_actor(opponent_field_unit)

        your_field_unit_index = \
        data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'][opponent_unit_index][
            'target_unit_index']
        your_field_unit = self.__your_field_unit_repository.find_field_unit_by_index(your_field_unit_index)
        self.__attack_animation_object.set_your_field_unit(your_field_unit)

        self.__attack_animation_object.set_is_opponent_attack_main_character(False)

        self.__opponent_field_area_inside_handler.set_active_field_area_action(
            OpponentFieldAreaActionProcess.PLAY_ANIMATION)

        self.__opponent_field_area_inside_handler.set_field_area_action(
            OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_PASSIVE_SKILL_PROCESS)

        self.__opponent_field_area_inside_handler.set_unit_action(
            OpponentUnitAction.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL)

    def notify_deploy_targeting_attack_passive_skill_to_unit(self, notice_dictionary):

        data = notice_dictionary['NOTIFY_DEPLOY_TARGETING_ATTACK_PASSIVE_SKILL_TO_UNIT']
        self.__attack_animation_object.set_notify_data(data)

        opponent_unit_index = list(data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'].keys())[0]
        opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
            int(opponent_unit_index))
        self.__attack_animation_object.set_opponent_animation_actor(opponent_field_unit)

        your_field_unit_index = \
        data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'][opponent_unit_index][
            'target_unit_index']
        your_field_unit = self.__your_field_unit_repository.find_field_unit_by_index(your_field_unit_index)
        self.__attack_animation_object.set_your_field_unit(your_field_unit)

        self.__attack_animation_object.set_is_opponent_attack_main_character(False)

        self.__opponent_field_area_inside_handler.set_active_field_area_action(
            OpponentFieldAreaActionProcess.PLAY_ANIMATION)

        self.__opponent_field_area_inside_handler.set_field_area_action(
            OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_PASSIVE_SKILL_PROCESS)

        self.__opponent_field_area_inside_handler.set_unit_action(
            OpponentUnitAction.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL)

    def notify_turn_start_non_targeting_attack_passive_skill(self, notice_dictionary):

        data = notice_dictionary['NOTIFY_TURN_START_NON_TARGETING_ATTACK_PASSIVE_SKILL']
        self.__attack_animation_object.set_notify_data(data)

        opponent_unit_index = int(
            list(data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'].keys())[0])
        opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
            opponent_unit_index)
        self.__attack_animation_object.set_opponent_animation_actor(opponent_field_unit)

        self.__opponent_field_area_inside_handler.set_active_field_area_action(
            OpponentFieldAreaActionProcess.PLAY_ANIMATION)

        self.__opponent_field_area_inside_handler.set_field_area_action(
            OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_PASSIVE_SKILL_PROCESS)

        self.__opponent_field_area_inside_handler.set_unit_action(
            OpponentUnitAction.NETHER_BLADE_FIRST_WIDE_AREA_PASSIVE_SKILL)

    def notify_deploy_non_targeting_attack_passive_skill(self, notice_dictionary):

        data = notice_dictionary['NOTIFY_DEPLOY_NON_TARGETING_ATTACK_PASSIVE_SKILL']
        print(f"{Fore.RED}notify_deploy_non_targeting_attack_passive_skill:{Fore.GREEN} {data}{Style.RESET_ALL}")

        self.__attack_animation_object.set_notify_data(data)

        opponent_unit_index = int(
            list(data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'].keys())[0])
        opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
            opponent_unit_index)
        self.__attack_animation_object.set_opponent_animation_actor(opponent_field_unit)

        self.__opponent_field_area_inside_handler.set_active_field_area_action(
            OpponentFieldAreaActionProcess.PLAY_ANIMATION)

        self.__opponent_field_area_inside_handler.set_field_area_action(
            OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_PASSIVE_SKILL_PROCESS)

        self.__opponent_field_area_inside_handler.set_unit_action(
            OpponentUnitAction.NETHER_BLADE_FIRST_WIDE_AREA_PASSIVE_SKILL)

    def notify_turn_start_targeting_attack_to_game_main_character(self, notice_dictionary):

        data = notice_dictionary['NOTIFY_TURN_START_TARGETING_ATTACK_TO_GAME_MAIN_CHARACTER']
        self.__attack_animation_object.set_notify_data(data)

        opponent_unit_index = list(data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'].keys())[0]
        opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
            int(opponent_unit_index))
        self.__attack_animation_object.set_opponent_animation_actor(opponent_field_unit)

        your_field_unit_index = \
        data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'][opponent_unit_index][
            'target_unit_index']
        your_field_unit = self.__your_field_unit_repository.find_field_unit_by_index(your_field_unit_index)
        self.__attack_animation_object.set_your_field_unit(your_field_unit)

        self.__attack_animation_object.set_is_opponent_attack_main_character(True)

        self.__opponent_field_area_inside_handler.set_active_field_area_action(
            OpponentFieldAreaActionProcess.PLAY_ANIMATION)

        self.__opponent_field_area_inside_handler.set_field_area_action(
            OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_PASSIVE_SKILL_PROCESS)

        self.__opponent_field_area_inside_handler.set_unit_action(
            OpponentUnitAction.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL)

    def notify_deploy_targeting_attack_to_game_main_character(self, notice_dictionary):

        data = notice_dictionary['NOTIFY_DEPLOY_TARGETING_ATTACK_TO_GAME_MAIN_CHARACTER']
        print(f"{Fore.RED}notify_deploy_non_targeting_attack_passive_skill:{Fore.GREEN} {data}{Style.RESET_ALL}")

        self.__attack_animation_object.set_notify_data(data)

        survival_info = data['player_main_character_survival_map']['You']

        opponent_unit_index = int(
            list(data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'].keys())[0])
        opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
            opponent_unit_index)
        self.__attack_animation_object.set_opponent_animation_actor(opponent_field_unit)

        self.__attack_animation_object.set_is_opponent_attack_main_character(True)

        self.__opponent_field_area_inside_handler.set_active_field_area_action(
            OpponentFieldAreaActionProcess.PLAY_ANIMATION)

        self.__opponent_field_area_inside_handler.set_field_area_action(
            OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_PASSIVE_SKILL_PROCESS)

        self.__opponent_field_area_inside_handler.set_unit_action(
            OpponentUnitAction.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL)

    def notify_use_instant_unit_death_item_card(self, notice_dictionary):

        # 1006 = {"NOTIFY_USE_INSTANT_UNIT_DEATH_ITEM_CARD":
        #     {"player_hand_use_map":
        #          {"Opponent": {"card_id": 8, "card_kind": 2}},
        #     "player_field_unit_health_point_map":
        #         {"You": {"field_unit_health_point_map": {"0": 0}}},
        #     "player_field_unit_death_map":
        #          {"You": {"dead_field_unit_index_list": [0]}}}}

        # 수신된 정보를 대입
        data = notice_dictionary['NOTIFY_USE_INSTANT_UNIT_DEATH_ITEM_CARD']
        self.__attack_animation_object.set_notify_data(data)
        # 유저 관련 키값 대입
        self.__attack_animation_object.set_animation_action(AnimationAction.DEATH_SCYTHE)

    def notify_use_field_energy_remove_item_card(self, notice_dictionary):

        # 수신된 정보를 대입
        data = notice_dictionary['NOTIFY_USE_FIELD_ENERGY_REMOVE_ITEM_CARD']

        # 유저 관련 키값 변수 선언
        player_who_use_card = None
        player_who_targeted = None

        # 카드 번호 추출
        for player_who_use_card_index in data['player_hand_use_map'].keys():
            player_who_use_card = player_who_use_card_index
            used_card_id = data['player_hand_use_map'][player_who_use_card]['card_id']

            # 카드를 사용 하고, 묘지로 보냄
            if player_who_use_card == "Opponent":
                self.__opponent_tomb_repository.create_opponent_tomb_card(used_card_id)
            elif player_who_use_card == "You":
                self.__your_tomb_repository.create_tomb_card(used_card_id)

            self.__battle_field_repository.set_current_use_card_id(used_card_id)

        for player_who_targeted_index in data['player_field_energy_map'].keys():
            player_who_targeted = player_who_targeted_index

            # 필드 에너지 제거
            if player_who_targeted == "Opponent":
                def remove_field_energy(data):
                    result_opponent_energy_count = data["player_field_energy_map"]['Opponent']

                    self.__opponent_field_energy_repository.set_opponent_field_energy(result_opponent_energy_count)

                effect_animation = EffectAnimation()
                effect_animation.set_animation_name('field_of_death')

                self.__notify_reader_repository.save_notify_effect_animation_request(
                    EffectAnimationRequest(
                        effect_animation=effect_animation,
                        target_player='Opponent',
                        target_index=99999,
                        target_type=TargetType.AREA,
                        call_function=remove_field_energy,
                        function_need_param=True,
                        param=data,
                        need_dalay=True
                    )
                )


            elif player_who_targeted == "You":
                def remove_field_energy(data):
                    result_your_energy_count = data["player_field_energy_map"]['You']
                    # remove_field_energy_point = data["player_field_energy_map"][player_who_targeted]
                    # your_energy_count = self.__your_field_energy_repository.get_your_field_energy() - remove_field_energy_point
                    # if your_energy_count <= 0:
                    #     result_your_energy_count = 0
                    # else:
                    #     result_your_energy_count = your_energy_count

                    self.__your_field_energy_repository.set_your_field_energy(result_your_energy_count)

                effect_animation = EffectAnimation()
                effect_animation.set_animation_name('field_of_death')

                self.__notify_reader_repository.save_notify_effect_animation_request(
                    EffectAnimationRequest(
                        effect_animation=effect_animation,
                        target_player='You',
                        target_index=99999,
                        target_type=TargetType.AREA,
                        call_function=remove_field_energy,
                        function_need_param=True,
                        param=data
                    )
                )

    def notify_surrender(self, notice_dictionary):

        data = notice_dictionary['NOTIFY_SURRENDER']
        print(f"{Fore.RED}notify_surrender:{Fore.GREEN} {data}{Style.RESET_ALL}")

        self.__battle_field_repository.win()

    def notify_use_unit_energy_remove_item_card(self, notice_dictionary):

        notify_dict_data = notice_dictionary['NOTIFY_USE_UNIT_ENERGY_REMOVE_ITEM_CARD']

        self.__attack_animation_object.set_notify_data(notify_dict_data)
        # 유저 관련 키값 대입
        self.__attack_animation_object.set_animation_action(AnimationAction.ENERGY_BURN)

    def notify_use_field_energy_increase_item_card(self, notice_dictionary):

        notify_dict_data = notice_dictionary['NOTIFY_USE_FIELD_ENERGY_INCREASE_ITEM_CARD']

        hand_use_card_id = int(notify_dict_data.get("player_hand_use_map", {})
                               .get("Opponent", {})
                               .get("card_id", None))

        field_energy = notify_dict_data.get('player_field_energy_map', {}).get('Opponent', None)

        unit_index = (notify_dict_data.get("player_field_unit_death_map", {})
                      .get("Opponent", {})
                      .get("dead_field_unit_index_list", []))[0]

        def change_field_energy():
            self.__opponent_field_energy_repository.set_opponent_field_energy(field_energy)
            self.apply_notify_data_of_dead_unit(notify_dict_data['player_field_unit_death_map'])

        self.__battle_field_repository.set_current_use_card_id(hand_use_card_id)
        # todo : 애니메이션 제작해서 넘겨야합
        effect_animation = EffectAnimation()
        effect_animation.set_animation_name('morale_conversion')
        effect_animation.change_local_translation(
            self.__opponent_field_unit_repository.find_field_unit_by_index(
                unit_index).get_fixed_card_base().get_local_translation())
        effect_animation.draw_animation_panel()

        self.__notify_reader_repository.save_notify_effect_animation_request(
            EffectAnimationRequest(
                effect_animation=effect_animation,
                target_player='Opponent',
                target_index=unit_index,
                target_type=TargetType.UNIT,
                call_function=change_field_energy
            )
        )


