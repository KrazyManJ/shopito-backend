from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from starlette.responses import FileResponse

router = APIRouter()

@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")

@router.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        swagger_favicon_url="/favicon.ico",
        title="Shopito API | Swagger UI"
    )

@router.get("/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        redoc_favicon_url="/favicon.ico",
        title="Shopito API | Redoc"
    )