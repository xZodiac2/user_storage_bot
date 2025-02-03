from .core import *
from .orm import *
from .crud import *

async def init_db():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
