from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from .db import get_db, redis

app = FastAPI(title="music-stats API")

@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    # test Postgres
    result = await db.execute(text("SELECT 1"))
    pg_ok = bool(result.scalar())

    # test Redis
    await redis.set("healthcheck", "ok")
    redis_ok = await redis.get("healthcheck")

    return {"postgres": pg_ok, "redis": redis_ok}
