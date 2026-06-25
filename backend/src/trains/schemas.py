from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class TrainBase(BaseModel):
    train_id: str
    current_station_id: Optional[int] = None
    status: str
    current_speed: Decimal = Field(default=Decimal("0.00"))
    headway_buffer_seconds: int = Field(default=180)

class TrainRequest(TrainBase):
    """Schema for updating train location and status from telemetry feeds."""
    pass

class TrainResponse(TrainBase):
    """Schema for returning train data."""
    last_ping_time: datetime
    
    model_config = ConfigDict(from_attributes=True)
