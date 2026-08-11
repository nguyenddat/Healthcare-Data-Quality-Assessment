import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from fastapi import FastAPI

from app.modules.completeness.routes.overview import router as overview_router
from app.modules.completeness.routes.null_stats import router as null_stats_router

app = FastAPI()
app.include_router(overview_router)
app.include_router(null_stats_router)
