import fastapi  # noqa: EXE002
from fastapi import Query
from fastapi.responses import Response

from ..services.overview import write_overview_excel

router = fastapi.APIRouter()


@router.get("/completeness/overview")
async def get_overview(
    schemas: list[str] = Query(
        default=["public"],
        description="Danh sách schema cần duyệt. Truyền lặp lại tham số cho nhiều schema.",
    ),
):
    content = write_overview_excel(schemas)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=completeness_overview.xlsx"},
    )
