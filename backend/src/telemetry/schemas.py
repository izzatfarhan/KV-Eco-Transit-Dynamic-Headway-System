from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TelemetryLogBase(BaseModel):
    station_id: int
    tap_in_count: int
    tap_out_count: int
    estimated_platform_count: int

class TelemetryLogRequest(TelemetryLogBase):
    """Schema for logging new tap events."""
    pass

class TelemetryLogResponse(TelemetryLogBase):
    """Schema for outputting telemetry log records."""
    log_id: int
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)
