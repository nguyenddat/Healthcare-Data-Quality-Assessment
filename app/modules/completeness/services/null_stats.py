from pathlib import Path
from io import BytesIO

from metadata.sdk import Tables
from metadata.generated.schema.entity.data.table import Constraint
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from ....core.setting import config
from ...open_medata.dependencies import client
from ..schemas.overview import PhanTang
from .overview import HEADER_LABELS as OVERVIEW_HEADER_LABELS
from ..schemas.null_stats import ColumnNullInfo, NullableStatus, NullPhanLoai

OUTPUT_PATH = Path("output/completeness_overview.xlsx")

NULL_STATS_HEADER_LABELS = {
    "ten_bang": "Tên bảng",
    "ten_cot": "Tên cột",
    "nullable": "Ràng buộc null",
    "so_luong_null": "Số lượng null",
    "tong_so_dong": "Tổng số dòng",
    "ty_le_null": "Tỷ lệ null (%)",
    "phan_loai": "Phân loại",
}

NULL_PHAN_LOAI_FILL = {
    "danger": "FFC7CE",
    "review": "FFEB9C",
    "ok": "C6EFCE",
    "not_profiled": "D9D9D9",
}


def classify_null(nullable: NullableStatus, ty_le_null: float | None) -> NullPhanLoai:
    if ty_le_null is None:
        return NullPhanLoai.NOT_PROFILED
    if nullable == NullableStatus.NOT_NULLABLE:
        return NullPhanLoai.DANGER if ty_le_null > 5 else NullPhanLoai.OK
    if ty_le_null > 90:
        return NullPhanLoai.DANGER
    if ty_le_null > 10:
        return NullPhanLoai.REVIEW
    return NullPhanLoai.OK


def extract_tier1_table_names(ws: Worksheet) -> list[str]:
    header = {cell.value: idx for idx, cell in enumerate(ws[1], start=1)}
    ten_bang_col = header[OVERVIEW_HEADER_LABELS["ten_bang"]]
    phan_tang_col = header[OVERVIEW_HEADER_LABELS["phan_tang"]]
    names = []
    for row in ws.iter_rows(min_row=2):
        if row[phan_tang_col - 1].value == PhanTang.TIER_1.value:
            names.append(row[ten_bang_col - 1].value)
    return names


def get_null_stats(tier1_names: list[str]) -> list[ColumnNullInfo]:
    tier1_set = set(tier1_names)
    rows = []
    for table in Tables.list_all(filters={"service": config.SERVICE_NAME}):
        if table.database.name != config.DATABASE_NAME:
            continue
        if table.name.root not in tier1_set:
            continue
        fqn = table.fullyQualifiedName.root
        detail = client.get_latest_table_profile(fqn)
        row_count = detail.profile.rowCount if detail.profile else None
        for col in detail.columns:
            p = col.profile
            nullable = (
                NullableStatus.NOT_NULLABLE
                if col.constraint == Constraint.NOT_NULL
                else NullableStatus.NULLABLE
            )
            ty_le_null = (
                round(p.nullProportion * 100, 2)
                if p and p.nullProportion is not None
                else None
            )
            rows.append(ColumnNullInfo(
                ten_bang=table.name.root,
                ten_cot=col.name.root,
                nullable=nullable,
                so_luong_null=p.nullCount if p else None,
                tong_so_dong=row_count,
                ty_le_null=ty_le_null,
                phan_loai=classify_null(nullable, ty_le_null),
            ))
    return rows


def _append_null_stats_sheet(wb, rows: list[ColumnNullInfo]) -> None:
    ws = wb.create_sheet("Null_Stats")
    fields = list(NULL_STATS_HEADER_LABELS.keys())

    header_fill = PatternFill("solid", fgColor="305496")
    header_font = Font(bold=True, color="FFFFFF")
    thin = Side(style="thin", color="B7B7B7")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for col_idx, field in enumerate(fields, start=1):
        cell = ws.cell(row=1, column=col_idx, value=NULL_STATS_HEADER_LABELS[field])
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border

    dumped = [row.model_dump() for row in rows]

    for row_idx, data in enumerate(dumped, start=2):
        for col_idx, field in enumerate(fields, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=data[field])
            cell.border = border
            cell.alignment = Alignment(vertical="center")
        phan_loai_col = fields.index("phan_loai") + 1
        fill = PatternFill("solid", fgColor=NULL_PHAN_LOAI_FILL.get(data["phan_loai"], "FFFFFF"))
        ws.cell(row=row_idx, column=phan_loai_col).fill = fill

    for col_idx, field in enumerate(fields, start=1):
        max_len = max(
            [len(NULL_STATS_HEADER_LABELS[field])]
            + [len(str(data[field])) for data in dumped]
            + [1]
        )
        ws.column_dimensions[get_column_letter(col_idx)].width = max_len + 4

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions


def write_null_stats_excel(file_bytes: bytes) -> Path:
    wb = load_workbook(BytesIO(file_bytes))
    tier1_names = extract_tier1_table_names(wb["Overview"])
    rows = get_null_stats(tier1_names)
    _append_null_stats_sheet(wb, rows)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUTPUT_PATH)
    return OUTPUT_PATH
