# app/cache.py
from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends, Request


def get_redis(request: Request) -> redis.Redis:
    return request.app.state.redis


RedisDep = Annotated[redis.Redis, Depends(get_redis)]