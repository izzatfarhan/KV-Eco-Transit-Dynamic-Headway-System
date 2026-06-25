import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.stations.models import Station
from src.trains.models import Train

logger = logging.getLogger(__name__)

# Constants based on PRD requirements
CONGESTION_THRESHOLD = 0.75
OFF_PEAK_HEADWAY_SECONDS = 180
COMPRESSED_PEAK_HEADWAY_SECONDS = 90

async def evaluate_station_density(db: AsyncSession, station_id: int):
    """
    Evaluates current crowd density at a given station and adjusts the headways
    of incoming trailing trains to absorb peak surges.
    """
    result = await db.execute(select(Station).where(Station.station_id == station_id))
    station = result.scalars().first()
    
    if not station:
        logger.warning(f"Station {station_id} not found during density evaluation.")
        return
    
    # ---------------------------------------------------------
    # Algorithm Breakdown: Dynamic Headway Logic
    # 1. Check if the station's density exceeds the surge threshold (e.g. 0.75).
    # 2. If true, find all active trailing trains approaching this station.
    # 3. Compress their headways from 180s to 90s to quickly absorb the crowd.
    # ---------------------------------------------------------
    
    if float(station.current_crowd_density) > CONGESTION_THRESHOLD:
        logger.info(f"SURGE DETECTED at Station {station.name}. Density: {station.current_crowd_density}")
        
        # Find trains currently assigned to this station
        trains_result = await db.execute(
            select(Train).where(
                Train.current_station_id == station_id,
                Train.status == 'Moving'
            )
        )
        trailing_trains = trains_result.scalars().all()
        
        for train in trailing_trains:
            if train.headway_buffer_seconds > COMPRESSED_PEAK_HEADWAY_SECONDS:
                train.headway_buffer_seconds = COMPRESSED_PEAK_HEADWAY_SECONDS
                logger.info(f"Compressed headway for Train {train.train_id} to 90s.")
        
        # Trigger Standby Allocation
        await _release_pocket_trains(db, station_id)
        
        await db.commit()
    else:
        # Revert to off-peak parameters if density normalizes
        await _normalize_headways(db, station_id)


async def _release_pocket_trains(db: AsyncSession, target_station_id: int):
    """
    Automated Standby Allocation: Triggers signaling to release pre-staged 
    'pocket trains' from siding tracks to absorb heavy peak bottlenecks.
    """
    # ---------------------------------------------------------
    # Algorithm Breakdown: Pocket Train Dispatch
    # 1. Query for trains with status 'Pocket_Standby' nearest to the target.
    # 2. Update their status to 'Moving' and assign them to the surging station.
    # 3. This injects additional capacity before cascading delays occur.
    # ---------------------------------------------------------
    result = await db.execute(select(Train).where(Train.status == 'Pocket_Standby'))
    pocket_trains = result.scalars().all()
    
    if pocket_trains:
        # Release the first available pocket train
        released_train = pocket_trains[0]
        released_train.status = 'Moving'
        released_train.current_station_id = target_station_id
        released_train.headway_buffer_seconds = COMPRESSED_PEAK_HEADWAY_SECONDS
        
        logger.info(f"DISPATCHED Pocket Train {released_train.train_id} to Station {target_station_id}")


async def _normalize_headways(db: AsyncSession, station_id: int):
    """
    Reverts incoming trains back to off-peak safety margins when congestion clears.
    """
    result = await db.execute(
        select(Train).where(
            Train.current_station_id == station_id,
            Train.headway_buffer_seconds < OFF_PEAK_HEADWAY_SECONDS
        )
    )
    trains = result.scalars().all()
    
    for train in trains:
        train.headway_buffer_seconds = OFF_PEAK_HEADWAY_SECONDS
        logger.debug(f"Normalized headway for Train {train.train_id} back to 180s.")
    
    if trains:
        await db.commit()
