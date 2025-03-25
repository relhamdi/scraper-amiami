from io import TextIOWrapper
from json import dump as json_dump

from models.base import CustomBaseModel


def save_model_to_json(file: TextIOWrapper, model: CustomBaseModel):
    """
    Save a Pydantic model as JSON into a given file.

    Args:
        file (TextIOWrapper): File.
        model (CustomBaseModel): Model to write.
    """
    json_dump(
        model.model_dump(mode="json"),
        file,
        indent=4,
        ensure_ascii=False,
    )
