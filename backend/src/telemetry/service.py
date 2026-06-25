import httpx
import asyncio
import logging
from typing import Optional

# Using google.transit.gtfs_realtime_pb2 (typically imported after installing gtfs-realtime-bindings)
try:
    from google.transit import gtfs_realtime_pb2
except ImportError:
    gtfs_realtime_pb2 = None

logger = logging.getLogger(__name__)

OPEN_DATA_URL = "https://api.data.gov.my/gtfs-realtime/vehicle-positions"

async def fetch_live_telemetry(api_key: Optional[str] = None):
    """
    Fetch live GTFS-Realtime telemetry streams from the Malaysian Open Data API.
    Runs every 30 seconds to update train positions and speed.
    """
    if not gtfs_realtime_pb2:
        logger.error("gtfs-realtime-bindings is not installed.")
        return

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(OPEN_DATA_URL, headers=headers, timeout=10.0)
            response.raise_for_status()
            
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            # Process entities and save to DB
            from src.database import SessionFactory
            from src.trains.models import Train
            from sqlalchemy.future import select
            from datetime import datetime
            
            async with SessionFactory() as db:
                for entity in feed.entity:
                    if entity.HasField('vehicle'):
                        vehicle = entity.vehicle
                        v_id = vehicle.vehicle.id
                        if not v_id: 
                            continue
                        
                        # Map GTFS Realtime CurrentStatus enum
                        status_map = {
                            0: "Incoming",
                            1: "Stopped",
                            2: "Moving"
                        }
                        v_status = status_map.get(vehicle.current_status, "Moving")
                        v_speed = vehicle.position.speed if vehicle.position.HasField('speed') else 0.0
                        
                        result = await db.execute(select(Train).where(Train.train_id == v_id))
                        train = result.scalars().first()
                        
                        if train:
                            train.status = v_status
                            train.current_speed = v_speed
                            train.last_ping_time = datetime.utcnow()
                        else:
                            new_train = Train(
                                train_id=v_id,
                                status=v_status,
                                current_speed=v_speed,
                                last_ping_time=datetime.utcnow()
                            )
                            db.add(new_train)
                await db.commit()
            
            logger.info(f"Successfully processed {len(feed.entity)} telemetry entities.")
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred while fetching telemetry: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during telemetry ingestion: {e}", exc_info=True)

async def ingestion_loop(api_key: Optional[str] = None):
    """
    Background worker loop to continuously fetch data every 30 seconds.
    """
    while True:
        logger.info("Fetching new telemetry tick...")
        await fetch_live_telemetry(api_key)
        await asyncio.sleep(30)
