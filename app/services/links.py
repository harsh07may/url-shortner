# No FastAPI imports here.
from app.codes import make_code
from app.errors import CodeTaken, LinkNotFound
from app.store import LinkRecord, Store


async def create_link(store: Store, target_url: str, code: str | None = None) -> LinkRecord:
    code = code or make_code()
    if code in store:
        raise CodeTaken(code)
    store[code] = LinkRecord(code=code, target_url=target_url)
    return store[code]


async def get_link(store: Store, code: str) -> LinkRecord:
    if code not in store:
        raise LinkNotFound(code)
    return store[code]


async def resolve(store: Store, code: str) -> str:
    return (await get_link(store, code)).target_url


async def record_click(store: Store, code: str) -> None:
    store[code].clicks += 1


async def delete_link(store: Store, code: str) -> None:
    await get_link(store, code)
    del store[code]