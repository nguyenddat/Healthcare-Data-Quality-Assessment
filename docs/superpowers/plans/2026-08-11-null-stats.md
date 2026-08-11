# Null stats module Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `POST /completeness/null-stats` — nhận Excel đã gán tier (output của `/completeness/overview`), tính thống kê null/nan cho cột của các bảng Tier 1, thêm sheet `Null_Stats` vào workbook, trả lại file.

**Architecture:** Module `null_stats` mới, song song `overview`, cùng cấu trúc `routes/services/schemas`. Đọc sheet `Overview` bằng openpyxl để lấy tên bảng Tier 1, query `client.get_latest_table_profile(fqn)` cho từng bảng (OpenMetadata SDK có sẵn), ghi sheet mới vào workbook đã load, lưu đè `output/completeness_overview.xlsx`.

**Tech Stack:** FastAPI (`UploadFile`), openpyxl, `metadata.sdk` (OpenMetadata Python SDK), pydantic.

## Global Constraints

- Chạy Python trong conda env `lc_openmetadata` — mọi lệnh `python`/`pip` phải `conda activate lc_openmetadata` trước.
- YAGNI tuyệt đối — không thêm validate/error handling ngoài spec, không tạo abstraction cho 1-2 use case.
- Không sửa `app/modules/completeness/{routes,services,schemas}/overview.py` hay `app/modules/open_medata/dependencies.py`.
- Không test tự động bằng pytest (project chưa có framework test) — verify bằng smoke-check `python -c` cho logic thuần, và chạy thủ công qua `uvicorn` cho phần cần OpenMetadata thật (khớp `overview` hiện tại).
- Spec đầy đủ: `docs/superpowers/specs/2026-08-11-null-stats-design.md`.

---

### Task 1: Thêm dependency `python-multipart`

**Files:**
- Modify: `requirements.txt`

**Interfaces:**
- Produces: FastAPI có thể nhận `UploadFile` ở route (dùng ở Task 4).

- [ ] **Step 1: Thêm dòng vào requirements.txt**

Append dòng `python-multipart` vào cuối `requirements.txt`.

- [ ] **Step 2: Cài đặt trong conda env**

Run: `conda activate lc_openmetadata && pip install python-multipart`
Expected: `Successfully installed python-multipart-...`

- [ ] **Step 3: Verify import**

Run: `conda activate lc_openmetadata && python -c "import multipart; print('ok')"`
Expected: `ok`

- [ ] **Step 4: Commit**

```bash
git add requirements.txt
git commit -m "chore: add python-multipart dependency for file upload"
```

---

### Task 2: `schemas/null_stats.py`

**Files:**
- Create: `app/modules/completeness/schemas/null_stats.py`

**Interfaces:**
- Produces: `NullableStatus` (enum: `NOT_NULLABLE`, `NULLABLE`), `NullPhanLoai` (enum: `DANGER`, `REVIEW`, `OK`, `NOT_PROFILED`), `ColumnNullInfo` (pydantic model, `use_enum_values=True`, fields `ten_bang: str`, `ten_cot: str`, `nullable: NullableStatus`, `so_luong_null: float | None`, `tong_so_dong: float | None`, `ty_le_null: float | None`, `phan_loai: NullPhanLoai`). Dùng ở Task 3.

- [ ] **Step 1: Viết file schema**

```python
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
```

- [ ] **Step 2: Smoke-test model**

Run:
```bash
conda activate lc_openmetadata && python -c "
from app.modules.completeness.schemas.null_stats import ColumnNullInfo, NullableStatus, NullPhanLoai
row = ColumnNullInfo(ten_bang='t', ten_cot='c', nullable=NullableStatus.NULLABLE, so_luong_null=5, tong_so_dong=100, ty_le_null=5.0, phan_loai=NullPhanLoai.OK)
print(row.model_dump())
"
```
Expected: dict in đúng 7 field, `nullable`/`phan_loai` là plain string (`'nullable'`, `'ok'`) chứ không phải enum object.

