from animation_action_checker.check_action import CheckAction


class CurrentStatusRepository:
    __instance = None

    check_action = CheckAction.DUMMY

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def set_check_action(self, check_action):
        self.__check_action = check_action

    def get_check_action(self):
        return self.__check_action
