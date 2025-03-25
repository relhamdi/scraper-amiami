from datetime import datetime


def get_current_date(format: str = "%Y%m%d_%H%M%S") -> str:
    """
    Format the current datetime to a given format.

    Args:
        format (str, optional): Data format. Defaults to "%Y%m%d_%H%M%S".

    Returns:
        str: Date formatted.
    """
    return datetime.now().strftime(format)