- [ ] **Step 3: Commit**

```bash
git add app/modules/completeness/schemas/null_stats.py
git commit -m "feat: add null_stats schema"
```

---

### Task 3: `services/null_stats.py`

**Files:**
- Create: `app/modules/completeness/services/null_stats.py`
- Read (không sửa): `app/modules/completeness/schemas/overview.py` (cần `HEADER_LABELS`, `PhanTang`)

**Interfaces:**
- Consumes: `ColumnNullInfo`, `NullableStatus`, `NullPhanLoai` từ `..schemas.null_stats` (Task 2). `HEADER_LABELS: dict[str,str]`, `PhanTang` từ `..schemas.overview` (đã có). `client` từ `...open_medata.dependencies` (đã có, có method `get_latest_table_profile(fqn: str)`). `config` từ `....core.setting` (đã có, có `SERVICE_NAME`, `DATABASE_NAME`). `Tables.list_all(filters=...)` từ `metadata.sdk` (đã có).
- Produces: `classify_null(nullable, ty_le_null) -> NullPhanLoai`, `extract_tier1_table_names(ws) -> list[str]`, `get_null_stats(tier1_names: list[str]) -> list[ColumnNullInfo]`, `write_null_stats_excel(file_bytes: bytes) -> Path`. Dùng ở Task 4.

- [ ] **Step 1: Viết file service**

```python
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
```

- [ ] **Step 2: Smoke-test `classify_null`**

Run:
```bash
conda activate lc_openmetadata && python -c "
from app.modules.completeness.services.null_stats import classify_null
from app.modules.completeness.schemas.null_stats import NullableStatus, NullPhanLoai

assert classify_null(NullableStatus.NOT_NULLABLE, None) == NullPhanLoai.NOT_PROFILED
assert classify_null(NullableStatus.NOT_NULLABLE, 10) == NullPhanLoai.DANGER
assert classify_null(NullableStatus.NOT_NULLABLE, 3) == NullPhanLoai.OK
assert classify_null(NullableStatus.NULLABLE, 95) == NullPhanLoai.DANGER
assert classify_null(NullableStatus.NULLABLE, 50) == NullPhanLoai.REVIEW
assert classify_null(NullableStatus.NULLABLE, 2) == NullPhanLoai.OK
print('ok')
"
```
Expected: `ok`

- [ ] **Step 3: Smoke-test `extract_tier1_table_names` với workbook giả**

Run:
```bash
conda activate lc_openmetadata && python -c "
from openpyxl import Workbook
from app.modules.completeness.services.null_stats import extract_tier1_table_names

wb = Workbook()
ws = wb.active
ws.append(['Tên bảng', 'Số dòng', 'Phân tầng', 'Phân loại'])
ws.append(['benh_nhan', 1000, 'Tier 1 - Bảng lõi', 'sufficient'])
ws.append(['log_tam', 10, 'Tier 3 - Bảng kỹ thuật', 'sparse'])
ws.append(['chan_doan', 500, 'Tier 1 - Bảng lõi', 'sufficient'])

names = extract_tier1_table_names(ws)
assert names == ['benh_nhan', 'chan_doan'], names
print('ok')
"
```
Expected: `ok`

- [ ] **Step 4: Verify import toàn module (không gọi OpenMetadata)**

Run: `conda activate lc_openmetadata && python -c "from app.modules.completeness.services import null_stats; print('ok')"`
Expected: `ok`

- [ ] **Step 5: Commit**

```bash
git add app/modules/completeness/services/null_stats.py
git commit -m "feat: add null_stats service"
```

---

### Task 4: `routes/null_stats.py` + wire vào `app/main.py`

**Files:**
- Create: `app/modules/completeness/routes/null_stats.py`
- Modify: `app/main.py`

**Interfaces:**
- Consumes: `write_null_stats_excel(file_bytes: bytes) -> Path` từ `..services.null_stats` (Task 3).
- Produces: route `POST /completeness/null-stats`, `router` object export cho `app/main.py`.

