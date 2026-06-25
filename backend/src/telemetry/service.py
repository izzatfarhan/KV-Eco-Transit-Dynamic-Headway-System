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
            
            # Processing would happen here (saving to DB via AsyncSession)
            
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
