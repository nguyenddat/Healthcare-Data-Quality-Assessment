import re
from enum import Enum

from metadata.generated.schema.entity.data.table import DataType

DATE_NAME_PATTERNS = [
    r"(^|_)NGAY($|_)",       # NGAY, NGAY_TAO
    r"^NGAY",                # NGAYTAO, NGAYSINH
    r"NGAY$",                # CREATEDNGAY (nếu có)
    r"(^|_)DATE($|_)",       # CREATE_DATE
    r"_DATE$",               # BIRTH_DATE
    r"^DATE_",               # DATE_CREATED
    r"(^|_)DAY($|_)",        # START_DAY
    r"_DAY$",                # BIRTH_DAY
]

DATE_DATA_TYPES = {DataType.DATE, DataType.DATETIME, DataType.TIMESTAMP}

def is_date_column_name(column_name: str) -> bool:
    name = column_name.upper().strip()
    if any(re.search(pattern, name) for pattern in DATE_NAME_EXCLUDES):
        return False
    return any(re.search(pattern, name) for pattern in DATE_NAME_PATTERNS)

def is_date_datatype(column: any) -> bool:
    if column.dataType in DATE_DATA_TYPES:
        return True
    return False
