import enum
from enum import Enum


class NoticeType(Enum):
    NOTIFY_HAND_CARD_USE = 0
    NOTIFY_DRAW_COUNT = 1
    NOTIFY_DRAWN_CARD_LIST = 2
    NOTIFY_DECK_CARD_LIST_USE = 3
    NOTIFY_FIELD_UNIT_ENERGY = 4
    NOTIFY_SEARCH_COUNT = 5
    NOTIFY_SEARCH_CARD_LIST = 6
