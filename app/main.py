import secrets
import string
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field, HttpUrl, field_validator

app = FastAPI(title="URL Shortener")


# ---------------------------------------------------------------------------
# Configuration & in-memory storage (data is lost when the server restarts)
# ---------------------------------------------------------------------------

ALPHABET = string.ascii_letters + string.digits  # characters allowed in a code

store: dict[str, str] = {}   # code -> target URL
clicks: dict[str, int] = {}  # code -> click count
RESERVED = {"docs", "redoc", "openapi.json", "links", "health"}

Code = Annotated[str, Path(min_length=4, max_length=16)]





# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------
class LinkNotFound(Exception): ...
class CodeTaken(Exception): ...

@app.exception_handler(LinkNotFound)
async def on_not_found(request: Request, exc: LinkNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": f"no link '{exc}'"})


@app.exception_handler(CodeTaken)
async def on_taken(request: Request, exc: CodeTaken) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": f"code '{exc}' is taken"})

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class LinkCreate(BaseModel):
    """Request body for creating a short link."""
    url: HttpUrl              
    code: str | None = Field(default=None,
                             min_length=6, max_length=16,
                             pattern=r"^[A-Za-z0-9_-]+$")
    @field_validator("code")
    @classmethod
    def not_reserved(cls, v: str | None) -> str | None:
        if v in RESERVED:
            raise ValueError("this code is reserved")
        return v

class LinkOut(BaseModel):
    code: str
    short_url: str
    target_url: str
    clicks: int = 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_code(length: int = 6) -> str:
    """Return a random code using a cryptographically secure generator."""
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def get_target_or_404(code: str) -> str:
    """Look up the target URL for a code, or raise a 404 if it doesn't exist."""
    if code not in store:
        raise HTTPException(status_code=404, detail="link not found")
    return store[code]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
async def healthcheck() -> dict:
    """Liveness probe."""
    return {"status": "ok"}


@app.post("/links", status_code=201)
async def create_link(payload: LinkCreate, request: Request) -> dict:
    """Create a short link, using the caller's custom code or a random one."""
    
    code = payload.code or make_code()

    # Reject codes that are already in use so we never overwrite a link.
    if code in store:
        raise HTTPException(status_code=409, detail="code already taken")

    store[code] = str(payload.url)
    clicks[code] = 0

    return {
        "code": code,
        "short_url": f"{request.base_url}{code}",
    }


@app.get("/links/{code}")
async def get_link(code: str) -> dict:
    """Return details (target URL and click count) for a short link."""
    target_url = get_target_or_404(code)

    return {
        "code": code,
        "target_url": target_url,
        "clicks": clicks[code],
    }

@app.delete("/links/{code}", status_code=204)
async def delete_link(code: str) -> None:
    if code not in store:
        raise HTTPException(status_code=404, detail="link not found")
    
    del store[code]
    del clicks[code]

# Declared last so it doesn't shadow the more specific routes above
# (e.g. "/health" would otherwise be treated as a code).
@app.get("/{code}")
async def follow(code: str) -> RedirectResponse:
    """Redirect to the target URL and record the click."""
    target_url = get_target_or_404(code)

    clicks[code] += 1
    return RedirectResponse(target_url, status_code=302)