- [ ] **Step 1: Viết route**

```python
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

from ..services.null_stats import write_null_stats_excel

router = APIRouter()


@router.post("/completeness/null-stats")
async def post_null_stats(file: UploadFile = File(...)):
    contents = await file.read()
    path = write_null_stats_excel(contents)
    return FileResponse(
        path,
        filename="completeness_overview.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
```

- [ ] **Step 2: Wire vào `app/main.py`**

`app/main.py` hiện tại:
```python
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from fastapi import FastAPI

from app.modules.completeness.routes.overview import router as completeness_router

app = FastAPI()
app.include_router(completeness_router)
```

Sửa thành:
```python
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from fastapi import FastAPI

from app.modules.completeness.routes.overview import router as overview_router
from app.modules.completeness.routes.null_stats import router as null_stats_router

app = FastAPI()
app.include_router(overview_router)
app.include_router(null_stats_router)
```

- [ ] **Step 3: Verify app khởi tạo được (route đăng ký đúng)**

Run:
```bash
conda activate lc_openmetadata && python -c "
from app.main import app
paths = {r.path for r in app.routes}
assert '/completeness/overview' in paths
assert '/completeness/null-stats' in paths
print('ok')
"
```
Expected: `ok`

- [ ] **Step 4: Commit**

```bash
git add app/modules/completeness/routes/null_stats.py app/main.py
git commit -m "feat: add POST /completeness/null-stats route"
```

---

### Task 5: Verify end-to-end thủ công (cần OpenMetadata server thật)

**Files:** không tạo/sửa file — chỉ chạy thủ công.

- [ ] **Step 1: Chạy server**

Run: `conda activate lc_openmetadata && uvicorn app.main:app --reload`

- [ ] **Step 2: Lấy overview**

Gọi `GET http://127.0.0.1:8000/completeness/overview?service_name=noi_tru`, lưu file trả về là `overview.xlsx`.

- [ ] **Step 3: Gán tier**

Mở `overview.xlsx`, ở cột "Phân tầng" gán `Tier 1 - Bảng lõi` cho vài bảng (dùng dropdown data validation có sẵn), lưu file.

- [ ] **Step 4: Gọi null-stats**

Gọi `POST http://127.0.0.1:8000/completeness/null-stats` với multipart form field `file` = `overview.xlsx` đã sửa. Lưu response.

- [ ] **Step 5: Kiểm tra kết quả**

Mở file trả về, xác nhận:
- Sheet `Overview` còn nguyên (tier đã gán vẫn còn).
- Sheet `Null_Stats` mới, chỉ chứa các bảng đã gán Tier 1.
- Cột `Phân loại` tô màu đúng theo `nullable` + `Tỷ lệ null (%)` (not_nullable > 5% → đỏ, nullable > 90% → đỏ, 10-90% → vàng, còn lại → xanh; không có profile → xám).

Nếu đúng, task hoàn tất — không cần commit gì thêm (bước verify thủ công, không sinh code mới).

---

## Self-Review Notes

- **Spec coverage:** Task 1 = dependency (spec §1). Task 2 = schema (spec §2). Task 3 = toàn bộ service logic + styling (spec §3, quy tắc phân loại, `OUTPUT_PATH` dùng lại). Task 4 = route + wiring (spec §4, §5). Task 5 = testing thủ công (khớp spec "Testing"). Không có mục nào trong spec thiếu task tương ứng.
- **Placeholder scan:** Không còn "TBD"/"tương tự Task N" — code đầy đủ trong từng step.
- **Type consistency:** `ColumnNullInfo` (Task 2) dùng đúng field names xuyên suốt Task 3 (`ten_bang`, `ten_cot`, `nullable`, `so_luong_null`, `tong_so_dong`, `ty_le_null`, `phan_loai`) và route Task 4 chỉ truyền `bytes` vào `write_null_stats_excel` — khớp chữ ký định nghĩa ở Task 3.
