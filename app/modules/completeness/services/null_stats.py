from io import BytesIO
from pathlib import Path

from metadata.sdk import Tables
from openpyxl import load_workbook

from ....core.settings import config
from ...excel.null_stats import append_null_stats_sheet
from ...excel.overview import extract_tiered_table_names
from ...openmetadata.client import get_metadata_client
from ..schemas.null_stats import ColumnNullInfo, NullPhanLoai

OUTPUT_PATH = Path("output/completeness_overview.xlsx")


def classify_null(so_luong_null: float | None) -> NullPhanLoai:
    if so_luong_null:
        return NullPhanLoai.REVIEW
    return NullPhanLoai.OK


def get_null_stats(tiered_names: list[str]) -> list[ColumnNullInfo]:
    tiered_set = set(tiered_names)
    client = get_metadata_client()

    rows = []
    for table in Tables.list_all(filters={"service": config.SERVICE_NAME}):
        if table.database.name != config.DATABASE_NAME:
            continue
        if table.name.root not in tiered_set:
            continue
        fqn = table.fullyQualifiedName.root
        detail = client.get_latest_table_profile(fqn)
        for col in detail.columns:
            p = col.profile
            so_luong_null = p.nullCount if p else None
            ty_le_null = (
                round(p.nullProportion * 100, 2)
                if p and p.nullProportion is not None
                else None
            )
            rows.append(ColumnNullInfo(
                ten_bang=table.name.root,
                ten_cot=col.name.root,
                so_luong_null=so_luong_null,
                ty_le_null=ty_le_null,
                phan_loai=classify_null(so_luong_null),
                ghi_chu="",
            ))
    return rows


def write_null_stats_excel(file_bytes: bytes) -> Path:
    wb = load_workbook(BytesIO(file_bytes))
    tiered_names = extract_tiered_table_names(wb["Overview"])
    rows = get_null_stats(tiered_names)
    append_null_stats_sheet(wb, rows)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUTPUT_PATH)
    return OUTPUT_PATH
