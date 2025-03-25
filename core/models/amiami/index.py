from typing import List

from config import AMIAMI_IMG_ROOT
from models.amiami.v1.item import (
    AmiAmiItemDetailModel,
    AmiAmiItemModelFinal,
    AmiAmiItemResponseModel,
)
from models.amiami.v1.items import (
    AmiAmiItemModel,
    AmiAmiItemsResponseModel,
)
from pydantic import Field


class AmiAmiItemOutput(AmiAmiItemModelFinal):
    """
    Alias for the final data model used to output enriched data.
    """

    ...


# Items (list) endpoint


class AmiAmiItem(AmiAmiItemModel):
    """
    Alias for the basic item representation returned in the /items endpoint.
    """

    def minify(self) -> AmiAmiItemOutput:
        """
        Map the item to the final data model (mostly by removing fields).

        Returns:
            AmiAmiItemOutput: Mapped item.
        """
        return AmiAmiItemOutput(
            gcode=self.gcode,
            name=self.gname,
            gcode_url=f"https://www.amiami.com/eng/detail/?gcode={self.gcode}",
            scode_url="https://www.amiami.com/eng/detail/?scode=",
            image_url=AMIAMI_IMG_ROOT + self.thumb_url,
            full_price=self.c_price_taxed,
            price=self.max_price,
            release_date=self.releasedate,
            jancode=self.jancode,
            is_preowned=self.is_preowned,
            is_preorder=self.is_preorder,
            is_backorder=self.list_backorder_available,
            has_store_bonus=self.list_store_bonus,
            is_amiami_limited=self.list_amiami_limited,
            is_age_limited=self.gcode.startswith("LTD"),
            has_preorder_bonus=self.list_store_bonus,
            is_on_sale=self.is_on_sale,
            is_preowned_sale=self.is_preowned_sale,
        )


class AmiAmiItemsResponse(AmiAmiItemsResponseModel):
    """
    Alias for the data model returned by the /items endpoint.
    """

    # Overriding type of the variable
    items: List[AmiAmiItem] = Field(default_factory=list)


# Item (detail) endpoint


class AmiAmiItemInput(AmiAmiItemDetailModel):
    """
    Alias for the detailed item representation returned in the /item endpoint.
    """

    def minify(self) -> AmiAmiItemOutput:
        """
        Map the item to the final data model (mostly by removing fields).

        Returns:
            AmiAmiItemOutput: Mapped item.
        """
        return AmiAmiItemOutput(
            gcode=self.gcode,
            scode=self.scode,
            name=self.gname,
            gcode_url=f"https://www.amiami.com/eng/detail/?gcode={self.gcode}",
            scode_url=f"https://www.amiami.com/eng/detail/?scode={self.scode}",
            image_url=AMIAMI_IMG_ROOT + self.main_image_url,
            full_price=self.c_price_taxed,
            price=self.price,
            reward_point=self.point,
            sale_status=self.salestatus,
            jancode=self.jancode,
            maker_name=self.maker_name,
            modeler_name=self.modeler,
            description=self.spec,
            memo=self.memo,
            copyright=self.copyright,
            is_preowned=self.is_preowned,
            is_preorder=self.is_preorder,
            is_backorder=self.is_backorder,
            has_store_bonus=self.has_store_bonus,
            is_amiami_limited=self.is_amiami_limited,
            is_age_limited=self.is_age_limited,
            has_preorder_bonus=self.has_preorder_bonus,
            is_on_sale=self.is_on_sale,
            is_preowned_sale=self.is_preowned_sale,
            categories=self.categories,
        )


class AmiAmiItemResponse(AmiAmiItemResponseModel):
    """
    Alias for the data model returned by the /item endpoint.
    """

    # Overriding type of the variable
    item: AmiAmiItemInput
