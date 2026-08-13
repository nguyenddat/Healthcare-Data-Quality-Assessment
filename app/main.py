import warnings  # noqa: EXE002
from contextlib import asynccontextmanager

warnings.filterwarnings("ignore", category=UserWarning)

from fastapi import FastAPI

from app.modules.completeness.routes.null_stats import router as null_stats_router
from app.modules.completeness.routes.overview import router as overview_router
from app.modules.openmetadata.routes.test_suites import router as test_suites_router
from app.modules.openmetadata.test_cases.constant_value import (
    create_constant_value_test_cases,
)
from app.modules.openmetadata.test_cases.dirty_values import (
    create_dirty_value_test_cases,
)
from app.modules.openmetadata.test_cases.pipeline import create_table_test_pipelines


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_dirty_value_test_cases()
    create_constant_value_test_cases()
    create_table_test_pipelines()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(overview_router)
app.include_router(null_stats_router)
app.include_router(test_suites_router)
