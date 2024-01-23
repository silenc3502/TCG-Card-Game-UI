import tkinter

from my_card_main_frame.entity.my_card_main_frame import MyCardMainFrame
from my_card_main_frame.repository.my_card_main_frame_repository import MyCardMainFrameRepository


class MyCardMainFrameRepositoryImpl(MyCardMainFrameRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createMyCardMainFrame(self, rootWindow):
        print("MyCardFrameRepositoryImpl: createMyCardFrame()")
        myCardMainFrame = MyCardMainFrame(rootWindow, width=1200, height=800)

        return myCardMainFrame