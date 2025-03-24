from collections.abc import Iterable
from typing import Any


## External Function ##
def convert_enum_to_list(enum: Any) -> list[str]:
    if isinstance(enum, Iterable):
        return [item.value for item in enum]
    return []
