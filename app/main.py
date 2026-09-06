import warnings  # noqa: EXE002

warnings.filterwarnings("ignore", category=UserWarning)

from fastapi import FastAPI

from app.modules.completeness.routes.null_stats import router as null_stats_router
from app.modules.completeness.routes.overview import router as overview_router
from app.modules.openmetadata.routes.test_suites import router as test_suites_router

app = FastAPI()
app.include_router(overview_router)
app.include_router(null_stats_router)
app.include_router(test_suites_router)
