from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute("SELECT 1")
        return {"message": "API Gateway is running and database is connected."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection failed.")


