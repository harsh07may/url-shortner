from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import JSONResponse, RedirectResponse

from app.codes import make_code
from app.errors import CodeTaken, LinkNotFound
from app.routers import links, redirect
from app.schemas import LinkCreate

app = FastAPI(title="URL Shortener")

@app.exception_handler(LinkNotFound)
async def on_not_found(request: Request, exc: LinkNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": f"no link '{exc}'"})


@app.exception_handler(CodeTaken)
async def on_taken(request: Request, exc: CodeTaken) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": f"code '{exc}' is taken"})


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
async def healthcheck() -> dict:
    """Liveness probe."""
    return {"status": "ok"}

app.include_router(links.router)
app.include_router(redirect.router) 
