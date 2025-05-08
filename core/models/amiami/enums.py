from enum import Enum


class ItemSortingEnum(str, Enum):
    """
    Possible sorting values for queries.
    """

    RECENT_UPDATE = "regtimed"
    RECOMMENDATION = "recommend"
    RELEASE_DATE = "releasedated"
    PREOWNED = "preowned"


class ItemTypeEnum(str, Enum):
    """
    Possible item type values for queries.
    """

    PRE_ORDER = "s_st_list_preorder_available"
    BACK_ORDER = "s_st_list_backorder_available"
    NEW = "s_st_list_newitem_available"
    PRE_OWNED = "s_st_condition_flg"
    # WITH_BONUS = "s_st_list_store_bonus"
    # ON_SALE = "s_st_saleitem"


class ItemCategory1Enum(str, Enum):
    """
    Possible item category 1 values for queries.
    """

    TRADING_FIGURES = "219"
    CHARACTER_GOODS = "194"
    FASHION = "9882"
    CARD_GAMES = "1"
    TRADING_CARDS = "120"
    HOUSEHOLD_GOODS = "680"
    AGE_RESTRICTED = "8551"

# todo rename ensuite (figures suffix) et agerestricted_products

class ItemCategory2Enum(str, Enum):
    """
    Possible category 2 values for queries.
    """

    BISHOUJO = "459"
    CHARACTER = "1298"
    FOREIGN = "1081"
    DOLLS = "460"
    SCALE_MILITARY = "944"
    CAR_MODELS = "949"
    TRAIN_MODELS = "9604"
    TOOLS_PAINTS_MATERIAL = "9565"
    CAR_PLASTIC_MODEL_KITS = "946"
    BOOKS_MANGAS = "161"
    VIDEO_GAMES = "162"
    BLURAY_DISCS = "9996"
    DVDS = "1372"
    CDS = "156"
    CARD_SUPPLIES = "215"
    KIDS_TOYS = "1299"
    STATIONERY = "10119"
    JIGSAW_PUZZLES = "200"
    CALENDARS = "10042"

class ItemCategory3Enum(str, Enum):
    GUNDAM_TOYS = "918"
    ROBOTS = "986"
    TOKUSATSU_TOYS = "952"
    PLUSH_DOLLS = "10118"