import tkinter


from my_card_main_frame.repository.my_card_main_frame_repository_impl import MyCardMainFrameRepositoryImpl
from my_card_main_frame.service.my_card_main_frame_service import MyCardMainFrameService
from my_deck_frame_legacy.service.my_deck_frame_service_impl import MyDeckFrameRepositoryImpl, MyDeckFrameServiceImpl


class MyCardMainFrameServiceImpl(MyCardMainFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__myCardMainFrameRepository = MyCardMainFrameRepositoryImpl.getInstance()
            cls.__instance.__myDeckFrameRepository = MyDeckFrameRepositoryImpl.getInstance()
            cls.__instance.__myDeckFrameService = MyDeckFrameServiceImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def createMyCardMainUiFrame(self, rootWindow, switchFrameWithMenuName):
        myCardMainFrame = self.__myCardMainFrameRepository.createMyCardMainFrame(rootWindow)

        deck_generation_button = tkinter.Button(myCardMainFrame, text="덱 생성", bg="#2E7D32", fg="white",
                                                command=lambda:[myCardMainFrame.alphaBackground(), myCardMainFrame.makeMyDeckFrame()], width=24, height=2)
        deck_generation_button.place(relx=0.85, rely=0.8, anchor="center")

        go_back_to_lobby_button = tkinter.Button(myCardMainFrame, text="로비로 돌아가기", bg="#C62828", fg="white",
                                                 command=lambda: switchFrameWithMenuName("lobby-menu"), width=24,
                                                 height=2)
        go_back_to_lobby_button.place(relx=0.85, rely=0.9, anchor="center")

        deck_generation_button = tkinter.Button(myCardMainFrame, text="이전 페이지", bg="#2E7D32", fg="white",
                                                command=lambda: switchFrameWithMenuName("lobby-menu"), width=24,
                                                height=2)
        deck_generation_button.place(relx=0.2, rely=0.9, anchor="e")

        go_back_to_lobby_button = tkinter.Button(myCardMainFrame, text="다음 페이지", bg="#C62828", fg="white",
                                                 command=lambda: switchFrameWithMenuName("lobby-menu"), width=24,
                                                 height=2)
        go_back_to_lobby_button.place(relx=0.5, rely=0.9, anchor="w")

        return myCardMainFrame
