# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.db import engine
from app.errors import CodeTaken, LinkNotFound
from app.routers import links, redirect


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(title="Shortener", lifespan=lifespan)


@app.exception_handler(LinkNotFound)
async def on_not_found(request: Request, exc: LinkNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": f"no link '{exc}'"})


@app.exception_handler(CodeTaken)
async def on_taken(request: Request, exc: CodeTaken) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": f"code '{exc}' is taken"})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(links.router)
app.include_router(redirect.router)      # catch-all /{code} goes last