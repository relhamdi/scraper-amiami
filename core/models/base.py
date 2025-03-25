from pydantic import BaseModel


class CustomConfig:
    use_enum_values = True
    arbitrary_types_allowed = True


class CustomBaseModel(BaseModel): ...


class CustomBaseForbid(CustomBaseModel):
    class Config(CustomConfig):
        extra = "forbid"


class CustomBaseAllow(CustomBaseForbid):
    class Config(CustomConfig):
        extra = "allow"
