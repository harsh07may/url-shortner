# app/store.py
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends


@dataclass
class LinkRecord:
    code: str
    target_url: str
    clicks: int = 0


Store = dict[str, LinkRecord]
_store: Store = {}


def get_store() -> Store:
    return _store


StoreDep = Annotated[Store, Depends(get_store)] 