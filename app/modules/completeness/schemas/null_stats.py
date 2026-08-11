from enum import Enum

from pydantic import BaseModel, ConfigDict


class NullableStatus(str, Enum):
    NOT_NULLABLE = "not_nullable"
    NULLABLE = "nullable"


class NullPhanLoai(str, Enum):
    DANGER = "danger"
    REVIEW = "review"
    OK = "ok"
    NOT_PROFILED = "not_profiled"


class ColumnNullInfo(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    ten_bang: str
    ten_cot: str
    nullable: NullableStatus
    so_luong_null: float | None
    tong_so_dong: float | None
    ty_le_null: float | None
    phan_loai: NullPhanLoai
