# app/services/links.py
# No FastAPI imports here. Services own the transaction.
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.codes import make_code
from app.errors import CodeTaken, LinkNotFound
from app.models import Link


async def create_link(session: AsyncSession, target_url: str, code: str | None = None) -> Link:
    link = Link(code=code or make_code(), target_url=target_url)
    session.add(link)
    
    try:
        await session.commit()
    except IntegrityError as e:              # unique constraint on code
        await session.rollback()
        raise CodeTaken(link.code) from e
    await session.refresh(link)              # load server defaults (created_at)
    return link


async def get_link(session: AsyncSession, code: str) -> Link:
    link = await session.scalar(select(Link).where(Link.code == code))
    
    if link is None:
        raise LinkNotFound(code)
    return link


async def resolve(session: AsyncSession, code: str) -> str:
    return (await get_link(session, code)).target_url


async def record_click(session: AsyncSession, code: str) -> None:
    # atomic increment in the database: no read-modify-write race
    await session.execute(update(Link).where(Link.code == code).values(clicks=Link.clicks + 1))
    await session.commit()


async def delete_link(session: AsyncSession, code: str) -> None:
    link = await get_link(session, code)
    await session.delete(link)
    await session.commit()