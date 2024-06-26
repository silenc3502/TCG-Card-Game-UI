import os
import time

import pygame.mixer

from music_player.repository.music_player_repository import MusicPlayerRepository


class MusicPlayerRepositoryImpl(MusicPlayerRepository):
    __instance = None
    __uiIpcChannel = None
    __backgroundMusicFilePathDict = {}
    __soundPathDict = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            # pygame.mixer.init()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def saveUiIpcChannel(self, uiIpcChannel):
        print('music channel saved')
        self.__uiIpcChannel = uiIpcChannel

    def load_background_music_path_with_frame_name(self, frame_name: str):
        print(f"MusicPlayerRepositoryImpl : load_background_music_path_with_frame_name - {frame_name}")
        current_location = os.getcwd()
        background_music_path = os.path.join(current_location, 'local_storage', 'background_music', f'{frame_name}.mp3')
        self.__backgroundMusicFilePathDict[frame_name] = background_music_path
        print(self.__backgroundMusicFilePathDict)

    def load_sound_effect_path_with_event_name(self, event_name: str):
        print(f"MusicPlayerRepositoryImpl : load_sound_effect_path_with_event_name - {event_name}")
        current_location = os.getcwd()
        sound_effect_file_path = os.path.join(current_location, 'local_storage', 'sound_effect', f'{event_name}.mp3')
        self.__soundPathDict[event_name] = sound_effect_file_path
        print(self.__soundPathDict)

    def play_background_music(self):
        while True:
            try:
                frame_name = self.__uiIpcChannel.get()
                if frame_name:
                    for frame in self.__backgroundMusicFilePathDict.keys():
                        if frame == frame_name:
                            path = self.__get_background_music_path(frame_name)
                            pygame.mixer.init()
                            self.play_music(path)
                            if pygame.mixer.music.get_busy():
                                print("Background music - " + frame_name)
            finally:
                time.sleep(0.1)

    def play_music(self, path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)

    def __get_background_music_path(self, frame_name: str):
        return self.__backgroundMusicFilePathDict[frame_name]

    def play_sound_effect_with_event_name(self, event_name: str):
        print("MusicPlayerRepositoryImpl : play_sound_effect_with_event_name - " + event_name)
        pygame.mixer.init()
        sound = pygame.mixer.Sound(self.__soundPathDict[event_name])
        sound.play()

        time.sleep(0.1)

    # def play_sound_effect_with_event_name_for_wav(self, event_name: str):
    #     print("MusicPlayerRepositoryImpl : play_sound_effect_with_event_name_for_wav - " + event_name)
    #     pygame.mixer.init()
    #     current_location = os.getcwd()
    #     sound_effect_file_path = os.path.join(current_location, 'local_storage', 'sound_effect', f'{event_name}.wav')
    #     sound = pygame.mixer.Sound(sound_effect_file_path)
    #     sound.play()
    #
    #     time.sleep(0.1)
    def play_sound_effect_of_mouse_on_click(self, mouse_on_click_event_name: str):
        # print("MusicPlayerRepositoryImpl : play_sound_effect_of_mouse_on_click - " + mouse_on_click_event_name)
        current_location = os.getcwd()
        sound_effect_file_path = (
            os.path.join(
                current_location,
                'local_storage', 'sound_effect', 'mouse_on_click', f'{mouse_on_click_event_name}.mp3'))
        if not os.path.exists(sound_effect_file_path):
            print('유효하지 않은 경로입니다.')
            return
        pygame.mixer.init()
        sound = pygame.mixer.Sound(sound_effect_file_path)
        sound.play()

    def play_sound_effect_of_battle_match(self, battle_match_event_name: str):
        print("MusicPlayerRepositoryImpl : play_sound_effect_of_battle_match - " + battle_match_event_name)
        current_location = os.getcwd()
        sound_effect_file_path = (
            os.path.join(
                current_location,
                'local_storage', 'sound_effect', 'battle_match', f'{battle_match_event_name}.mp3'))
        if not os.path.exists(sound_effect_file_path):
            print('유효하지 않은 경로입니다.')
            return
        pygame.mixer.init()
        sound = pygame.mixer.Sound(sound_effect_file_path)
        sound.play()

    def play_sound_effect_of_unit_deploy(self, deployed_unit_number: str):
        print("MusicPlayerRepositoryImpl : play_sound_effect_of_unit_deploy - " + deployed_unit_number)
        current_location = os.getcwd()
        sound_effect_file_path = (
            os.path.join(
                current_location,
                'local_storage', 'sound_effect', 'unit_deploy', f'{deployed_unit_number}.mp3'))
        if not os.path.exists(sound_effect_file_path):
            print('유효하지 않은 경로입니다.')
            return
        pygame.mixer.init()
        sound = pygame.mixer.Sound(sound_effect_file_path)
        sound.play()

    def play_sound_effect_of_unit_attack(self, unit_attack_event_name: str):
        print("MusicPlayerRepositoryImpl : play_sound_effect_of_unit_attack - " + unit_attack_event_name)
        current_location = os.getcwd()
        sound_effect_file_path = (
            os.path.join(
                current_location,
                'local_storage', 'sound_effect', 'unit_attack', f'{unit_attack_event_name}.mp3'))
        if not os.path.exists(sound_effect_file_path):
            print('유효하지 않은 경로입니다.')
            return
        pygame.mixer.init()
        sound = pygame.mixer.Sound(sound_effect_file_path)
        sound.play()

    def play_sound_effect_of_card_execution(self, card_execution_event_name: str):
        print("MusicPlayerRepositoryImpl : play_sound_effect_of_card_execution - " + card_execution_event_name)
        current_location = os.getcwd()
        sound_effect_file_path = (
            os.path.join(
                current_location,
                'local_storage', 'sound_effect', 'card_execution', f'{card_execution_event_name}.mp3'))
        if not os.path.exists(sound_effect_file_path):
            print('유효하지 않은 경로입니다.')
            return
        pygame.mixer.init()
        sound = pygame.mixer.Sound(sound_effect_file_path)
        sound.play()

    def play_sound_effect_of_card_execution_with_delay(self, card_execution_event_name: str, delay: int):
        print("MusicPlayerRepositoryImpl : play_sound_effect_of_card_execution_with_delay - " + card_execution_event_name)
        current_location = os.getcwd()
        sound_effect_file_path = (
            os.path.join(
                current_location,
                'local_storage', 'sound_effect', 'card_execution', f'{card_execution_event_name}.mp3'))
        if not os.path.exists(sound_effect_file_path):
            print('유효하지 않은 경로입니다.')
            return
        time.sleep(delay)
        pygame.mixer.init()
        sound = pygame.mixer.Sound(sound_effect_file_path)
        sound.play()

    def play_sound_effect_of_timer(self, timer_event_name: str, stop_event: int):
        print("MusicPlayerRepositoryImpl : play_sound_effect_of_timer - " + timer_event_name)
        pygame.mixer.init()
        if stop_event == -1:
            pygame.mixer.stop()
            return
        current_location = os.getcwd()
        sound_effect_file_path = (
            os.path.join(
                current_location,
                'local_storage', 'sound_effect', 'timer', f'{timer_event_name}.mp3'))
        if not os.path.exists(sound_effect_file_path):
            print('유효하지 않은 경로입니다.')
            return
        sound = pygame.mixer.Sound(sound_effect_file_path)
        sound.play()

    def play_sound_effect_of_game_end(self, game_end_event_name: str):
        print("MusicPlayerRepositoryImpl : play_sound_effect_of_game_end - " + game_end_event_name)
        pygame.mixer.init()
        current_location = os.getcwd()
        sound_effect_file_path = (
            os.path.join(
                current_location,
                'local_storage', 'sound_effect', 'game_end', f'{game_end_event_name}.mp3'))
        if not os.path.exists(sound_effect_file_path):
            print('유효하지 않은 경로입니다.')
            return
        sound = pygame.mixer.Sound(sound_effect_file_path)
        sound.play()
