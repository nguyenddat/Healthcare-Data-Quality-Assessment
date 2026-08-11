# Profiler agent module — design

## Bối cảnh

`test/completeness/check_null.py` hiện có logic trigger + chờ profiler pipeline của OpenMetadata (`get_profiler_pipeline`, `trigger_profiler`, `wait_for_profiler`), tự tạo `OMeta` instance riêng, hardcode `service="noi_tru"`.

`app/modules/open_medata/client.py` đã có sẵn `OMeta` instance dùng chung (`client`) + `om_health_check()`.

Cần: code chạy agent (đầu tiên là profiler) đặt trong module `open_medata`, tái sử dụng `client` có sẵn, không hardcode service name.

## Thiết kế

### 1. Đổi tên `client.py` → `dependencies.py`

`app/modules/open_medata/client.py` → `app/modules/open_medata/dependencies.py`. Nội dung giữ nguyên y hệt (instance `client` + `om_health_check`). Chỉ đổi tên file để phản ánh đúng vai trò: nơi cung cấp dependency (`client`) cho các agent, không phải nơi chứa logic nghiệp vụ.

### 2. Module mới `app/modules/open_medata/agents/profiler.py`

Import `client` từ `..dependencies` (import global, không truyền qua tham số).

3 hàm move nguyên logic từ `check_null.py` sang, tham số hóa `service_name` thay vì hardcode:

```python
def get_profiler_pipeline(service_name: str) -> dict:
    res = client.client.get(
        "/services/ingestionPipelines",
        data={"service": service_name, "pipelineType": "profiler"},
    )
    return res["data"][0]

def trigger_profiler(pipeline_id: str) -> None:
    client.client.post(f"/services/ingestionPipelines/trigger/{pipeline_id}")

def wait_for_profiler(pipeline_fqn: str, start_ts: int, poll_seconds: int = 5) -> None:
    while True:
        statuses = client.get_pipeline_status_between_ts(pipeline_fqn, start_ts, int(time.time() * 1000))
        if statuses:
            latest = max(statuses, key=lambda s: s.timestamp.root)
            if latest.pipelineState in TERMINAL_STATES:
                return
        time.sleep(poll_seconds)
```

`pipelineType="profiler"` giữ hardcode trong `get_profiler_pipeline` — đúng vì file này chỉ lo agent profiler. `TERMINAL_STATES` (set các `PipelineState` kết thúc) move theo cùng module.

Giữ 3 hàm public riêng biệt (không gộp thành 1 hàm `run_profiler`) — caller tự phối hợp gọi.

### 3. Không đụng `test/completeness/check_null.py`

File test giữ nguyên như hiện tại, không refactor.

### 4. Không làm thêm

- Không tạo base class/interface/factory cho agent khác (chưa có use case thứ 2).
- Không thêm error handling mới ngoài logic hiện có.
- Không đổi `om_health_check`.

## Testing

Không có test tự động cho module này (khớp với hiện trạng — `check_null.py` cũng không phải test tự động, là script chạy tay). Verify bằng cách import và gọi thử 3 hàm.
