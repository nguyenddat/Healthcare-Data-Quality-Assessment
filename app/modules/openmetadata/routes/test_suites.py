import fastapi

from ..test_cases.pipeline import (
    run_constant_value_test_pipelines,
    run_dirty_value_test_pipelines,
)

router = fastapi.APIRouter()


@router.post("/openmetadata/test-suites/run/dirty-value")
async def post_run_dirty_value_test_suites():
    triggered = run_dirty_value_test_pipelines()
    return {"triggered": triggered}


@router.post("/openmetadata/test-suites/run/constant-value")
async def post_run_constant_value_test_suites():
    triggered = run_constant_value_test_pipelines()
    return {"triggered": triggered}
