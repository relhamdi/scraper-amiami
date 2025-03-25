from datetime import datetime
from typing import List, Optional

from models.base import CustomBaseAllow, CustomBaseForbid
from pydantic import ConfigDict, Field, field_validator


class CategoryTagModel(CustomBaseForbid):
    id: int
    name: str
    count: int


class SearchResultModel(CustomBaseForbid):
    total_results: int


class AmiAmiItemModel(CustomBaseForbid):
    model_config = ConfigDict(populate_by_name=True)

    gcode: str
    gname: str
    thumb_url: str
    min_price: int
    max_price: int
    maker_name: Optional[str]
    is_on_sale: bool = Field(alias="saleitem")
    is_preowned: bool = Field(alias="condition_flg")
    is_in_stock: bool = Field(alias="instock_flg")
    is_order_closed: bool = Field(alias="order_closed_flg")
    releasedate: Optional[datetime]
    jancode: Optional[str]
    is_preorder: bool = Field(alias="preorderitem")
    saletopitem: bool
    is_resale: bool = Field(alias="resale_flg")
    is_preowned_sale: bool = Field(alias="preowned_sale_flg")
    cat_for_women: bool = Field(alias="for_women_flg")
    cat_moe: bool = Field(alias="genre_moe")
    cate6: Optional[int]
    cate7: Optional[int]
    buy_price: Optional[int]

    thumb_alt: Optional[str]
    thumb_title: Optional[str]
    c_price_taxed: int
    list_preorder_available: bool
    list_backorder_available: bool
    list_store_bonus: bool
    list_amiami_limited: bool
    element_id: Optional[str]
    salestatus: Optional[str]
    salestatus_detail: Optional[str]
    buy_flg: bool
    buy_remarks: Optional[str]
    stock_flg: bool
    image_on: bool
    image_category: Optional[str]
    image_name: Optional[str]
    metaalt: Optional[str]

    @field_validator(
        "is_on_sale",
        "is_preowned",
        "list_preorder_available",
        "list_backorder_available",
        "list_store_bonus",
        "list_amiami_limited",
        "is_in_stock",
        "is_order_closed",
        "is_preorder",
        "saletopitem",
        "is_resale",
        "is_preowned_sale",
        "cat_for_women",
        "cat_moe",
        "buy_flg",
        "stock_flg",
        "image_on",
        mode="before",
    )
    def convert_int_to_bool(cls, v):
        return bool(v)

    @field_validator("releasedate", mode="before")
    @classmethod
    def convert_date(cls, v):
        if v:
            return datetime.fromisoformat(v)
        return None


class AmiAmiEmbeddedModel(CustomBaseAllow):
    category_tags: List[CategoryTagModel] = Field(default_factory=list)


class AmiAmiItemsResponseModel(CustomBaseForbid):
    api_success: bool = Field(alias="RSuccess")
    api_value: Optional[str] = Field(alias="RValue")
    api_message: str = Field(alias="RMessage")
    search_result: SearchResultModel
    items: List[AmiAmiItemModel] = Field(default_factory=list)
    embedded_data: AmiAmiEmbeddedModel = Field(alias="_embedded")
