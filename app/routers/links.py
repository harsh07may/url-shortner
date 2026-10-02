# app/routers/links.py
from typing import Annotated

from fastapi import APIRouter, Path

from app.core.config import settings
from app.cache import RedisDep
from app.db import SessionDep
from app.models import Link
from app.schemas import LinkCreate, LinkOut
from app.services import links as links_svc

router = APIRouter(prefix="/links", tags=["links"])

Code = Annotated[str, Path(min_length=4, max_length=16)]


def to_out(link: Link) -> LinkOut:
    return LinkOut(code=link.code, short_url=f"{settings.base_url}/{link.code}",
                   target_url=link.target_url, clicks=link.clicks)


@router.post("", status_code=201)
async def create(payload: LinkCreate, session: SessionDep) -> LinkOut:
    return to_out(await links_svc.create_link(session, str(payload.url), payload.code))


@router.get("/{code}")
async def read(code: Code, session: SessionDep) -> LinkOut:
    return to_out(await links_svc.get_link(session, code))


@router.delete("/{code}", status_code=204)
async def remove(code: Code, session: SessionDep, cache: RedisDep) -> None:
    await links_svc.delete_link(session, cache, code)