import secrets
import string

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="URL Shortener")


# ---------------------------------------------------------------------------
# Configuration & in-memory storage (data is lost when the server restarts)
# ---------------------------------------------------------------------------

ALPHABET = string.ascii_letters + string.digits  # characters allowed in a code

store: dict[str, str] = {}   # code -> target URL
clicks: dict[str, int] = {}  # code -> click count


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class LinkCreate(BaseModel):
    """Request body for creating a short link."""

    url: HttpUrl              # destination; validated as a proper http(s) URL
    code: str | None = None   # optional custom code; generated if omitted


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
