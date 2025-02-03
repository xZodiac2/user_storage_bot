from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///database/storage/database.db", echo=True)
get_session = async_sessionmaker(engine)