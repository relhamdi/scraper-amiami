from typing import List, Optional

from models.amiami.enums import (
    ItemCategory1Enum,
    ItemCategory2Enum,
    ItemSortingEnum,
    ItemTypeEnum,
)
from models.amiami.index import AmiAmiItem, AmiAmiItemOutput
from models.base import CustomBaseForbid
from pydantic import Field


class AmiAmiQueryArgs(CustomBaseForbid):
    """
    Summary of the supported query args for the /items endpoint.
    """

    num_pages: Optional[int] = None
    keyword: str = ""
    types: List[ItemTypeEnum] = Field(default_factory=list)
    category1: Optional[ItemCategory1Enum] = None
    category2: Optional[ItemCategory2Enum] = None
    sort_key: Optional[ItemSortingEnum] = None

    def stringify(self) -> str:
        """
        Generate a string from the arguments of the query.

        Returns:
            str: Stringified arguments
        """
        args_list = []
        for arg, val in self.model_dump(mode="json").items():
            if isinstance(val, list):
                args_list.append(f"{arg}={','.join(val)}")
            else:
                args_list.append(f"{arg}={val}")
        return "&".join(args_list)


class AmiAmiItemsDump(CustomBaseForbid):
    """
    Data model for the temporary data dump after the /items scraping.
    """

    items_length: int
    items: List[AmiAmiItem] = Field(default_factory=list)


class AmiAmiItemOutputDump(CustomBaseForbid):
    """
    Data model for the final data dump after enriching.
    """

    current_index: int = 0
    items_length: int
    items: List[AmiAmiItemOutput] = Field(default_factory=list)
