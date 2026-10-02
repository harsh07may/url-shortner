# app/routers/redirect.py
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.routers.links import Code
from app.services import links as svc
from app.store import StoreDep

router = APIRouter()


@router.get("/{code}")
async def follow(code: Code, store: StoreDep) -> RedirectResponse:
    target = await svc.resolve(store, code)
    await svc.record_click(store, code)
    return RedirectResponse(target, status_code=302)