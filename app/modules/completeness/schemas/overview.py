from enum import Enum

from pydantic import BaseModel, ConfigDict


class DuLieu(str, Enum):
    NO_DATA = "no_data"
    SPARSE_DATA = "sparse_data"
    FULL_DATA = "full_data"


class TableOverviewInfo(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    ten_bang: str
    so_dong: int
    ngay_tao: str | None = None
    du_lieu: DuLieu
    tier: str | None = None
