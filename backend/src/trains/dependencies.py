from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import get_db
from src.trains.models import Train

async def valid_train_id(
    train_id: str,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> Train:
    """
    Dependency to validate a train_id and return the Train object.
    Raises 404 if not found.
    """
    result = await db.execute(select(Train).where(Train.train_id == train_id))
    train = result.scalars().first()
    
    if not train:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Train {train_id} not found."
        )
    return train
