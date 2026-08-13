import fastapi  # noqa: EXE002
from fastapi.responses import Response

from ..services.overview import write_overview_excel

router = fastapi.APIRouter()


@router.get("/completeness/overview")
async def get_overview():
    content = write_overview_excel()
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=completeness_overview.xlsx"},
    )
