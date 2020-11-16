from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse

import app.music.router as music

api_router = APIRouter(default_response_class=JSONResponse)
doc_router = APIRouter()


@api_router.get("/healthcheck", include_in_schema=False)
async def healthcheck():
    return {"status": "ok"}


@doc_router.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return JSONResponse(
        get_openapi(
            title="REST API Documentation",
            version=1,
            routes=api_router.routes
        )
    )


@doc_router.get("/", include_in_schema=False)
async def get_api_docs():
    return get_redoc_html(
        openapi_url="/api/v1/docs/openapi.json",
        title="REST API Documentation"
    )


api_router.include_router(doc_router, prefix="/docs")
api_router.include_router(music.router, prefix="/music")
