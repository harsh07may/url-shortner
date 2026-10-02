import redis.asyncio as redis
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
    link = await session.scalar(select(Link)
                                .where(Link.code == code))
    
    if link is None:
        raise LinkNotFound(code)
    return link


async def resolve(session: AsyncSession, cache: redis.Redis, code: str) -> str:
    if cached := await cache.get(f"link:{code}"):
        return cached                                            # hit
    
    link = await get_link(session, code)                         # miss: raises LinkNotFound
    
    await cache.set(f"link:{code}", link.target_url, ex=86_400)  # fill
    return link.target_url


async def record_click(session: AsyncSession, code: str) -> None:
    # atomic increment in the database: no read-modify-write race
    await session.execute(update(Link)
                          .where(Link.code == code)
                          .values(clicks=Link.clicks + 1))
    
    await session.commit()


async def delete_link(session: AsyncSession, cache: redis.Redis, code: str) -> None:
    link = await get_link(session, code)

    await session.delete(link)
    await session.commit()
    await cache.delete(f"link:{code}")                           # invalidate after the commit