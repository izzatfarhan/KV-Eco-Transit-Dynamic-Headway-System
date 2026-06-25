from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal

class StationBase(BaseModel):
    name: str = Field(..., description="Official station naming")
    line_name: str = Field(..., description="Transit line taxonomy")
    current_crowd_density: Decimal = Field(default=Decimal("0.00"), description="Real-time density index (0.00 to 1.00)")
    passenger_arrival_rate_per_min: int = Field(default=0, description="Count of inbound commuters per min")

class StationRequest(StationBase):
    """Schema for validating input when creating or updating a station."""
    pass

class StationResponse(StationBase):
    """Schema for returning station data to clients."""
    station_id: int
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
