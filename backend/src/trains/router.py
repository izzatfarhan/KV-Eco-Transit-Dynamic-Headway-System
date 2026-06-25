from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import get_db
from src.trains import models, schemas, dependencies

router = APIRouter()

@router.get("/", response_model=List[schemas.TrainResponse])
async def get_all_trains(db: Annotated[AsyncSession, Depends(get_db)]):
    """
    Retrieve all moving and stopped trains across the network.
    """
    result = await db.execute(select(models.Train))
    trains = result.scalars().all()
    return trains

# Using Annotated for idiomatic dependency injection per AGENTS.md
TrainDep = Annotated[models.Train, Depends(dependencies.valid_train_id)]

@router.get("/{train_id}", response_model=schemas.TrainResponse)
async def get_train(train: TrainDep):
    """
    Retrieve a specific train's live status and telemetry.
    The dependency validation handles the 404 if not found.
    """
    return train
