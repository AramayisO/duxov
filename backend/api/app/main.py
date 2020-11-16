import multiprocessing as mp

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import AppConfig
from app.core.api import api_router
from app.core.queue import JobQueue
from app.music.service import SongService

# Create the ASGI for the app
app = FastAPI()

# Create the Web API
api = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


# Set response header that tells the browser that the server should only be
# accessed using HTTPS instead of using HTTP.
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Strict-Transport-Security"] = (
        "max-age=63072000; "
        "includeSubDomains; "
        "preload"
    )
    return response


# Add all routes to the API
api.include_router(api_router, prefix="/v1")

# Mount endpoints to the app
app.mount("/api", app=api)

# Start redis queue workers in the background
p = mp.Process(target=JobQueue.start_worker)
p.start()

# Initialize SongService
SongService.init()
