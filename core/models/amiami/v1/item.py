from datetime import datetime
from typing import List, Optional

from models.base import CustomBaseForbid
from pydantic import Field, field_validator


class AmiAmiReviewImageModel(CustomBaseForbid):
    image_url: str
    thumb_url: str
    alt: str
    title: str


class AmiAmiRelatedItemModel(CustomBaseForbid):
    gcode: str
    gname: str
    thumb_url: str
    thumb_alt: str
    thumb_title: str
    thumb_agelimit: bool

    @field_validator("thumb_agelimit", mode="before")
    def convert_int_to_bool(cls, v):
        return bool(v)


class AmiAmiOtherItemModel(CustomBaseForbid):
    scode: str
    icon_type: Optional[int]
    price: Optional[int]
    condition: str


class AmiAmiNamedFieldModel(CustomBaseForbid):
    id: int
    name: str


class AmiAmiEmbeddedDataModel(CustomBaseForbid):
    review_images: List[AmiAmiReviewImageModel] = Field(default_factory=list)
    bonus_images: list = Field(default_factory=list)
    related_items: List[AmiAmiRelatedItemModel] = Field(default_factory=list)
    other_items: List[AmiAmiOtherItemModel] = Field(default_factory=list)
    makers: List[AmiAmiNamedFieldModel] = Field(default_factory=list)
    series_titles: List[AmiAmiNamedFieldModel] = Field(default_factory=list)
    original_titles: List[AmiAmiNamedFieldModel] = Field(default_factory=list)
    character_names: List[AmiAmiNamedFieldModel] = Field(default_factory=list)

    @field_validator(
        "review_images",
        "bonus_images",
        "related_items",
        "other_items",
        "makers",
        "series_titles",
        "original_titles",
        "character_names",
        mode="before",
    )
    def check_cate7(cls, v):
        if v is None:
            return []
        return v


class AmiAmiItemModelFinal(CustomBaseForbid):
    gcode: str
    scode: str = ""
    name: str
    gcode_url: str
    scode_url: str
    image_url: str
    full_price: int
    price: Optional[int]
    reward_point: int = 0
    sale_status: str = ""
    release_date: Optional[datetime] = None
    jancode: Optional[str]
    maker_name: str = ""
    modeler_name: str = ""
    description: str = ""
    memo: str = ""
    copyright: str = ""

    item_condition: str = ""
    box_condition: str = ""

    is_preowned: bool
    is_preorder: bool
    is_backorder: bool
    has_store_bonus: bool
    is_amiami_limited: bool
    is_age_limited: bool
    has_preorder_bonus: bool
    is_on_sale: bool
    is_preowned_sale: bool

    categories: List[int] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class AmiAmiItemDetailModel(CustomBaseForbid):
    gcode: str
    scode: str
    gname: str
    sname: str
    main_image_url: str
    list_price: int
    c_price_taxed: int
    price: Optional[int]
    point: int = 0
    salestatus: str
    releasedate: str
    is_watch_list_available: bool = Field(alias="watch_list_available")
    jancode: Optional[str]
    maker_name: str
    modeler: str
    spec: str
    memo: str
    copyright: str
    is_preowned: bool = Field(alias="condition_flg")
    is_preorder: bool = Field(alias="preorderitem")
    is_backorder: bool = Field(alias="backorderitem")
    has_store_bonus: bool = Field(alias="store_bonus")
    is_amiami_limited: bool = Field(alias="amiami_limited")
    is_age_limited: bool = Field(alias="agelimit")
    categories: List[int] = Field(default_factory=list)
    has_preorder_bonus: bool = Field(alias="preorder_bonus_flg")
    is_on_sale: bool = Field(alias="onsale_flg")
    is_preowned_sale: bool = Field(alias="preowned_sale_flg")

    gname_sub: str
    sname_simple: str
    sname_simple_j: str
    main_image_alt: str
    main_image_title: str
    image_comment: str
    youtube: Optional[str]
    period_from: Optional[str]
    period_to: Optional[str]
    cart_type: int
    max_cartin_count: int
    include_instock_only_flg: bool
    remarks: str
    size_info: Optional[str]
    modelergroup: str
    saleitem: int
    instock_flg: bool
    order_closed_flg: bool
    preown_attention: bool
    producttypeattention: bool
    customs_warning_flg: bool
    preorderattention: str
    domesticitem: bool
    metadescription: str
    metawords: str
    releasechange_text: str
    cate1: Optional[List[int]] = Field(default_factory=list)
    cate2: Optional[List[int]] = Field(default_factory=list)
    cate3: Optional[List[int]] = Field(default_factory=list)
    cate4: Optional[List[int]] = Field(default_factory=list)
    cate5: Optional[List[int]] = Field(default_factory=list)
    cate6: Optional[List[int]] = Field(default_factory=list)
    cate7: Optional[List[int]] = Field(default_factory=list)
    salestalk: str
    buy_flg: bool
    buy_price: int
    buy_remarks: Optional[str]
    end_flg: bool
    disp_flg: bool
    handling_store: Optional[str]
    salestatus_detail: str
    stock: int
    newitem: int
    saletopitem: int
    resale_flg: bool
    big_title_flg: bool
    soldout_flg: bool
    inc_txt1: int
    inc_txt2: int
    inc_txt3: int
    inc_txt4: int
    inc_txt5: int
    inc_txt6: int
    inc_txt7: int
    inc_txt8: int
    inc_txt9: int
    inc_txt10: int
    image_on: bool
    image_category: Optional[str]
    image_name: Optional[str]
    metaalt: str
    image_reviewnumber: int
    image_reviewcategory: Optional[str]
    price1: int
    price2: int
    price3: int
    price4: int
    price5: int
    discountrate1: int
    discountrate2: int
    discountrate3: int
    discountrate4: int
    discountrate5: int
    sizew: str
    colorw: str
    thumb_url: str
    thumb_alt: Optional[str]
    thumb_title: Optional[str]
    thumb_agelimit: bool

    @field_validator(
        "is_watch_list_available",
        "is_preowned",
        "is_preorder",
        "is_backorder",
        "has_store_bonus",
        "is_amiami_limited",
        "is_age_limited",
        "has_preorder_bonus",
        "is_on_sale",
        "is_preowned_sale",
        "include_instock_only_flg",
        "instock_flg",
        "order_closed_flg",
        "preown_attention",
        "producttypeattention",
        "customs_warning_flg",
        "domesticitem",
        "buy_flg",
        "end_flg",
        "disp_flg",
        "resale_flg",
        "big_title_flg",
        "soldout_flg",
        "image_on",
        "thumb_agelimit",
        mode="before",
    )
    def convert_int_to_bool(cls, v):
        return bool(v)

    @field_validator("categories", mode="before")
    def merge_categories(cls, v, values):
        merged = []
        for key in ["cate1", "cate2", "cate3", "cate4", "cate5", "cate6", "cate7"]:
            if key in values and values[key]:
                merged.extend(values[key])
        return merged


class AmiAmiItemResponseModel(CustomBaseForbid):
    api_success: bool = Field(alias="RSuccess")
    api_value: Optional[str] = Field(alias="RValue")
    api_message: str = Field(alias="RMessage")
    item: AmiAmiItemDetailModel
    embedded_data: AmiAmiEmbeddedDataModel = Field(alias="_embedded")
