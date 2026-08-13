from datetime import datetime
from io import BytesIO

from metadata.sdk import Tables

from ....core.settings import config
from ...excel.overview import build_overview_workbook
from ...openmetadata.client import get_metadata_client
from ...openmetadata.tags.classification import (
    apply_du_lieu_tag,
    ensure_data_completeness_tags,
)
from ..schemas.overview import DuLieu, TableOverviewInfo

SPARSE_DATA_THRESHOLD = 500

DU_LIEU_TAG_NAME = {
    DuLieu.NO_DATA: "NoData",
    DuLieu.SPARSE_DATA: "SparseData",
    DuLieu.FULL_DATA: "FullData",
}


def classify_du_lieu(so_dong: int) -> DuLieu:
    if so_dong == 0:
        return DuLieu.NO_DATA
    if so_dong < SPARSE_DATA_THRESHOLD:
        return DuLieu.SPARSE_DATA
    return DuLieu.FULL_DATA


def get_table_overview() -> list[TableOverviewInfo]:
    client = get_metadata_client()
    ensure_data_completeness_tags(client)

    rows = []
    for table in Tables.list_all(filters={"service": config.SERVICE_NAME}):
        if table.database.name != config.DATABASE_NAME:
            continue
        fqn = table.fullyQualifiedName.root
        detail = client.get_latest_table_profile(fqn)
        row_count = detail.profile.rowCount if detail.profile else None
        so_dong = max(int(row_count), 0) if row_count is not None else 0

        ngay_tao = None
        if table.lifeCycle and table.lifeCycle.created:
            epoch_ms = table.lifeCycle.created.timestamp.root
            ngay_tao = datetime.fromtimestamp(epoch_ms / 1000).isoformat()

        du_lieu = classify_du_lieu(so_dong)
        apply_du_lieu_tag(client, table, DU_LIEU_TAG_NAME[du_lieu])

        rows.append(TableOverviewInfo(
            ten_bang=table.name.root,
            so_dong=so_dong,
            ngay_tao=ngay_tao,
            du_lieu=du_lieu,
        ))
    return rows


def write_overview_excel() -> bytes:
    rows = get_table_overview()
    wb = build_overview_workbook(rows)
    buffer = BytesIO()
    wb.save(buffer)
    return buffer.getvalue()
