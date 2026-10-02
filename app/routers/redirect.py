# app/routers/redirect.py
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.cache import RedisDep
from app.db import SessionDep
from app.routers.links import Code
from app.services import links as redirect_svc

router = APIRouter()


@router.get("/{code}")
async def follow(code: Code, session: SessionDep, cache: RedisDep) -> RedirectResponse:
    target = await redirect_svc.resolve(session, cache, code)
    await redirect_svc.record_click(session, code)
    return RedirectResponse(target, status_code=302)