from os import environ, getcwd, makedirs
from os.path import join
from typing import Literal

# Type aliases

# Possible code types
AmiAmiCodeTypeLiteral = Literal["gcode", "scode"]


# Directories

OUTPUT_DIR = join(getcwd(), "output")
makedirs(OUTPUT_DIR, exist_ok=True)

WEB_DIR = join(getcwd(), "web")
makedirs(WEB_DIR, exist_ok=True)

WEB_DATA_DIR = join(WEB_DIR, "data")
makedirs(WEB_DATA_DIR, exist_ok=True)


# Files

DATA_LIST_FILE = join(WEB_DATA_DIR, "_data_files.txt")


# Env variables

AMIAMI_USER_KEY = environ["AMIAMI_USER_KEY"]
AMIAMI_USER_AGENT = environ["AMIAMI_USER_AGENT"]

AMIAMI_API_ROOT = environ["AMIAMI_API_ROOT"]
AMIAMI_IMG_ROOT = environ["AMIAMI_IMG_ROOT"]

ITEMS_PER_PAGE = environ["ITEMS_PER_PAGE"]
