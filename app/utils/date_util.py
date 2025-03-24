from datetime import date, datetime

from app.common.enums import DateFormatEnum


## External Function ##
def format_date(value: date | None, fmt: DateFormatEnum = DateFormatEnum.DD_MM_YYYY) -> str | None:
    if not value:
        return None
    return value.strftime(fmt.value)

def format_datetime(value: datetime | None, fmt: DateFormatEnum = DateFormatEnum.HH_MM_SS_DD_MM_YYYY) -> str | None:
    if not value:
        return None
    return value.strftime(fmt.value)


def parse_date(date_str: str, fmt: DateFormatEnum = DateFormatEnum.DD_MM_YYYY) -> date | None:
    try:
        return datetime.strptime(date_str, fmt.value).date()
    except ValueError:
        return None

def parse_datetime(date_str: str, fmt: DateFormatEnum = DateFormatEnum.HH_MM_SS_DD_MM_YYYY) -> datetime | None:
    try:
        return datetime.strptime(date_str, fmt.value)
    except ValueError:
        return None
