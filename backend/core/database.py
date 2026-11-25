from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()  # Load environment variables from .env file


# Create the SQLAlchemy engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)
base = declarative_base()

session_local = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)



async def get_db():
    async with session_local() as db:
        try:
            yield db
        finally:
            await db.close()

