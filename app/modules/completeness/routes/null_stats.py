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
