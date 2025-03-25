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

    AGE_RESTRICTED = "8551"


class ItemCategory2Enum(str, Enum):
    """
    Possible category 2 values for queries.
    """

    FOREIGN = "1081"
    CHARACTER = "1298"
    BISHOUJO = "459"
