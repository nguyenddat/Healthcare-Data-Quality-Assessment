# Completeness overview module — design

## Bối cảnh

Cần bước 1 của module completeness: lấy bức tranh tổng thể toàn database — bảng nào rỗng, bảng nào ít dữ liệu (< t dòng), bảng nào có đủ dữ liệu. Đầu ra là file Excel, phục vụ qua API route trả file trực tiếp.

Repo đã có sẵn:
- `app/modules/open_medata/dependencies.py`: `client` (instance `OMeta`) + `om_health_check()`.
- `app/modules/open_medata/agents/profiler.py`: trigger/wait profiler pipeline (không dùng ở bước này — chỉ đọc profile có sẵn).
- Thư mục rỗng đã tạo sẵn: `app/modules/completeness/{routes,schemas,services}/`.
- `app/main.py` rỗng, `requirements.txt` chưa có `fastapi`/`uvicorn`/`openpyxl`.

Tham khảo cách lấy row count: `test/completeness/check_null.py` dùng `Tables.list_all(filters={"service": ...})` (từ `metadata.sdk`) + `om.get_latest_table_profile(fqn)` trả về `Table` entity, field `detail.profile.rowCount` (float, có thể `None` nếu bảng chưa từng chạy profiler).

## Thiết kế

### 1. Dependencies

Thêm vào `requirements.txt`: `fastapi`, `uvicorn`, `openpyxl` (cần cho `pandas.to_excel`).

### 2. `app/main.py`

Dựng `FastAPI()` app, `include_router` router completeness.

### 3. `app/modules/completeness/schemas/overview.py`

```python
class TableRowInfo(BaseModel):
    ten_bang: str
    so_dong: float | None
    phan_loai: str
```

### 4. `app/modules/completeness/services/overview.py`

Import `client` từ `..open_medata.dependencies` (import global, không truyền tham số — theo pattern `profiler.py`).

```python
def classify(row_count: float | None, threshold: int) -> str:
    if row_count is None:
        return "not_profiled"
    if row_count == 0:
        return "empty"
    if row_count < threshold:
        return "sparse"
    return "sufficient"


def get_table_rows(service_name: str) -> list[TableRowInfo]:
    # Tables.list_all(filters={"service": service_name})
    # với mỗi table: fqn = table.fullyQualifiedName.root
    # detail = client.get_latest_table_profile(fqn)
    # row_count = detail.profile.rowCount if detail.profile else None
    ...


def write_overview_excel(service_name: str, threshold: int = 300) -> Path:
    rows = get_table_rows(service_name)
    for r in rows:
        r.phan_loai = classify(r.so_dong, threshold)
    # pandas.DataFrame -> to_excel("output/completeness_overview.xlsx", index=False)
    # tạo thư mục output/ nếu chưa có
    ...
```

Cột Excel: `ten_bang`, `so_dong`, `phan_loai`. 4 giá trị `phan_loai`: `empty`, `sparse`, `not_profiled`, `sufficient`.

### 5. `app/modules/completeness/routes/overview.py`

```python
router = APIRouter()

@router.get("/completeness/overview")
def get_completeness_overview(service_name: str, threshold: int = 300):
    path = write_overview_excel(service_name, threshold)
    return FileResponse(
        path,
        filename="completeness_overview.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
```

`service_name`: query param bắt buộc. `threshold`: mặc định 300.

### 6. File output

`output/completeness_overview.xlsx` — ghi đè mỗi lần gọi route. Thư mục `output/` tạo tự động nếu chưa tồn tại.

### 7. Không làm

- Không trigger profiler pipeline — chỉ đọc `get_latest_table_profile` (latest có sẵn).
- Không filter theo database/schema — chỉ filter theo `service_name`.
- Không giữ lịch sử file cũ, không thêm timestamp vào tên file.
- Không thêm error handling ngoài case `not_profiled` (vd không try/except quanh call OpenMetadata).
- Không tạo base class/abstraction cho các bước completeness sau này (chưa có use case thứ 2).
- Không đổi `profiler.py` hay `dependencies.py`.

## Testing

Không có test tự động (khớp hiện trạng project). Verify bằng cách chạy `uvicorn app.main:app` rồi gọi `GET /completeness/overview?service_name=noi_tru`, kiểm tra file Excel trả về đúng 3 cột và giá trị `phan_loai` hợp lý.
