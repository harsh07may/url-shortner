# app/routers/links.py
from typing import Annotated

from fastapi import APIRouter, Path

from app.core.config import settings
from app.schemas import LinkCreate, LinkOut
from app.services import links as svc
from app.store import StoreDep

router = APIRouter(prefix="/links", tags=["links"])

Code = Annotated[str, Path(min_length=4, max_length=16)]


def to_out(link) -> LinkOut:
    return LinkOut(code=link.code, short_url=f"{settings.base_url}/{link.code}",
                   target_url=link.target_url, clicks=link.clicks)


@router.post("", status_code=201)
async def create(payload: LinkCreate, store: StoreDep) -> LinkOut:
    return to_out(await svc.create_link(store, str(payload.url), payload.code))


@router.get("/{code}")
async def read(code: Code, store: StoreDep) -> LinkOut:
    return to_out(await svc.get_link(store, code))


@router.delete("/{code}", status_code=204)
async def remove(code: Code, store: StoreDep) -> None:
    await svc.delete_link(store, code)