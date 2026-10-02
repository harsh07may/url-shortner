from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from nanoid import generate
from fastapi.responses import RedirectResponse
from pydantic import AnyHttpUrl
from models import create_db_and_tables, SessionDep, ShortUrl


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def health_check():
    return { "status": "healthy"}


@app.post("/shorten")
def shorten_url(url: AnyHttpUrl, session: SessionDep):
    code = generate(size=5)
    short_url = ShortUrl(code=code, original_url=str(url))
    session.add(short_url)
    session.commit()
    return {"url": f"http://127.0.0.1:8000/{code}"}

@app.get("/{code}")
def get_link(code: str, session: SessionDep):
    short_url = session.get(ShortUrl, code)
    if short_url is None:
        raise HTTPException(status_code=404, detail="Short link not found")
    return RedirectResponse(short_url.original_url)
