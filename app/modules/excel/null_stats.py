from ..completeness.schemas.null_stats import ColumnNullInfo
from .utils import write_sheet

NULL_STATS_HEADER_LABELS = {
    "ten_bang": "Tên bảng",
    "ten_cot": "Tên cột",
    "so_luong_null": "Số dòng NULL",
    "ty_le_null": "Tỷ lệ null (%)",
    "phan_loai": "Phân loại",
    "ghi_chu": "Ghi chú",
}

NULL_PHAN_LOAI_FILL = {
    "review": "FFEB9C",
    "ok": "C6EFCE",
}


def append_null_stats_sheet(wb, rows: list[ColumnNullInfo]) -> None:
    ws = wb.create_sheet("Null_Stats")
    write_sheet(
        ws,
        NULL_STATS_HEADER_LABELS,
        [row.model_dump() for row in rows],
        fill_map=NULL_PHAN_LOAI_FILL,
        fill_field="phan_loai",
    )
