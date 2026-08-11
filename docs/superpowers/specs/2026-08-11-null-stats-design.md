# Null stats module — design

## Bối cảnh

Bước 2 của module completeness, nối tiếp `overview` (xem `2026-08-11-completeness-overview-design.md`). Luồng chuẩn:

1. Người dùng gọi `GET /completeness/overview` lấy Excel (sheet `Overview`: `ten_bang`, `so_dong`, `phan_tang`, `phan_loai`).
2. Người dùng tự gán `phan_tang` (dropdown data validation có sẵn) cho từng bảng, lưu file.
3. Người dùng gọi API mới, upload lại Excel đã gán tier.
4. API xác định các bảng Tier 1, thống kê null/nan cho từng cột của các bảng đó, thêm sheet mới vào **chính file Excel đã upload**, trả về.

Repo đã có sẵn:
- `app/modules/completeness/{routes,services,schemas}/overview.py` — pattern tham khảo (style Excel, cách lọc `Tables.list_all` theo `service`+`database`, cách lấy `client.get_latest_table_profile(fqn)`).
- `test/completeness/check_null.py` — ví dụ đọc `col.profile.nullProportion`, `col.profile.nullCount` từ `detail.columns`.
- `metadata.generated.schema.entity.data.table.ColumnProfile`: có sẵn `nullCount`, `nullProportion` (không cần tự tính).
- `metadata.generated.schema.entity.data.table.Column.constraint`: `Constraint.NOT_NULL` nếu cột có ràng buộc not-null, ngược lại `None`/giá trị khác.

## Thiết kế

Module mới `null_stats`, song song `overview`, không sửa code cũ.

### 1. Dependencies

Thêm `python-multipart` vào `requirements.txt` (FastAPI cần để nhận `UploadFile`).

### 2. `app/modules/completeness/schemas/null_stats.py`

```python
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

### 3. `app/modules/completeness/services/null_stats.py`

Import `client` từ `..open_medata.dependencies`, `config` từ `..core.setting`, `Tables` từ `metadata.sdk`, `Constraint` từ `metadata.generated.schema.entity.data.table`. Import `HEADER_LABELS`, `PhanTang` từ `..schemas.overview` (tái dùng label để tìm đúng cột trong sheet Overview).

```python
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


def extract_tier1_table_names(ws) -> list[str]:
    # đọc header row 1, match theo HEADER_LABELS["ten_bang"] / HEADER_LABELS["phan_tang"]
    # duyệt từ row 2, thu ten_bang có phan_tang == PhanTang.TIER_1.value
    ...


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


def write_null_stats_excel(file_bytes: bytes) -> Path:
    wb = load_workbook(BytesIO(file_bytes))
    tier1_names = extract_tier1_table_names(wb["Overview"])
    rows = get_null_stats(tier1_names)
    _append_null_stats_sheet(wb, rows)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUTPUT_PATH)
    return OUTPUT_PATH


def _append_null_stats_sheet(wb, rows: list[ColumnNullInfo]) -> None:
    # tạo sheet "Null_Stats", ghi header (Vietnamese labels), ghi từng row
    # style: header fill xanh đậm giống Overview, border, column width,
    # tô màu cell phan_loai theo NULL_PHAN_LOAI_FILL (danger đỏ, review vàng, ok xanh, not_profiled xám)
    # freeze_panes="A2", auto_filter
    ...
```

`OUTPUT_PATH` dùng lại `output/completeness_overview.xlsx` — ghi đè mỗi lần gọi, khớp convention "không giữ lịch sử file cũ" của `overview`.

Style code (header fill, border, column width, freeze panes, autofilter) viết riêng trong file này, không tách abstraction chung với `overview.py` — mới có 2 sheet dùng, chưa đến ngưỡng refactor.

### 4. `app/modules/completeness/routes/null_stats.py`

```python
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

### 5. `app/main.py`

Thêm `include_router` cho router `null_stats` (bên cạnh router `overview` đã có).

### 6. Không làm

- Không tự tính null count/percentage từ query DB — dùng nguyên `col.profile.nullCount`/`nullProportion` từ OpenMetadata (không trigger profiler, khớp bước 1).
- Không lưu/khớp theo `fqn` — match Tier 1 theo `ten_bang` (tên bảng) như sheet Overview hiện có, chấp nhận rủi ro trùng tên nếu có (chưa gặp case này ở service `noi_tru`).
- Không validate file upload (sheet thiếu, format sai...) — không try/except, khớp triết lý "không thêm error handling cho case chưa xảy ra" của bước 1.
- Không giữ lịch sử file, không thêm timestamp vào tên file output.
- Không sửa `overview.py` (routes/services/schemas) hay `dependencies.py`.
- Không tạo abstraction style Excel dùng chung giữa `overview` và `null_stats`.

## Testing

Không có test tự động (khớp hiện trạng project). Verify: gọi `GET /completeness/overview?service_name=noi_tru`, mở file, gán vài dòng `phan_tang = "Tier 1 - Bảng lõi"`, lưu, upload qua `POST /completeness/null-stats`. Kiểm tra file trả về vẫn còn sheet `Overview` nguyên vẹn + sheet `Null_Stats` mới chỉ chứa cột của các bảng Tier 1, giá trị `phan_loai` hợp lý theo `nullable` + `ty_le_null`.
