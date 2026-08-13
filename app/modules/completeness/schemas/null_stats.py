from enum import Enum

from pydantic import BaseModel, ConfigDict


class NullPhanLoai(str, Enum):
    REVIEW = "review"
    OK = "ok"


class ColumnNullInfo(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    ten_bang: str
    ten_cot: str
    so_luong_null: float | None
    ty_le_null: float | None
    phan_loai: NullPhanLoai
    ghi_chu: str
